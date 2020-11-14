#!/usr/bin/env python

import json
import re

from ..common import get_content, r1, match1, playlist_not_supported
from ..extractor import VideoExtractor

__all__ = ['xuexi12371_download', 'xuexi12371_download_by_id']


class XUEXI12371(VideoExtractor):
    name = '12371.cn'
    stream_types = [
        {'id': '1', 'video_profile': '1280x720_2000kb/s', 'map_to': 'chapters4'},
        {'id': '2', 'video_profile': '1280x720_1200kb/s', 'map_to': 'chapters3'},
        {'id': '3', 'video_profile': '640x360_850kb/s', 'map_to': 'chapters2'},
        {'id': '4', 'video_profile': '480x270_450kb/s', 'map_to': 'chapters'},
        {'id': '5', 'video_profile': '320x180_200kb/s', 'map_to': 'lowChapters'},
    ]

    ep = 'http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={}'

    def __init__(self):
        super().__init__()
        self.api_data = None

    def prepare(self, **kwargs):
        self.api_data = json.loads(get_content(self.__class__.ep.format(self.vid)))
        self.title = self.api_data['title']
        for s in self.api_data['video']:
            for st in self.__class__.stream_types:
                if st['map_to'] == s:
                    urls = self.api_data['video'][s]
                    src = [u['url'] for u in urls]
                    stream_data = dict(src=src, size=0, container='mp4', video_profile=st['video_profile'])
                    self.streams[st['id']] = stream_data


def xuexi12371_download_by_id(rid, **kwargs):
    XUEXI12371().download_by_vid(rid, **kwargs)


def xuexi12371_download(url, **kwargs):
    if re.match(r'http://tv\.12371\.cn/video/(\w+)/(\w+)', url):
        rid = match1(url, r'http://tv\.12371\.cn/video/\w+/(\w+)')
    elif re.match(r'http(s)?://tv\.cctv\.com/\d+/\d+/\d+/\w+.shtml', url):
        rid = r1(r'var guid = "(\w+)"', get_content(url))
    elif re.match(r'http://\w+\.12371\.cn/(\w+/\w+/(classpage/video/)?)?\d+/\d+\.shtml', url) or \
         re.match(r'http://\w+.12371.cn/(\w+/)*VIDE\d+.shtml', url) or \
         re.match(r'http://(\w+).12371.cn/(\w+)/classpage/video/(\d+)/(\d+).shtml', url) or \
         re.match(r'http(s)?://\w+.cctv.com/\d+/\d+/\d+/\w+.shtml', url) or \
         re.match(r'http://\w+.12371.cn/\d+/\d+/\d+/\w+.shtml', url): 
        page = get_content(url)
        rid = r1(r'videoCenterId","(\w+)"', page)
        if rid is None:
            guid = re.search(r'guid\s*=\s*"([0-9a-z]+)"', page).group(1)
            rid = guid
    elif re.match(r'http://xiyou.12371.cn/v-[\w-]+\.html', url):
        rid = r1(r'http://xiyou.12371.cn/v-([\w-]+)\.html', url)
    else:
        raise NotImplementedError(url)

    XUEXI12371().download_by_vid(rid, **kwargs)

site_info = "12371.cn"
download = xuexi12371_download
download_playlist = playlist_not_supported('12371')
