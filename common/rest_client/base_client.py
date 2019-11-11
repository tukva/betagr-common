import os
import aiohttp
import logging

from utils import logger as log


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


    async def get(self, api_uri, params=None, **kwargs):
        try:
            url = self.url + api_uri
            async with aiohttp.request("GET", url, params=params, **kwargs) as resp:
                log.response(self, resp)
                return resp, await resp.read()

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def post(self, api_uri, params=None, data=None, **kwargs):
        try:
            url = self.url + api_uri
            async with aiohttp.request("POST", url, params=params, data=data, **kwargs) as resp:
                log.response(self, resp)
                return resp, await resp.read()

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def put(self, api_uri, params=None, data=None, **kwargs):
        try:
            url = self.url + api_uri
            async with aiohttp.request("PUT", url, params=params, data=data, **kwargs) as resp:
                log.response(self, resp)
                return resp, await resp.json()

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def patch(self, api_uri, params=None, data=None, **kwargs):
        try:
            url = self.url + api_uri
            async with aiohttp.request("patch", url, params=params, data=data, **kwargs) as resp:
                log.response(self, resp)
                return resp, await resp.json()

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def delete(self, api_uri, params=None, **kwargs):
        try:
            url = self.url + api_uri
            async with aiohttp.request("DELETE", url, params=params, **kwargs) as resp:
                log.response(self, resp)
                return resp, await resp.json()

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")
