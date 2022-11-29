import uvicorn

if __name__ == "__main__":
    uvicorn.run('app.main:app', host="localhost", port=8000, reload=True) # reload=True 실제는 서버 환경에서는 작성하지 않는다.
    # uvicorn.run('app.main:app', host="0.0.0.0", port=80, reload=False) # 서버용으로 사용하기