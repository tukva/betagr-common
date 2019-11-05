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
        body = {'username': username,
                'password': password,
                'password_repeat': password}

        return await self.post(url, body=body)


    async def sign_in(self, username=None, password=None):
        url = 'sign-in'
        body = {'username': username or self.username,
                'password': password or self.password}

        response = await super().post(url, body=body)

        if response.status == 200:
            self.token = response.cookies['session'].value
            self.username = username
            self.password = password

        return response


    async def sign_out(self, token=None):
        url = 'sign-out'
        body = {'session': token or self.token}

        return await self.post(url, body=body)


    async def reset_password(self, new_password, username=None, old_password=None):
        url = 'reset-password'

        body = {'username': username or self.username,
                'old_password': old_password or self.password,
                'new_password': new_password,
                'new_password_repeat': new_password}

        response = await super().patch(url, body=body)

        if response.status == 200:
            self.password = new_password

        return response


# example
if __name__ == "__main__":
    async def main():
        async with aiohttp.ClientSession() as session:
            custom_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            sso_client = BaseClientSSO(session, custom_headers, 'vlad', 'qwerty')

            response = await sso_client.sign_up('john doe', 'qwerty')
            print(response)

            response = await sso_client.sign_in()
            print(response)

            response = await sso_client.reset_password('asdfgh')
            print(response)

            response = await sso_client.sign_out()
            print(response)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

