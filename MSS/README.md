# 소스분리(Music Source Separation) 모델과 사용법 가이드

-------

## Github repository
- https://github.com/pratikshaya/MSS_221118_project

-------
## Algorithm
- Reference Paper 
  - https://ieeexplore.ieee.org/document/9257356

-------

## 사용법 가이드
### docker image 설치
```
>> sudo docker load < source_separation_deploy.mine.tar
>> sudo docker run -it —shm-size 4G -gpus all source_separation_deploy /bin/bash
```

### 코드 실행

#### 1)	config.py
-	학습 중 데이터 경로의 설정:
“./MSS_221118_dataset/training_data_order”
-	테스트 중 데이터 경로의 설정: 
“./MSS_221118_dataset/test_data_order”
-	스팩트로그램 생성을 위한 샘플링 래이트 samplingrate (SR), 프래임 길이 frame length (L_FRAME)와 홉 길이 hop length (L_HOP)는  ModelConfig class 에서 변경가능

#### 2) training.py
-	train_MSS_221118.py를 실행 (모델 학습이 실행되는 동안, config.py 파일에 테스트를 위한 데이터 경로를 코멘트 처리하여 비활성화)
-	이 프로그램 수행은 프로젝트의 checkpoint 폴더에 checkpoints를 저장 

#### 3) Eval_MSS_221118.py
-	eval_MSS_221118.py를 실행 (evaluation이 진행되는 동안 config.py 파일에 학습을 위한 데이터 경로를 코멘트 처리하여 비활성화) 
-	평가(evaluation) 코드는 다음 작업을 수행함
    - 노래와 장구의 참값(ground truth) 스팩트로그램의 가시화 
    - 노래와 장구의 혼합된 소스의 스팩트로그램 가시화
    - 예측된 노래와 장구 소리의 스팩트로그램 가시화
    - 각 테스트 샘플의 SDR 계산 
    - 각 테스트 샘플 SDR로부터 median SDR 계산