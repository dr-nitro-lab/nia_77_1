import json
from pathlib import Path
from typing import Dict, Set, List, Any, Tuple, Union
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
    not_essential_keys: Set
) -> bool:
    for key, val in src_json.items():
        # print(key,end='')
        if isinstance(val, Dict):
            try:
                if not compare_keys_recursively(val, dst_json[key], not_essential_keys):
                    return False
            except KeyError as e:
                print(e)
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


def swapKeyVal(src_path: str, dst_path: Union[str,None] = None):
    json_obj: dict = loadjson(src_path)
    new_json = {val: key for key, val in json_obj.items()}
    if dst_path:
        writejson(dst_path, new_json)
    else:
        writejson(src_path, new_json)
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

def get_jsons_containing_key(dir, *keys):
    """
    dir 폴더 내의 json파일중 key들로 접근했을때 해당하는 필드가 value를 가지고 있는 json의 목록을 반환한다.
    ex) ["annotation_data_info"]["lyrics"] 로 접근했을 때 값이 있는 json 파일명들을 반환한다는 것.
    """
    jsons = json2list(dir)
    json_has_key = list()
    for name, j in jsons.items():
        for k in keys:
            j = j[k]
        if not isinstance(j, dict) and not isinstance(j, list) and not isinstance(j,tuple):
            raise TypeError
        if len(j)>0:
            json_has_key.append(name)
            # print(name)
    return json_has_key

def getValuesInList(keys:List,path:str)->List:
    json_list = json2list(path)
    val_list = []
    for json_obj in json_list.values():
        try:
            for key in keys:
                json_obj = json_obj[key]
            val_list.append(json_obj)
        except KeyError as k:
            try:
                print(f"{k}, \nkey {key} doesn't exist in {json_obj['music_source_info']['music_src_nm']}")
            except Exception as e:
                print(e)
    return val_list

if __name__ == "__main__":
    swapKeyVal("classJson/modeCode2Major.json")