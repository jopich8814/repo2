import asyncio
from asyncio import sleep

from extract import BinanceExtractor
from repo import ClickhousePriceRepo, TestPriceRepo


async def main():
    repo = TestPriceRepo()
    extractors = [BinanceExtractor(repo)]

    for extractor in extractors:
        asyncio.create_task(extractor.run(), name=extractor.__class__.__name__)

    while True:
        await sleep(2)


if __name__ == '__main__':
    asyncio.run(main())
