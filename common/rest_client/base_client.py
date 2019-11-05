import aiohttp


def prepared_data(data=None):
    """function should be used(in future) to add custom headers to data."""
    payload = aiohttp.FormData()

    if data:
        for key, value in data.items():
            payload.add_field(key, str(value))

    return payload


class BaseClient:

    _host = 'http://localhost'
    _port = 80

    def __init__(self, session, headers):
        self.session = session
        self.headers = headers
        self.url = f'{self._host}:{self._port}'


    @property
    def host(self):
        return self._host


    @property
    def port(self):
        return self._port


    async def _request(self, method, api_uri, params=None, body=None, **kwargs):
        url = f'{self.url}/{api_uri}'
        print(f'Make request: "{url}" with data: "{body}" ')

        if body:
            body = prepared_data(body)

        try:
            async with self.session.request(method, url, data=body, params=params, headers=self.headers, **kwargs) as response:
                return response

        except aiohttp.ClientError as e:
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")


    async def get(self, api_uri, params, **kwargs):
        response = await self._request('GET', api_uri, params, **kwargs)

        return response


    async def post(self, api_uri, params=None, body=None, **kwargs):
        response = await self._request('POST', api_uri, params, body, **kwargs)

        return response


    async def put(self, api_uri, params=None, body=None, **kwargs):
        response = await self._request('PUT', api_uri, params, body, **kwargs)

        return response


    async def patch(self, api_uri, params=None, body=None, **kwargs):
        response = await self._request('PATCH', api_uri, params, body, **kwargs)

        return response


    async def delete(self, api_uri, params, **kwargs):
        response = await self._request('DELETE', api_uri, params, **kwargs)

        return response
