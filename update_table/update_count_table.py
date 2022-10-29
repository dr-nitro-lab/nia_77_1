from argparse import ArgumentParser
from datetime import datetime
from typing import Dict, Optional

import pandas as pd
import numpy as np

from json_utils import json2list

from pathlib import Path
import os
import cfg


def update_table():
    """
    inputs
    --------------
    json_list :     "파일명":{json객체} 쌍으로 저장된 dictionary
    classJsons :      classJson 폴더의 json파일들을 모두 load한 dict를 입력한다. 각 파일들의 내용은 파일명으로 접근할 수 있다.
    excel_path :    if not None, excel_path에 excel 파일 저장
    """

    metadatas = json2list(cfg.DATASET_DIR)
    classJsons = json2list(cfg.CONFIG_JSONS)
    excel_path = os.path.join(cfg.DATASET_DIR, Path(cfg.DATASET_DIR).name + '.count.xlsx')

    # load JSONs
    genre_cd = classJsons["genreCode2Name"].keys()
    genre_nm = classJsons["genreCode2Name"].values()

    inst_cd = classJsons["instCode2Name"].keys()
    inst_nm = classJsons["instCode2Name"].values()

    beat_cd = classJsons["beatCode2Name"].keys()
    beat_nm = classJsons["beatCode2Name"].values()

    mode_cd = classJsons["modeCode2Name"].keys()
    mode_nm = classJsons["modeCode2Name"].values()

    # define main DataFrame
    # col이 악기 코드, row가 장르 코드인 DataFrame 생성
    total_table = pd.DataFrame(columns=inst_cd, index=genre_cd)
    beat_stat = pd.DataFrame(0,columns=["소분류", "Code", "count", "ratio(%)"], index=beat_cd)
    mode_stat = pd.DataFrame(0,columns=["대분류", "count(대분류)", "ratio(%)(대분류)", "소분류", "Code", "count", "ratio(%)"], index=mode_cd)
    mode_stat["대분류"] = classJsons["modeCode2Major"].values()


    ###########################################################################################
    # Construct main table and calculate main statistics
    for json_filename, json_dict in metadatas.items():
        try:
            genre = json_dict["music_type_info"]["music_genre_cd"]
            inst = json_dict["music_type_info"]["instrument_cd"]
            main_inst = json_dict["music_type_info"]["main_instrmt_cd"]
            beat = json_dict["annotation_data_info"]["gukak_beat_cd"]
            mode = json_dict["annotation_data_info"]["mode_cd"]

        except KeyError:
            print(f"{json_filename}의 키는 다른 json파일들의 key들과 다르다.")
            continue  # do something when wrong key detected!!

        # 현재는 "instrument_cd" 또는 "main_instrmt_cd" 둘 중 하나만 채워져 있음을 반영
        if inst != "":
            if pd.isnull(total_table.loc[genre, inst]):
                total_table[inst][genre] = 1
            else:
                total_table[inst][genre] += 1
        elif main_inst != "":
            if pd.isnull(total_table.loc[genre, main_inst]):
                total_table[main_inst][genre] = 1
            else:
                total_table[main_inst][genre] += 1
        
        try:
            beat_stat["count"][beat]+=1
        except KeyError as k:
            print(f"KeyError has occured because '{json_filename}' has beat key {k}")
        try:
            mode_stat["count"][mode]+=1
        except KeyError as k:
            print(f"KeyError has occured because '{json_filename}' has mode key {k}")


    # Column Multi Index 생성
    idx=[]
    for M,m,n,c in zip(classJsons["instCode2Major"].values(),\
        classJsons["instCode2Minor"].values(),\
            classJsons["instCode2Name"].values(),\
                classJsons["instCode2Name"].keys()):
        idx.append((M,m,n,c))

    total_table.columns = pd.MultiIndex.from_tuples(idx, names=["대분류","중분류","악기","소분류_코드"])

    # Row Multi Index 생성
    total_table["대분류"]=classJsons["genreCode2Major"].values()
    total_table["중분류"]=classJsons["genreCode2Minor"].values()
    total_table["소분류(Genre)"]=classJsons["genreCode2Name"].values()
    total_table["분류코드"]=classJsons["genreCode2Name"].keys()
        
    # 행(장르), 열(악기)별로 total 값 구하기
    inst_wise_total = total_table.drop(["대분류","중분류","소분류(Genre)","분류코드"],axis=1).sum(axis=0, skipna=True)
    total_table.loc['total'] = inst_wise_total
    genre_wise_total = total_table.drop(["대분류","중분류","소분류(Genre)","분류코드"],axis=1).sum(axis=1, skipna=True).astype('int16')
    total_table['total'] = genre_wise_total

    TOTAL = genre_wise_total["total"]  # 전체 total

    # 행, 열별로 백분위 % ratio(%) 구하기
    print(TOTAL)
    inst_wise_ratio = inst_wise_total/TOTAL*100
    inst_wise_ratio =inst_wise_ratio.astype(float).round(decimals=2)
    total_table.loc['ratio(%)'] = inst_wise_ratio
    genre_wise_ratio = genre_wise_total[:-1]/TOTAL*100
    genre_wise_ratio = genre_wise_ratio.astype(float).round(decimals=2)
    total_table['ratio(%)'] = genre_wise_ratio

    # 열 옮기기
    for c in ["분류코드","소분류(Genre)","중분류","대분류"]:
        total_table.insert(0,c,total_table.pop(c))

    total_table=total_table.set_index(["대분류","중분류","소분류(Genre)"])

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
    ################################################################################
    # 장단별 통계 테이블 만들기
    beat_stat["Code"] = beat_cd
    beat_stat["소분류"] = beat_nm
    beat_stat["ratio(%)"] = (beat_stat["count"]/sum(beat_stat["count"])*100).astype(float).round(decimals=2)

    beat_stat = beat_stat.set_index(["소분류", "Code"])
    ################################################################################
    # 음조직별 통계 테이블 만들기
    # mode_stat = pd.DataFrame(columns=["대분류", "count(대분류)", "ratio(%)(대분류)", "소분류", "Code", "count", "ratio(%)"], index=mode_cd)
    mode_stat["Code"] = mode_cd
    mode_stat["소분류"] = mode_nm
    mode_stat["ratio(%)"] = (mode_stat["count"]/sum(mode_stat["count"])*100).astype(float).round(decimals=2)

    mode_stat = __map_minor2major(mode_stat, "Code", "대분류", classJsons["modeCode2Major"])
    indices = [0, 9, 20]
    for i in range(len(indices)-1):
        mode_stat["count(대분류)"][indices[i]:indices[i+1]] = mode_stat["count"][indices[i]:indices[i+1]].sum()
    mode_stat["ratio(%)(대분류)"] = (mode_stat["count(대분류)"]/TOTAL*100).astype(float).round(decimals=2)

    mode_stat = mode_stat.set_index(["대분류", "count(대분류)", "ratio(%)(대분류)", "소분류"])
    ###################################################################################
    # save
    if excel_path:
        writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
        total_table.to_excel(writer, sheet_name="장르악기분포집계")
        inst_stat.to_excel(writer, sheet_name="악기분포집계")
        genre_stat.to_excel(writer, sheet_name="장르분포집계")
        beat_stat.to_excel(writer, sheet_name="장단분포집계")
        mode_stat.to_excel(writer, sheet_name="음조직분포집계")
        writer.save()


if __name__ == "__main__":
    update_table()