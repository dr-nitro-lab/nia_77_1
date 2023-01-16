# 자동채보 모델과 사용법 가이드

- 음악을 필사 해주는, “Omniscient Mozart”, Omnizart라는 모델을 이용하여 학습 진행.
- 학습은 악기 별로 (String, Wind, Vocal) 나누어서 진행.
- 각 파일별로 feature를 뽑고, 그 feature에 대해서 학습.
- 각 wav 파일별로 feature를 추출해서 ‘.hdf’ 파일로 저장.
	Feature의 구성요소:
	1. Multiplication of spectrum and cepstrum
	2. Spectrum of the audio.
	3. Generalized Cepstrum of Spectrum (GCoS)
	4. Cepstrum of the audio
	5. Central frequencies to each feature
-  그 이후에 mid 파일에서 label(정답 음계) 을 추출함. ‘.pickle’ 파일로 저장.
-  omnizart에서 제공된 piano transcription 모델 (music_piano-v2) 에 각각의 분류별 데이터를 추가 학습시켜 fine-tuning함.

------
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
