# 자동채보 모델과 사용법 가이드

------
## Repository
- link (추후 추가)
-------
## Algorithm
- Algorithm & Model : Omnizart
- Reference Paper: https://arxiv.org/abs/2106.00497

------
## 사용법 가이드
### 1. docker image 설치
```
>> docker load -I gugak_docker.tar
>> docker run -itd —gpus all -p 8888:8888 -v ~/gugak:/mnt –name gugak 78d56d9b5731 /bin/bash
```

### 2.   model 및 dataset 설치
- -	~/gugak 폴더에 동봉된 checkpoints 및 dataset 압축 풀기

### 3. test
####	`GUGAK/omnizart`에서 `inference.py`파일 실행
```
~/gugak/omnizart>> nohup python inference.py > inference.out &
```