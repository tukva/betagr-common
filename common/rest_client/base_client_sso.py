import os

from .base_client import BaseClient


class BaseClientSSO(BaseClient):
    """Base api client that describes full standard api for SSO service.
    _api_uri should contains the [key:value, ..] in form [method_name: api_uri which is used by the method, ..]"""
    
    _host = os.getenv('SSO_API_HOST')
    _port = os.getenv('SSO_API_PORT')

    def __init__(self, headers):
        super().__init__(headers=headers)
        self._api_uri = {
            'sign_up': 'sign-up',
            'sign_in': 'sign-in',
            'sign_out': 'sign-out',
            'reset_password': 'reset-password',
        }

    async def sign_up(self, body):
        url = self._api_uri['sign_up']
        resp, resp_body = await self.post(url, body=body, cookies=self._cookies)
        self.update_cookies(resp.cookies or {})

        return resp, resp_body


    async def sign_in(self, body):
        url = self._api_uri['sign_in']
        resp, resp_body = await self.post(url, body=body, cookies=self._cookies)
        self.update_cookies(resp.cookies or {})

        return resp, resp_body


    async def sign_out(self):
        url = self._api_uri['sign_out']
        resp, resp_body = await self.post(url, cookies=self._cookies)
        self.update_cookies(resp.cookies or {})

        return resp, resp_body

    async def reset_password(self, body):
        url = self._api_uri['reset_password']
        resp, resp_body = await self.patch(url, body=body, cookies=self._cookies)
        self.update_cookies(resp.cookies or {})

        return resp, resp_body
