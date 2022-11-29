import aiohttp
import asyncio
from app.config import get_secret

class NaverbookScraper:
    
    NAVER_API_BOOK = "https://openapi.naver.com/v1/search/book"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SERET")
    
    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["items"]
    
    def unit_url(self, keyword, start):
        return {
            "url" : f"{self.NAVER_API_BOOK}?query={keyword}&display=10&start={start}",
            "headers" : {
                "X-Naver-Client-Id" : self.NAVER_API_ID,
                "X-Naver-Client-Secret" : self.NAVER_API_SECRET,
                },
        }
    
    async def search(self, keyword, total_page):
        apis = [self.unit_url(keyword, 1 + i * 10) for i in range(total_page)]
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[NaverbookScraper.fetch(session, apis["url"], apis["headers"]) for aou in apis]
            )
            # print(all_data)
            result = []
            for data in all_data:
                if data is not None:
                    for book in data:
                        result.append(book)
            
    
    def run(self, keyword, total_page):
        return asyncio.run(self.search(keyword, total_page))
    


if __name__ == "__main__":
    scraper = NaverbookScraper()
    print(scraper.run("파이썬", 1))
    print(len(scraper.run("파이썬", 5)))