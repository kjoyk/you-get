'下载12371视频'
import requests
from lxml import etree
import pathlib
import sys
import os

sys.path.insert(1, r'D:\codes\work\you-get\src')
from you_get.extractors.xuexi import download
from functools import partial
dw = partial(download, merge=True, output_dir='./')


def dw_url(url, dp):
    dp = pathlib.Path(dp)
    dp.mkdir(exist_ok=True, parents=True)
    os.chdir(dp)
    htm = requests.get(url).content
    e = etree.HTML(htm)
    os.chdir(dp)
    for url in set(e.xpath('//a[contains(@href,"VIDE")]/@href')):
        dw(url)


# dw_url('http://xuexi.12371.cn/2015/07/22/VIDA1437550221426905.shtml',
#        'd:/践行三严三实的好榜样')
# dw_url('http://xuexi.12371.cn/2013/06/24/VIDA1372053134864695.shtml',
#        'd:/红色故事汇')

dw_url('http://www.12371.cn/special/dyjydsp15/05/',r'D:\第十五届全国党教片交流优秀作品\优秀奖')