# 2018-Spring

---

## Population and Economy / 인구와 경제
    1. kostat_data_trimming.py : 통계청 지역별 고용조사 데이터를 지역 패널 데이터로 다듬는 일련의 과정 포함
    2. kostat_data_trimming2.py : 통계청 지역별 고용조사 데이터 중 평균 교육 연한을 도출하는 코드
        - 데이터 파일이 약간 상이하여 별도 관리
    3. kostat_data_trimming3.py : 교수님 코멘트를 반영한 데이터를 추출하기 위한 코드
    4. kostat_data_trimmed folder : 위의 코드를 사용하여 전처리된 데이터 csv, dta 파일
    5. make_panel.py : 여러 자료를 합쳐 패널 데이터로 만드는 코드
    * 2018-1_인구와 경제_팀프로젝트_6조.pdf : 위 자료를 사용하여 분석 및 작성한 소논문

## Introduction to Numerical Method / 수치계산법 개론
    1. dogleg.m : 다변수 함수의 optimization을 위한 doglog algorithm을 담은 MATLAB 코드
    2. dogleg_results : 위의 두 코드를 실행했을 때 출력된 결과
    3. MSP~.gif : dogleg.m에서 사용된 함수들의 surface를 시각화한 

## Applied Econometrics / 응용 계량경제학
    1. klips_trimming.py : 연도별 KLIPS 데이터를 패널 데이터로 다듬는 일련의 코드
