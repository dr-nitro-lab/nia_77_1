import json
from pathlib import Path
from typing import Dict, Set, List, Any, Tuple
import os



def print_json(json_dict): return print(
    json.dumps(json_dict, indent=4, ensure_ascii=False))


def get_keys_recursively(json_dict: dict) -> Set:
    fields = list()

    for key, val in json_dict.items():
        if isinstance(val, dict):
            fields.extend(get_keys_recursively(val))

        elif isinstance(val, list):
            for dict_obj in val:
                fields.extend(get_keys_recursively(dict_obj))

        fields.append(key)

    return set(fields)


def compare_keys_recursively(
    src_json: Dict,
    dst_json: Dict,
    not_essential_keys: Set,
    i : int =0
) -> bool:
    for key, val in src_json.items():
        # print(key)
        if isinstance(val, Dict):
            try:
                if not compare_keys_recursively(val, dst_json[key], not_essential_keys):
                    return False
            except KeyError:
                print(f'비교대상인 json 파일에 "{key}"라는 key는 존재하지 않는다.')
                return False
        elif isinstance(val, List) or isinstance(val, Tuple):
            for dict_obj in val:
                if not compare_keys_recursively(val[0], dict_obj, not_essential_keys):
                    return False
            for dict_obj in dst_json[key]:
                if not compare_keys_recursively(val[0], dict_obj, not_essential_keys):
                    return False
        # else:
        #     raise ValueError(
        #         f"Input object is neither Dict nor List. Check type of object!! \n {val}")

    src_json_keys = set(src_json.keys())-set(not_essential_keys)
    dst_json_keys = set(dst_json.keys())-set(not_essential_keys)

    return src_json_keys == dst_json_keys


def loadjson(path) -> Dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def writejson(path, json_dict: dict) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=4)


def json2list(path) -> Dict[str, Dict]:
    json_paths = list(Path(path).glob("*.json"))
    json_list_dict = dict()
    for json_path in json_paths:
        data = loadjson(json_path)
        json_list_dict[json_path.stem] = data
    return json_list_dict


def swapKeyVal(src_path: str, dst_path: str):
    json_obj: dict = loadjson(src_path)
    new_json = {val: key for key, val in json_obj.items()}
    if dst_path:
        writejson(dst_path, new_json)
    return new_json


def parse_prefix_of_key(
    src_json: Dict,
    prefix_len: int = 1
) -> Dict:
    for k in src_json.keys():
        src_json[k] = k[:prefix_len]
    return src_json


def getVal(inp: Any, json_path: Dict):
    jsondict = loadjson(json_path)
    for i, inp_val in enumerate(inp):
        inp[i] = jsondict[inp_val]
    return inp


if __name__ == "__main__":
    # STD_JSON = "C:/Users/KSW/Desktop/Projects/학부연구생/220924/AP_C01_00001.json"
    # JSON_DIR = "C:/Users/KSW/Desktop/Projects/학부연구생/220924"

    # NOT_ESSENTIAL_KEYS = {
    #     "uuid", "index",
    #     "annotation_name", "annotation_parent",
    #     # "annotation_ID",
    #     # "annotation_category",
    #     # "start_time",
    #     # "end_time",
    #     # "annotation_code"
    # }

    # std_json_path = Path(STD_JSON)
    # std_json = loadjson(std_json_path)


    # # for json_filename, json_dict in json2list(JSON_DIR).items():
    # #     if not compare_keys_recursively(src_json=std_json, dst_json=json_dict,not_essential_keys=NOT_ESSENTIAL_KEYS):
    # #         print(json_filename)

    # CMP_JSON = "C:/Users/KSW/Desktop/Projects/학부연구생/220924/AP_E04_00107.json"
    # cmp_json_path = Path(CMP_JSON)
    # cmp_json = loadjson(cmp_json_path)
    # print(compare_keys_recursively(std_json, cmp_json, NOT_ESSENTIAL_KEYS))
    lst = json2list("classJson")
    print(lst)