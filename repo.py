import abc
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class PriceRecord:
    exchange: str
    symbol: str
    base: str
    quote: str
    last_price: float
    time_received: datetime = field(default_factory=datetime.now)


class BasePriceRepo(abc.ABC):
    @abc.abstractmethod
    async def insert(self, record: PriceRecord):
        pass

    @abc.abstractmethod
    async def get_average_prices_on_date(self, base, dt):
        pass


class TestPriceRepo(BasePriceRepo):
    async def insert(self, record: PriceRecord):
        print(record)

    async def get_average_prices_on_date(self, base, dt):
        pass


class ClickhousePriceRepo(BasePriceRepo):
    """
    Uses bulk insert on python side and buffer ClickHouse engine for inserts speeding up.
    https://clickhouse.com/docs/en/engines/table-engines/special/buffer/

    ClickHouse Schemas:
    CREATE TABLE IF NOT EXISTS price (
        exchange String,
        symbol String,
        base String,
        quote String,
        last_price Float64,
        time_received DateTime64(3, 'Europe/London')
    )
    ENGINE = MergeTree
    PRIMARY KEY (base, quote, time_received)

    CREATE TABLE price_buffer AS price ENGINE = Buffer(db1, price, 16, 1, 10, 1000, 1000000, 10000, 100000000)
    """
    #def __init__(self):
     #   self.client = Client(host='localhost',
      #                       database='db1')
       # self.insert_batch = []

    async def insert(self, record: PriceRecord):
        self.insert_batch.append(record)
        if len(self.insert_batch) > 2000:
            query = 'INSERT INTO price_buffer (*) VALUES '
            values = ''
            for r in self.insert_batch:
                d = {'e': r.exchange,
                     's': r.symbol,
                     'b': r.base,
                     'q': r.quote,
                     'lp': r.last_price,
                     'tr': r.time_received.strftime('%Y-%m-%d %H:%M:%S.%f')}
                value = "('%(e)s', '%(s)s', '%(b)s', '%(q)s', '%(lp)s', '%(tr)s')" % d
                values += value
            query += values
            self.insert_batch = []
            result = self.client.execute(query)

    async def get_average_prices_on_date(self, base, dt):
        result = self.client.execute(
            'SELECT base as c1, null as c2, quote as c3'
            'FROM price'
            'WHERE base = %(base)s AND quote = %(quote)s'
            'UNION'
            'SELECT base as c1, null as c2, quote as c3'
            'FROM price'
            'WHERE quote = %(base)s AND base = %(quote)s'
            'UNION'
            'SELECT a.base as c1, a.quote as c2, b.quote as c3'
            'FROM price AS a JOIN price AS b ON a.quote = b.base'
            'WHERE a.base = %(base)s AND b.quote = %(quote)s',
            {'base': base,
             'date': dt.strftime('%Y-%m-%d %H:%M:%S.%f')}
        )
