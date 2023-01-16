# 장르분류(Music Genre Classification) 모델과 사용법 가이드


--------
## Github repository
- https://github.com/pratikshaya/genre_221216_docker_project

-------
## Algorithm
- Reference Paper
  - https://arxiv.org/pdf/1703.09179.pdf

-----

## 사용법 가이드

### docker image 설치
```
>> sudo docker load < genre_classification_deploy.mine.tar
>> sudo docker run -it —shm-size 4G -gpus all genre_classification_deploy /bin/bash
```

### 코드 실행

#### a.	augmentaion.py
- i.	증강(augmentation)하는 동안 입력 폴더 경로 할당.  예: “./dataset/Fusion_gugak_S/”
- ii.	메인함수 내에 데이터 증강 파라메터 N 설정.  예: N = 2 이면 원래 audio 파일 샘플들 마다 2개의 증강된 데이터 생성
- iii.	증강된 오디오 데이터 출력을 입력 폴더 경로와 동일한 장소에 저장. 예: “./dataset/Fusion_gugak_S/”


#### b.	prepare_datasets.py
- i.	할당: PATH_DATASETS = “./genre_221216_docker_project/dataset/”
- ii.	할당: FOLDER_CSV = “./genre_221216_docker_project/data_csv/”
- iii.	할당: folder_dataset_gtg = “./genre_221216_docker_project/dataset/”
- iv.	prepare_datasets.py 을 실행하면 오디오 경로와 라벨을 담은 .CSV 파일을 생성.


#### c.	cross_validation_clean.py
- i.	사전 학습된 가중치(weights) 경로 할당: “./genre_221216_docker_project/model_best.hdf5”
- ii.	데이터 셋 경로 할당: “./genre_221216_docker_project/dataset/”
- iii.	.CSV 파일 경로 할당: “./genre_221216_docker_project/data_csv/genre_221216.csv”
- iv.	 cross_validation_clean.py 코드는 다음 작업을 수행:
    -	데이터 셋을 5개 폴드로 분할
    -	매 폴드 반복에서 테스트 폴드에 대한 정확도 계산
    -	매 폴드 혼동 행렬 가시화
    -	전체 5개의 폴드에 대한 평균 정확도와 통합 혼동 행렬 생성