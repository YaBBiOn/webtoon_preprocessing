# Webtoon Preprocessing
웹툰 이미지를 자동으로 컷별로 자릅니다.

## 작동 환경
- python 3.9
- 기타 라이브러리 : numpy, Pillow
```
pip install -r requirements.txt
```

## 작동 방법
- 아래의 코드를 터미널에 입력합니다.
```
python webtoon_preprocessing.py
```
- 컷할 이미지의 경로를 입력합니다. 
    - 이미지의 세로 크기가 가급적 3만 pixel을 넘지 않게 조정해주세요.
    - 이미지 크기가 일정 이상을 초과할 경우, 에러가 발생할 수 있습니다.
- 잠시만 기다리면 웹툰 이미지를 컷별로 잘라놓은 폴더가 생성되어이 있습니다.

## 유의사항
- 너무 작은 이미지도 분할되어 나올 경우, min_panel_h 파라미터를 조정하세요. (기본값은 200입니다.)

## 활용
해당 코드는 KinderGuardtoon(23년도 고려대학교 인공지능 SW 아카데미에서 진행한 프로젝트 CV 프로젝트)에서 활용되었습니다. 