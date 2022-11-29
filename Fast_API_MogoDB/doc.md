# DB연결

# 1. 시크릿 변수 설정

# 2. odmantic을 사용하여 fastapi와 여결

# 3. models 디렉토리를 사용하여 추상화

# 4. book 모델 개발

# 5. db에 insert

# 배포

lightsall로 들어가서 인스턴스를 만든다. -> linux 와 ubuntu(20.04)

# 배포 준비

uvicorn host 0.0.0.0으로 변경, reload=False, port=80
main.py jinja2에서 파일 경로 str 타입으로 변경
requirements.txt 패키지 체크 (aiohttp 누락되어 있는거 추가)
github에 코드 올리기

# 개인 git에 있는 토큰 발급

토큰 복사 해두기
VPS : 가상 사설 서버 구축

# git에다가 저장하기

git init
git add .
git commit -m "저장할 이름"
git branch -M main
git remote git개인 주소
git pull origin main
git push origin main

# AWS Lightsail 사용

# 인스턴스 생성

# ssh를 사용하여 연결 (브라우저에서 접속)

sudo apt-get update
sudo apt-get -y upgrade

메시지가 뜨면 enter눌러서 넘긴다.

sudo apt-get install build-essential
sudo apt-get install curl git vim python3 python3-pip
touch .gitconfig
git config --global user.name amamov
git config --global user.email amamov@kakao.com
git config --global --list
git clone <프로젝트>
cd <프로젝트>
vi secrets.json
sudo pip install -r requirements.txt
sudo python3 server.py
ip 접속
배포 성공!!
