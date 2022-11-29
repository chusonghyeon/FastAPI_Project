import time
import asyncio

# await : 기다리게 하는 함수
# async함수를 사용해서 비동기적으로 수행 즉, 순차적으로 수행되는것이 아니다
# 바로 다른 함수로 넘어가는 것이다.
# 무조건 비동기 함수가 좋은것은 아니다. 순차적인 계산이 필요한 경우에는 비동기보단 동기가 좋을 수 가 있다.


async def delivery(name, mealtime):
    print(f"{name}에게 배달 완료!")
    # 배달 완료되고 바로 다음 함수로 들어가게 된다.
    await asyncio.sleep(mealtime)
    print(f"{name} 식사 완료, {mealtime}시간 소요...")
    print(f"{name} 그릇 수거 완료")
    return mealtime


async def main():
    
    task1 = asyncio.create_task(delivery("A",2))
    task2 = asyncio.create_task(delivery("B",2))
    
    await task2 # await deliver("A",2)와 같은 개념
    await task1

    result = await asyncio.gather(
        delivery("A", 5),
        delivery("B", 4),
        delivery("C", 3),
    )

    print(result)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)