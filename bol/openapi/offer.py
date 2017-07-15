
import requests
from bol.plaza.api import PlazaAPI

import time
import requests
import hmac
import hashlib
import base64
from datetime import datetime
import collections
from enum import Enum

from xml.etree import ElementTree


# __all__ = ['OfferManagement']


class OfferAPI(PlazaAPI):

    def request(self, method, uri, params={}, data=None):
        uri = "/offers/v2/7103656606473?condition=NEW"
        uri = "/offers/v2/"
        content_type = 'application/xml; charset=UTF-8'
        date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        msg = """{method}

{content_type}
{date}
x-bol-date:{date}
{uri}""".format(content_type=content_type,
                date=date,
                method=method,
                uri=uri)
        h = hmac.new(
            self.private_key.encode('utf-8'),
            msg.encode('utf-8'), hashlib.sha256)
        b64 = base64.b64encode(h.digest())

        signature = self.public_key.encode('utf-8') + b':' + b64

        headers = {'Content-Type': content_type,
                   'X-BOL-Date': date,
                   'X-BOL-Authorization': signature}
        request_kwargs = {
            'method': method,
            'url': self.url + uri,
            'params': params,
            'headers': headers,
            'timeout': self.timeout,
        }
        if data:
            request_kwargs['data'] = data
        resp = requests.request(**request_kwargs)
        resp.raise_for_status()
        tree = ElementTree.fromstring(resp.content)
        return tree
