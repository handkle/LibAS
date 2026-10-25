import httpx

ENDPOINTS = 'https://wechat.v2.traceint.com/index.php/graphql/'

USEAGENT = (
    "Mozilla/5.0 (Windows NT 6.1; WOW64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/81.0.4044.138 Safari/537.36 "
    "NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) "
    "WindowsWechat(0x63070626)"
)

def post_graghql(cookie, payload):
    """
    发送一次 GraphQL 请求，返回解析后的响应。
    """
    headers = {
        'Cookie':cookie,
        'Origin':'https://wechat.traceint.com',
        'Referer':'https://wechat.traceint.com',
        'User-Agent':USEAGENT,
        'App-Version':'2.0.11',
        'Accept':'*/*',
    }

    with httpx.Client(timeout=20.0) as client:
        response=client.post(
            ENDPOINTS,
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        result=response.json()
        if not isinstance(result,dict):
            raise ValueError("服务器返回的数据不是预期的 JSON 对象")
        return result