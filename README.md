# BetAgr-common - base async api-clients for betagr-project wrote with aiohttp

A set of tools, utilities and base async api-classes for maintaining the infrastructure of betagr-project services.

### Requirements

* python>=3.6
* aiohttp>=3.6

### Usage

BetAgr-common ships with two base api-classes: BaseClient and BaseClientSSO.

##### BaseClient

It is a base class provides a basic REST API methods which are simple wrapper over a aiohttp.request.
Сlass also implements basic logging of client requests and handling cookies within one client, since the connection session exists only during one request.

Api-clients of each  services should be inherited from the BaseClient.

```
class BakeryClient(BaseClient):
    _host = 'www.some-bakery.com'

    async def bake_bread(self, bread_flour='first-grade'):
        body = {'flour': bread_flour}
        response = await super().post(url, body=body, cookies=self._cookies)
        self.update_cookies(response.cookies or {})

        return response
```

```python
    async def main():
        async for client in db_clients_orders:
            custom_headers = {'Content-Type': 'application/json'}

            bakery_client = BakeryClient(custom_headers)
            
            bread_flour_type = client['flour']            

            response = await bakery_client.bake_bread(bread_flour_type)
            print(response)    # bread was bake!

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())  
```

##### BaseClientSSO
Api abstraction for sso-client with the release of basic methods:
* sign_up
* sign_in
* sign_out
* reset_password

``BaseClientSSO._api_uri`` should be used to represent method and relevant api path.
For default it looks like:
```python
BaseClientSSO._api_uri = {
            'sign_up': 'sign-up',
            'sign_in': 'sign-in',
            'sign_out': 'sign-out',
            'reset_password': 'reset-password',
        }
```

Use ``sef._api_uri.apdate({'my_new_method': 'api_uri'})``  - it is some kind of bookmark that makes it easy to maintain your inherited classes.

```python
async def main():

        custom_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        sso_client_one = BaseClientSSO(custom_headers)

        body = {'username': 'john doe',
                'password': 'qwerty'}

        response = await sso_client_one.sign_up(body)
        print(response)

        body = {'username': 'john doe',
                'password': 'qwerty'}

        response = await sso_client_one.sign_in(body)
        print(response)

        body = {'username': 'john doe',
                'old_password': 'qwerty',
                'new_password': 'qwerty'}

        response = await sso_client_one.reset_password(body)
        print(response)

        response = await sso_client_one.sign_out()
        print(response)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```
Environment variables are used to determine url parameters in base classes:
|               .env             |         value         |
|               ---              |          ---          |
| BASE_API_HOST                  |  'http://example.com' |
| BASE_API_PORT                  |          8080         |
| SSO_API_HOST                   | 'http://example.com'  |
| SSO_API_PORT                   |         8080          |
| COMMON_API_CLIENT_LOGGING_MODE | 0, 10, 20, 30, 40, 50 |