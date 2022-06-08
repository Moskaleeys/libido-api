
## 설치방법
### Install Python
+ Python 및 PIP 설치 (공식사이트 : https://www.python.org/downloads/)
    + Mac
        + 파이썬3 설치 시 pip3 자동설치
    + Windows
        + 파이썬 설치 후 환경변수 설정
        + 제어판 -> 시스템 -> 고급 시스템 설정 -> 환경변수 path에 설치 폴더 추가
        + 설치폴더는 사용자마다 서로 다름 
          - 기본설치폴더 : C:\Users\{사용자명}\AppData\Local\Programs\Python\Python310\Scripts
          - 기본설치폴더 : C:\Users\{사용자명}\AppData\Local\Programs\Python\Python310
        ![image](https://user-images.githubusercontent.com/105629261/172600583-67b039f4-3733-45f7-9b2b-e1a76e295254.png)


+ 설치 후 python3 및 pip3 버전 확인
```bash
$ python3 --version
$ pip3 --version
```

### Git Clone
```bash
$ git clone https://github.com/moskalabs/libido-api.git
```

## Local 환경설정 또는 Docker 둘 중 한 방법 사용하여 설정
### Local 환경설정
1. 원하는 폴더명에 가상환경 설치
    ```bash
    $ cd {개별경로}/libido-api/
    $ python3 -m venv {폴더명}
    ```
2. 생성된 가상환경 실행
    ```bash
    $ soucre ./{폴더명}/bin/activate
    ```
3. requirements/requirements.txt 있는 폴더로 이동 후 패키지 설치 => 의존성 패키지는 패키지 추가 될 때마다 추가할 필요가 있음
    ```bash
    $ cd {개별경로}/libido-api/requirements/
    $ pip3 install -r requirements.txt
    ```
    참고) 패키지 추가 후 requirements.txt 재생성
    ```bash
    $ pip3 freeze > requirements.txt
    ```
4. 서버실행
    + 테스트버전 실행
    ```bash
    $ cd {개별경로}/libido-api/libido_api/
    $ python3 manage.py runserver 8888 --settings=libido_api.settings.development
    ```   
    <br>
### 의존성 패키지 설치 시 오류 날 경우
+ Mac
    + homebrew 설치 (공식 사이트 : https://brew.sh/index_ko )
    + mysqlclient 설치 오류 시 mac에서 mysql 설치 후 의존성 패키지 재설치
    ```bash
    $ brew install mysql
    ```
    + mysql 설치 후 Local 환경설정 -> 의존성패키지 설치부터 다시 실행

 <br><br>
### Docker 환경설정
1. Install Docker (공식 사이트 : https://www.docker.com/get-started/)
2. Install Docker Compose (공식 사이트 : https://docs.docker.com/compose/install/)
3. Docker-comppose 실행
    ```bash
    $ cd {docker-compose.yml 존재하는 폴더로 이동}
    ```
   + 테스트버전 실행
    ```bash
    $ docker-compose --env-file .env.dev up -d --build 
    ```
   + 실버전 실행
    ```bash
    $ docker-compose --env-file .env.prd up -d --build
    ```
