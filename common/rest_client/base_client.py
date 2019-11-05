import os
import aiohttp
import logging

from utils import logger


def prepared_data(data=None):
    """function should be used(in future) to add custom headers to data."""
    if not data:
        return None

    payload = aiohttp.FormData()

    for key, value in data.items():
        payload.add_field(key, str(value))

    return payload


def full_url(host, api_uri, params=None):
    url = f'{host}/{api_uri}'
    if params:
        url += f'?{params}'

    return url


class BaseClient:

    _host = os.getenv('BASE_API_HOST', 'http://localhost')
    _port = os.getenv('BASE_API_PORT', 8080)

    def __init__(self, session, headers):
        self.session = session
        self.headers = headers
        self.url = f'{self._host}:{self._port}'
        logger.start_logging(client=self)


    @property
    def host(self):
        return self._host


    @property
    def port(self):
        return self._port


    async def _request(self, method, api_uri, params=None, body=None, **kwargs):
        url = full_url(self.url, api_uri, params)

        logging.info(f'Request by {self.__class__.__name__}: '
                     f'"{method} {url}" with data: "{body}" ')

        body = prepared_data(body)

        try:
            async with self.session.request(method, url, data=body, params=params, headers=self.headers, **kwargs) as response:
                return response

        except aiohttp.ClientError as e:
            logging.error(f"Client error: {e.__class__.__name__}: {e}", exc_info=True)
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def get(self, api_uri, params, **kwargs):
        response = await self._request('GET', api_uri, params, **kwargs)
        logging.info(f'Response to {self.__class__.__name__}: '
                     f'"{response.status} {response.reason}"')

        return response


    async def post(self, api_uri, params=None, body=None, **kwargs):
        response = await self._request('POST', api_uri, params, body, **kwargs)
        logging.info(f'Response to {self.__class__.__name__}: '
                     f'"{response.status} {response.reason}"')

        return response


    async def put(self, api_uri, params=None, body=None, **kwargs):
        response = await self._request('PUT', api_uri, params, body, **kwargs)
        logging.info(f'Response to {self.__class__.__name__}: '
                     f'"{response.status} {response.reason}"')

        return response


    async def patch(self, api_uri, params=None, body=None, **kwargs):
        response = await self._request('PATCH', api_uri, params, body, **kwargs)
        logging.info(f'Response to {self.__class__.__name__}: '
                     f'"{response.status} {response.reason}"')

        return response


    async def delete(self, api_uri, params, **kwargs):
        response = await self._request('DELETE', api_uri, params, **kwargs)
        logging.info(f'Response to {self.__class__.__name__}: '
                     f'"{response.status} {response.reason}"')

        return response
