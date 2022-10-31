import os


# dataset이 있는 directory의 경로
DATASET_DIR = "./221011"

# 분야, 악기 관련 코드에 대한 json파일들이 있는 directory의 경로
CONFIG_JSONS = "./classJson"

# json 파일의 무결성을 체크할때 비교기준으로 사용할 파일
STD_JSON = os.path.join(DATASET_DIR, "AP_C11_01566.json")

# json과 wav, midi 비교 기준
DURATION_TOLERANCE = 1 # wav 파일의 실제길이와 json 에 기록된 음원길이 사이의 허용되는 차이
BPM_TOLERANCE = 0.1