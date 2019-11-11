import asyncio
import aiohttp
from rest_client.base_client import BaseClient

# example
if __name__ == "__main__":
    async def main():

        custom_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        client = BaseClient(custom_headers)
        client._host = 'http://localhost'
        client._port = 8000
        print(client.url)

        # resp = await client.patch(api_uri='parse-links/1/teams')
        # print(resp)

        resp = await client.get(api_uri='parse-links/1/teams')
        print(resp)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
