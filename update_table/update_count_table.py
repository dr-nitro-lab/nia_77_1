from argparse import ArgumentParser
from datetime import datetime
from typing import Dict, Optional

import pandas as pd
import numpy as np

from json_utils import json2list



def arg_parser():
    parser = ArgumentParser()
    parser.add_argument("--dataset", "-d", type=str, default="D:\\NIA_77_1\\221011")
    parser.add_argument("--cls_json", "-c", type=str, default="classJson")
    parser.add_argument("--excel_path", "-e", type=str, default=None)

    config = parser.parse_args()
    return config


def update_table(config):
    """
    inputs
    --------------
    json_list :     "파일명":{json객체} 쌍으로 저장된 dictionary
    classJsons :      classJson 폴더의 json파일들을 모두 load한 dict를 입력한다. 각 파일들의 내용은 파일명으로 접근할 수 있다.
    excel_path :    if not None, excel_path에 excel 파일 저장
    """

    metadatas = json2list(config.dataset)
    classJsons = json2list(config.cls_json)
    if config.excel_path is None:
        excel_path = os.path.join(config.dataset, Path(config.dataset).name + '.count.xlsx')
    else:
        excel_path = config.excel_path

    # load JSONs
    genre_cd = classJsons["genreCode2Name"].keys()
    genre_nm = classJsons["genreCode2Name"].values()

    inst_cd = classJsons["instCode2Name"].keys()
    inst_nm = classJsons["instCode2Name"].values()

    # define main DataFrame
    # col이 악기 코드, row가 장르 코드인 DataFrame 생성
    table = pd.DataFrame(columns=inst_cd, index=genre_cd)


    ###########################################################################################
    # Construct main table and calculate main statistics
    for json_filename, json_dict in metadatas.items():
        try:
            genre = json_dict["music_type_info"]["music_genre_cd"]
            inst = json_dict["music_type_info"]["instrument_cd"]
            main_inst = json_dict["music_type_info"]["main_instrmt_cd"]

        except KeyError:
            print(f"{json_filename}의 키는 다른 json파일들의 key들과 다르다.")
            continue  # do something when wrong key detected!!

        # 현재는 "instrument_cd" 또는 "main_instrmt_cd" 둘 중 하나만 채워져 있음을 반영
        if inst != "":
            if pd.isnull(table.loc[genre, inst]):
                table[inst][genre] = 1
            else:
                table[inst][genre] += 1
        elif main_inst != "":
            if pd.isnull(table.loc[genre, main_inst]):
                table[main_inst][genre] = 1
            else:
                table[main_inst][genre] += 1

    # Column Multi Index 생성
    idx=[]
    for M,m,n,c in zip(classJsons["instCode2Major"].values(),\
        classJsons["instCode2Minor"].values(),\
            classJsons["instCode2Name"].values(),\
                classJsons["instCode2Name"].keys()):
        idx.append((M,m,n,c))

    table.columns = pd.MultiIndex.from_tuples(idx, names=["대분류","중분류","악기","소분류_코드"])

    # Row Multi Index 생성
    table["대분류"]=classJsons["genreCode2Major"].values()
    table["중분류"]=classJsons["genreCode2Minor"].values()
    table["소분류(Genre)"]=classJsons["genreCode2Name"].values()
    table["분류코드"]=classJsons["genreCode2Name"].keys()
        
    # 행(장르), 열(악기)별로 total 값 구하기
    inst_wise_total = table.drop(["대분류","중분류","소분류(Genre)","분류코드"],axis=1).sum(axis=0, skipna=True)
    table.loc['total'] = inst_wise_total
    genre_wise_total = table.drop(["대분류","중분류","소분류(Genre)","분류코드"],axis=1).sum(axis=1, skipna=True).astype('int16')
    table['total'] = genre_wise_total

    TOTAL = genre_wise_total["total"]  # 전체 total

    # 행, 열별로 백분위 % ratio(%) 구하기
    print(TOTAL)
    inst_wise_ratio = inst_wise_total/TOTAL*100
    inst_wise_ratio =inst_wise_ratio.astype(float).round(decimals=2)
    table.loc['ratio(%)'] = inst_wise_ratio
    genre_wise_ratio = genre_wise_total[:-1]/TOTAL*100
    genre_wise_ratio = genre_wise_ratio.astype(float).round(decimals=2)
    table['ratio(%)'] = genre_wise_ratio

    # 열 옮기기
    for c in ["분류코드","소분류(Genre)","중분류","대분류"]:
        table.insert(0,c,table.pop(c))

    table=table.set_index(["대분류","중분류","소분류(Genre)"])

    ################################################################################
    # define util functions
    def __map_minor2major(
        df: pd.DataFrame,
        minor_col: str,
        major_col: str,
        m2M_json: dict,
    ) -> pd.DataFrame:
        for i, minorClass in enumerate(df[minor_col]):
            MajorCode = m2M_json[minorClass]
            df[major_col][i] = MajorCode
        return df

    ################################################################################
    # 악기별 통계 테이블 만들기
    inst_stat = pd.DataFrame(columns=["대분류", "count(대분류)", "ratio(%)(대분류)", "중분류",
                             "count(중분류)", "ratio(%)(중분류)", "악기", "소분류_코드", "count", "ratio(%)"], index=inst_cd)
    # M stands for Major class of instrument
    # m stands for minor class of instrument
    inst_stat["악기"] = inst_nm
    inst_stat["소분류_코드"] = inst_cd
    inst_stat["count"] = inst_wise_total.values
    inst_stat["ratio(%)"] = inst_wise_ratio.values

    inst_stat = __map_minor2major(inst_stat, "소분류_코드", "중분류", classJsons["instCode2Minor"])
    indices = [0, 3, 5, 9, 12, 21, 24, 27]
    for i in range(len(indices)-1):
        inst_stat["count(중분류)"][indices[i]:indices[i+1]] = inst_stat["count"][indices[i]:indices[i+1]].sum()
    inst_stat["ratio(%)(중분류)"] = (inst_stat["count(중분류)"]/TOTAL*100).astype(float).round(decimals=2)

    inst_stat = __map_minor2major(inst_stat, "소분류_코드", "대분류", classJsons["instCode2Major"])
    indices = [0, 5, 12, 24, 27]
    for i in range(len(indices)-1):
        inst_stat["count(대분류)"][indices[i]:indices[i+1]] = inst_stat["count"][indices[i]:indices[i+1]].sum()
    inst_stat["ratio(%)(대분류)"] = (inst_stat["count(대분류)"]/TOTAL*100).astype(float).round(decimals=2)

    inst_stat = inst_stat.set_index(["대분류", "count(대분류)", "ratio(%)(대분류)", "중분류", "count(중분류)", "ratio(%)(중분류)", "악기"])

    ################################################################################
    # 장르별 통계 테이블 만들기
    genre_stat = pd.DataFrame(columns=["대분류", "count(대분류)", "ratio(%)(대분류)", "중분류", "count(중분류)", "ratio(%)(중분류)", "소분류", "Code", "count", "ratio(%)"], index=genre_cd)
    genre_stat["Code"] = genre_cd
    genre_stat["소분류"] = genre_nm
    genre_stat["count"] = genre_wise_total
    genre_stat["ratio(%)"] = genre_wise_ratio

    genre_stat = __map_minor2major(genre_stat, "Code", "중분류", classJsons["genreCode2Minor"])
    indices = [0, 11, 19, 33, 35, 38]
    for i in range(len(indices)-1):
        genre_stat["count(중분류)"][indices[i]:indices[i+1]] = genre_stat["count"][indices[i]:indices[i+1]].sum()
    genre_stat["ratio(%)(중분류)"] = (genre_stat["count(중분류)"]/TOTAL*100).astype(float).round(decimals=2)

    genre_stat = __map_minor2major(genre_stat, "Code", "대분류", classJsons["genreCode2Major"])
    indices = [0, 33, 38]
    for i in range(len(indices)-1):
        genre_stat["count(대분류)"][indices[i]:indices[i+1]] = genre_stat["count"][indices[i]:indices[i+1]].sum()
    genre_stat["ratio(%)(대분류)"] = (genre_stat["count(대분류)"]/TOTAL*100).astype(float).round(decimals=2)

    genre_stat = genre_stat.set_index(["대분류", "count(대분류)","ratio(%)(대분류)", "중분류", "count(중분류)", "ratio(%)(중분류)", "소분류"])
    ###################################################################################
    # save
    if excel_path:
        writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
        inst_stat.to_excel(writer, sheet_name="악기분포집계")
        genre_stat.to_excel(writer, sheet_name="장르분포집계")
        table.to_excel(writer, sheet_name="장르악기분포집계")
        writer.save()


if __name__ == "__main__":
    import os
    from pathlib import Path
    config = arg_parser()

    update_table(config)