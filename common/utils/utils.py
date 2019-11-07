import aiohttp


def prepared_data(data=None):
    """ Function should be used(in future) to add custom headers to data
    for multipart/form-data body generation.
    For present serializes values to str.
    :param data: A container for the key/value pairs,
    :return: aiohttp.FormData
    """
    if not data:
        return None

    payload = aiohttp.FormData()

    for key, value in data.items():
        payload.add_field(key, str(value))

    return payload


def full_url(host, api_uri, params=None):
    """ Create full url from host, api path and query params
    :param host: str,
    :param api_uri: str,
    :param params: Optional[str]=None
    :return: str
    """
    url = f'{host}/{api_uri}'
    if params:
        url += f'?{params}'

    return url