import os
import aiohttp
import logging

from utils import utils, logger


class BaseClient:

    _host = os.getenv('BASE_API_HOST')
    _port = os.getenv('BASE_API_PORT')

    def __init__(self, headers):
        self.headers = headers
        self._cookies = {}
        self._url = f'{self._host}:{self._port}'
        logger.start_logging(client=self)


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


    async def _request(self, method, api_uri, params=None, body=None, **kwargs):
        """ Just a simple wrapper under aiohttp.request method.
        :param method: str,
        :param api_uri:  str,
        :param params: Optional[Mapping[str, str]]=None,
        :param body: key/value container=None,
        :return: ClientResponse
        """
        url = utils.full_url(self.url, api_uri, params)

        logging.info(f'Request by {self.__class__.__name__}: '
                     f'"{method} {url}" with data: "{body}" ')

        body = utils.prepared_data(body)

        try:
            async with aiohttp.request(method, url, data=body, params=params, headers=self.headers, **kwargs) as response:
                return response

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def get(self, api_uri, params, **kwargs):
        response = await self._request('GET', api_uri, params, **kwargs)
        logger.log_response(self, response)

        return response


    async def post(self, api_uri, params=None, body=None, **kwargs):
        response = await self._request('POST', api_uri, params, body, **kwargs)
        logger.log_response(self, response)

        return response


    async def put(self, api_uri, params=None, body=None, **kwargs):
        response = await self._request('PUT', api_uri, params, body, **kwargs)
        logger.log_response(self, response)

        return response


    async def patch(self, api_uri, params=None, body=None, **kwargs):
        response = await self._request('PATCH', api_uri, params, body, **kwargs)
        logger.log_response(self, response)

        return response


    async def delete(self, api_uri, params, **kwargs):
        response = await self._request('DELETE', api_uri, params, **kwargs)
        logger.log_response(self, response)

        return response
