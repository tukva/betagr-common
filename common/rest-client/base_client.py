import asyncio
import aiohttp


def prepared_data(data=None):
    """function should be used(in future) to add custom headers to data."""
    payload = aiohttp.FormData()

    if data:
        for key, value in data.items():
            payload.add_field(key, str(value))

    return payload


class BaseClient:

    _host = None

    def __init__(self, session, headers):
        self.session = session
        self.headers = headers


    async def _request(self, method, api_url, params=None, body=None, **kwargs):
        url = f'{self._host}/{api_url}'
        print(f'Make request: "{url}" with data: "{body}" ')

        if body:
            body = prepared_data(body)

        try:
            async with self.session.request(method, url, data=body, params=params, headers=self.headers, **kwargs) as response:
                return response

        except aiohttp.ClientError as e:
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def get(self, api_url, params, **kwargs):
        response = await self._request('GET', api_url, params, **kwargs)

        return response


    async def post(self, api_url, params=None, body=None, **kwargs):
        response = await self._request('POST', api_url, params, body, **kwargs)

        return response

    async def put(self, api_url, params=None, body=None, **kwargs):
        response = await self._request('PUT', api_url, params, body, **kwargs)

        return response

    async def patch(self, api_url, params=None, body=None, **kwargs):
        response = await self._request('PATCH', api_url, params, body, **kwargs)

        return response

    async def delete(self, api_url, params, **kwargs):
        response = await self._request('DELETE', api_url, params, **kwargs)

        return response
