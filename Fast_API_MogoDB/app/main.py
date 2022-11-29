from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path

from app.models import mongodb
from app.models.book import BookModel
from app.book_scraper import NaverbookScraper


# 절대 경로 지정 현재 파일의 경로이며, parent는 부모(app)
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

Templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# 
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    #book = BookModel(keyword="파이썬", pulicher="BJpulicher", price=1200, image="me.png")
    #await mongodb.engine.save(book) # DB에 저장 된다.
    return Templates.TemplateResponse("./index.html", {"request": request, "title": "콜렉터 북북이"})

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q:str):
    # 1. 쿼리에서 검색어 추출
    # print(q)
    # 쿼리는 q이다.
    keyword = q
    # (예외처리)
    if not keyword:
        context = {"request": request, "title": "콜렉터 북북이"}
    
    # 해당 모델에서 keyword가 같은 경우 keyword와 같은 모델을 가져온다.
    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        context = {"request": request, "keyword": "kwyword", "books": books}
        return Templates.TemplateResponse("index.html", context=context)
    # 검색어가 없다면 사용자에게 검색을 요구 return
    # 해당 검색어에 대해 수집된 데이터가 이미 DB에 존재한다면 해당 데이터를 사용자에게 보여준다.
    # 2. 데이터 수집기(book_scraper)를 해당 검색어에 대해 데이터를 수집한다. -> Search라니 메소드를 사용해서 수집
    naver_book_scaper = NaverbookScraper()
    books = await naver_book_scaper.search(keyword, 10)
    book_models = [] # books는 리스형식이다
    for book in books:
        book_models = BookModel(
            keyword= keyword,
            pulicher= book["piblisher"],
            price=book["price"],
            image=book["image"]            
        )

    # 3. DB에 수집된 데이터를 저장한다.
    # asyncio.gather를 대신해서 하는 메서드는 save_all
    await mongodb.engine.save_all(book_models)
    # 수집된 각각의 데이터에 대해서 DB에 들어갈 모델 인스턴스를 찍는다.
    # 가가 모델 인스턴스를 DB에 저장한다.
    return Templates.TemplateResponse("./index.html", {"request": request, "title": "콜렉터 북북이", "books":books})


@app.on_event("startup")
def on_app_start():
    pass
    '''before app starts'''
    # await momgodb.connect()
    mongodb.connect()
    

@app.on_event("shutdown")
async def on_app_shotdown():
    '''after app shutdown'''
    # await momgodb.close()
    mongodb.close()
    
