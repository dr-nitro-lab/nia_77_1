# nia_77_1

## 데이터 무결성 확인방법
#### 1. `cfg.py` 의 변수들을 설정한다. 
- `DATASET_DIR` : 데이터셋이 있는 폴더의 경로를 `DATASET_DIR`에 입력
- `CONFIG_JSONS` : 각 장르와 악기에 대한 코드와 분류를 서로 mapping한 json 파일을 모아둔 폴더. 이 repository를 clone 하여 그대로 사용한다면 바꾸지 않아도 된다.
- `STD_JSON` : key값이 다른 json들과 다르지 않으면서, 최대한 모든 key를 포함하는 json 파일을 선정한다. 여기서는 `single_tonguing_cd`, `tempo`, `lyrics` 모두에 대해 annotation을 가지는 AP_C11_01566.json을 선정했다.
```python
# dataset이 있는 directory의 경로
DATASET_DIR = "./221011"

# 분야, 악기 관련 코드에 대한 json파일들이 있는 directory의 경로
CONFIG_JSONS = "./classJson"

# json 파일의 무결성을 체크할때 비교기준으로 사용할 파일
STD_JSON = os.path.join(DATASET_DIR, "AP_C11_01566.json")
```

#### 2. check_integrity.ipynb의 셀들을 순차적으로 실행시킨다.

## error, count, time 테이블 생성방법
#### 1. 위와 같은 방식으로 `cfg.py` 의 변수들을 설정한다.

#### 2. error, count, time 테이블을 생성하기 위해 
- Windows에서 실행할 경우 update_table.bat을 실행시킨다.
- Linux 또는 git bash 에서 실행할 경우에는 update_table.sh를 실행시킨다.
