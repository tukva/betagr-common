import asyncio
import aiohttp


def prepare_data(params=None):
    data = aiohttp.FormData(quote_fields=False)

    if params:
        for key, value in params.items():
            data.add_field(key, str(value))



class BaseClient:

    _host = 'https://www.google.com'
    headers = None

    async def request(self, session, api_url, data=None, **kwargs):
        url = f'{self._host}/{api_url}'

        print(f'Make request: "{api_url}" \nwith data: "{data}" ')

        data = prepare_data(data)
        try:
            async with session.post(url, data=data, headers=self.headers, **kwargs) as response:
                return (response.content_type, response.status, await response.text())

        except aiohttp.ClientError as e:
            raise Exception(f"Client error: {e.__class__.__name__}: {e}")

    # def __init__(self,):
    #     self.username = username
    #     self.password = password
        

    # async def get(self, api_path, params, *args, **kwargs):
    #     request = {
    #             'url': f'{self.host}/{api_path}',
    #             'params': params   
    #         }

    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(*args, **request, **kwargs) as resp:
    #             print(resp.status)

    #             return await resp


    # response = self.session(
    #     url=f'{host}/{api_path}',
    #     method="GET",
    #     params=params,
    #     token=self.token
    # )

    # return response

    # async def post(self, api_path, data, token):
    # response = self.session(
    #     url=host + api_path,
    #     method="POST",
    #     data=serialize(data),
    #     token=self.token
    # )

    # return response

    # async def put(self, api_path, data, token):
    # response = self.session(
    #     url=host + api_path,
    #     method="PUT",
    #     data=serialize(data),
    #     token=self.token,
    # )

    # return response

    # async def patch(self, api_path, data, token):
    # response = self.session(
    #     url=host + api_path,
    #     method="PATCH",
    #     data=serialize(data),
    #     token=self.token
    # )

    # return response

    # async def delete(self, api_path, token):
    # response = self.session(
    #     url=host + api_path,
    #     method="DELETE",
    #     token=self.token
    # )

    # return response