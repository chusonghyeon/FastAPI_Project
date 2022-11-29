# 코루틴 hello world!
# https://docs.python.org/ko/3/library/asyncio-task.html

import asyncio

# 일반적인 서브루틴
async def hello_world():
    print("hello world")
    return 123


if __name__ == "__main__":
    # asyncio를 통해 파이썬 함수를 실행시켜준다
    asyncio.run(hello_world())