import abc
import logging
import os
from asyncio import sleep

from binance import AsyncClient


from repo import PriceRecord, BasePriceRepo

logger = logging.getLogger(__name__)
fileHandler = logging.StreamHandler()
os.makedirs('logs', exist_ok=True)
consoleHandler = logging.FileHandler(f'logs/{__name__ }.log')
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
logger.setLevel(logging.INFO)


class BaseExtractor(abc.ABC):
    def __init__(self, repo: BasePriceRepo):
        self.repo = repo
        logger.info(f'initialized {self.__class__.__name__} with repo {self.repo.__class__.__name__}')

    @abc.abstractmethod
    async def run(self):
        pass

    async def save(self, price_record):
        await self.repo.insert(price_record)


class BinanceExtractor(BaseExtractor):
    """
    Uses python-binance library with REST API calls.
    """
    @staticmethod
    def get_symbol_mapping(exchange_info: dict) -> dict:
        result = {}
        for symbol in exchange_info['symbols']:
            s = symbol['symbol']
            base = symbol['baseAsset']
            quote = symbol['quoteAsset']
            result[s] = (base, quote)
        return result

    async def run(self):
        client = await AsyncClient.create()
        exchange_info = await client.get_exchange_info()
        symbols_mapping = self.get_symbol_mapping(exchange_info)
        logger.info(f'got exchange info from Binance: {len(symbols_mapping)} symbols exist')

        while True:
            tickers = await client.get_all_tickers()
            logger.debug(f'Binance {tickers=}')
            for symbol in tickers:
                base, quote = symbols_mapping[symbol['symbol']]
                if base != 'USDT' or quote != 'RUB':
                    continue
                record = PriceRecord(exchange='Binance',
                                     symbol=symbol['symbol'],
                                     base=base,
                                     quote=quote,
                                     last_price=symbol['price'],
                                     )
                await self.repo.insert(record)

            await sleep(60)
