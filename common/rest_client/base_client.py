import os
import aiohttp
import logging

from utils import logger as log
from utils.utils import prepared_data


class BaseClient:

    _host = os.getenv('BASE_API_HOST')
    _port = os.getenv('BASE_API_PORT')

    def __init__(self, headers):
        self.headers = headers
        self._cookies = {}
        self._url = f'{self._host}:{self._port}/'
        log.start_logging(client=self)


    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def url(self):
        return self._url

    def update_cookies(self, cookies):
        """ Use to update client cookies
        :param cookies: http.cookie.SimpleCookie
        :return: None
        """
        try:
            for key, morsel in cookies.items():
                self._cookies.update({key: str(morsel.value)})
        except Exception as e:
            logging.error(f"Client [update cookie] error: {e.__class__.__name__}: {e}", exc_info=True)


    async def _request(self, method,api_uri, params=None, data=None, **kwargs):
        url = self.url + api_uri
        data = prepared_data(data)

        try:
            async with aiohttp.request(method=method, url=url, params=params, **kwargs) as resp:
                log.response(self, resp)
                return {'response': resp,
                        'json': resp.json(),
                        'raw_data': resp.read()}

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def _get(self, api_uri, params=None, **kwargs):
        return self._request('GET', api_uri=api_uri, params=params, **kwargs)

    async def _post(self, api_uri, params=None, data=None, **kwargs):
        return self._request('POST', api_uri=api_uri, params=params, data=data, **kwargs)

    async def _put(self, api_uri, params=None, data=None, **kwargs):
        return self._request('PUT', api_uri=api_uri, params=params, data=data, **kwargs)


    async def get(self, api_uri, params=None, **kwargs):
        try:
            url = self.url + api_uri
            async with aiohttp.request("GET", url, params=params, **kwargs) as resp:
                log.response(self, resp)
                if 'json' in resp.headers.get('Content-Type'):
                    return resp, await resp.json()
                return resp, await resp.read()

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def post(self, api_uri, params=None, data=None, **kwargs):
        try:
            url = self.url + api_uri
            async with aiohttp.request("POST", url, params=params, data=data, **kwargs) as resp:
                log.response(self, resp)
                if 'json' in resp.headers.get('Content-Type'):
                    return resp, await resp.json()
                return resp, await resp.read()

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def put(self, api_uri, params=None, data=None, **kwargs):
        try:
            url = self.url + api_uri
            async with aiohttp.request("PUT", url, params=params, data=data, **kwargs) as resp:
                log.response(self, resp)
                if 'json' in resp.headers.get('Content-Type'):
                    return resp, await resp.json()
                return resp, await resp.read()

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def patch(self, api_uri, params=None, data=None, **kwargs):
        try:
            url = self.url + api_uri
            async with aiohttp.request("patch", url, params=params, data=data, **kwargs) as resp:
                log.response(self, resp)
                if 'json' in resp.headers.get('Content-Type'):
                    return resp, await resp.json()
                return resp, await resp.read()

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def delete(self, api_uri, params=None, **kwargs):
        try:
            url = self.url + api_uri
            async with aiohttp.request("DELETE", url, params=params, **kwargs) as resp:
                log.response(self, resp)
                if 'json' in resp.headers.get('Content-Type'):
                    return resp, await resp.json()
                return resp, await resp.read()

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")
