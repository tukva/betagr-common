import asyncio
import aiohttp
from base_client import BaseClient

class BaseClientSSO(BaseClient):
    _host = 'http://localhost:8080'

    def __init__(self, session, headers, username, password):
        super().__init__(session, headers)
        self.username = username
        self.password = password
        self.token = None

    async def sign_up(self, username, password):
        url = 'sign-up'
        data = {'username': username,
                'password': password,
                'password_repeat': password}

        return await self.post(url, data=data)


    async def sign_in(self, username=None, password=None):
        url = 'sign-in'
        data = {'username': username or self.username,
                'password': password or self.password}

        response = await super().post(url, data=data)

        if response.status == 200:
            self.token = response.cookies['session'].value
            self.username = username
            self.password = password

        return response


    async def sign_out(self, session=None):
        url = 'sign-out'
        data = {'session': session or self.session}

        return await self.post(url, data=data)


    async def reset_password(self, username=None, old_password=None, new_password='qwerty'):
        url = 'reset-password'
        data = {'username': username or self.username,
                'old_password': old_password or self.password,
                'new_password': new_password,
                'new_password_repeat': new_password}

        response = await super().patch(url, data=data)

        if response.status == 200:
            self.password = new_password

        return response


if __name__ == "__main__":

    async def main():
        async with aiohttp.ClientSession() as session:
            custom_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            client = BaseClientSSO(session, custom_headers, 'vlad', 'qwerty')

            response = await client.sign_up('john doe', 'qwerty')
            print(response)

            response = await client.sign_in('john doe', 'qwerty')
            print(response)

            response = await client.reset_password(new_password='123456')
            print(response)

            response = await client.sign_out()
            print(response)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

