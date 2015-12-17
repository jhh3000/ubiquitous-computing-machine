from cache import Cache
from yahoo import backtest


cache = Cache()
#html_doc = cache.get()
#cache.update()

data = cache.get()

print backtest(data[max(data)][0])