import urllib.request as ur
import urllib.error as u_err
import re
from urllib3.response import HTTPResponse
from urllib3 import PoolManager
from typing import Tuple

pattern = re.compile('bytes (\d+)-(\d+)/(\d+)')


def download_from_url(url: str, folder: str) -> str:
    try:
        filename: str = url.split('/')[-1]
        ur.urlretrieve(url, folder+filename)
        print('downloaded file to '+folder+filename)

    except Exception as err:

        raise err
    else:
        return filename


def get_stream_from_url(url: str) -> Tuple:
    try:
        filename: str = url.split('/')[-1]
        #pool: PoolManager = PoolManager()
        #stream: HTTPResponse = pool.request('GET', url)
        request = ur.Request(url)
        response = ur.urlopen(request)
        print('fetched stream for file %s' % filename)

    except Exception as err:

        raise err
    else:
        return filename, response


def download_chunk_from_url(url: str, folder: str, byte_range: str, filename: str) -> str:
    try:
        #filename: str = url.split('/')[-1]+str(chunk_number)
        #ur.urlretrieve(url, folder+filename)
        opener = ur.build_opener()
        opener.addheaders = [('Range', byte_range)]
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        ur.install_opener(opener)
        ur.urlretrieve(url, folder+filename)
        #request = ur.Request(url)
        #request.headers['Range'] = byte_range
        #request.headers['User-Agent'] = 'Mozilla/5.0'
        #response = ur.urlopen(request)
        #response = opener.open(request)
        #with open(folder+filename, "wb") as f:
        #    f.write(response.read())
        print('downloaded file to '+folder+filename)

    except Exception as err:

        raise err
    else:
        return filename


def get_content_length(url) -> int:
    request = ur.Request(url)
    response = ur.urlopen(request)
    content_range: str = response.headers['content-range']
    (start, end, length) = pattern.search(content_range).groups()
    return int(length)


