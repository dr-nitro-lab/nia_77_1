import os
import glob
from pathlib import Path
from argparse import ArgumentParser
import pandas as pd
from json_utils import (
    compare_keys_recursively,
    loadjson
)


def parse_arg():
    parser = ArgumentParser("1. 같은 이름의 세가지 파일 [.wav, .json., .mid]이 한 세트를 이루고 있는지 확인.\n"
                            "2. metadata 형식에 어긋나는 json파일 검출")
    parser.add_argument("--dataset", '-d', type=str,
                        default='220924')
    parser.add_argument("--excel", '-e', type=str,
                        default='220924.error.xlsx')
    args = parser.parse_args()
    return args


NOT_ESSENTIAL_KEYS = {
    # "uuid", "index",
    # "annotation_name", "annotation_parent",
    # "annotation_ID",
    # "annotation_category",
    # "start_time",
    # "end_time",
    # "annotation_code"
}


def check_missing_files(dataset_path):
    
    wav_files = list(dataset_path.glob("*.wav"))
    json_files = list(dataset_path.glob("*.json"))
    mid_files = list(dataset_path.glob("*.mid"))

    # extension과 directory를 제외한 파일의 basename의 리스트로 변환
    for i, wav in enumerate(wav_files):
        wav_files[i] = wav.stem
    for i, json in enumerate(json_files):
        json_files[i] = json.stem
    for i, mid in enumerate(mid_files):
        mid_files[i] = mid.stem

    # union
    wav_set, json_set, mid_set = set(
        wav_files), set(json_files), set(mid_files)
    union = wav_set.union(json_set).union(mid_set)

    # difference
    wav_missing = union - wav_set
    json_missing = union - json_set
    mid_missing = union - mid_set

    print(f"length of union: {len(union)}")
    print(f"length of wav_missing: {len(wav_missing)}")
    print(f"length of json_missing: {len(json_missing)}")
    print(f"length of mid_missing: {len(mid_missing)}")

    return pd.DataFrame({
        "wav": pd.Series(sorted(list(wav_missing))),
        "json": pd.Series(sorted(list(json_missing))),
        "mid": pd.Series(sorted(list(mid_missing)))
    })


def check_error_jsons(dataset_path, std_json_path):
    std_json = loadjson(std_json_path)
    json_files = list(dataset_path.glob("*.json"))
    error_json_files = []
    for json_file in json_files:
        cmp_json = loadjson(json_file)
        if not compare_keys_recursively(std_json,cmp_json,NOT_ESSENTIAL_KEYS):
            error_json_files.append(cmp_json)
    return pd.DataFrame(error_json_files,columns=["에러파일목록"])


if __name__ == "__main__":
    args = parse_arg()


    missing_table = check_missing_files(Path(args.dataset))

    error_table = check_error_jsons(Path(args.dataset), std_json_path="220924/AP_C01_00001.json")

    writer = pd.ExcelWriter(args.excel)
    missing_table.to_excel(writer, sheet_name="누락파일목록")
    error_table.to_excel(writer, sheet_name="에러json파일목록")
    writer.save()
