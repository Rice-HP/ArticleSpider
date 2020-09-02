from scrapy.cmdline import  execute

import  sys
import os
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy","crawl","xiaozu"])
# execute(["scrapy","crawl","zhihu"])
# execute(["scrapy","crawl","text"])
# execute(["scrapy","crawl","lagou"])
execute(["scrapy","crawl","lagou2"])