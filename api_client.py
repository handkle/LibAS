from transport import post_graghql

LIBRARY_QUERY = """
query list{
    userAuth{
        reserve{
            libs(libType: -1){
                lib_id
                lib_name
                lib_floor
                is_open
            }
        }
    }
}
"""

def parse_libraries(result):
    """
    提取场馆列表，并过滤楼层为字符串 '0' 的记录。
    """
    if result.get('errors'):
        raise ValueError(
            '服务端返回GraghQL错误，尚未取得场馆列表'
        )

    try:
        libraries = result['data']['userAuth']['reserve']['libs']
    except (KeyError, TypeError) as exc:
        raise ValueError(
            '响应中缺少场馆列表，请检查登录状态和接口格式'
        )from exc

    if not isinstance(libraries,list):
        raise ValueError('响应中的场馆列表格式不正确')

    output=[]

    for library in libraries:
        if not isinstance(library,dict):
            raise ValueError('场馆记录格式不正确')
        required_fields = (
            'lib_id',
            'lib_name',
            'lib_floor',
            'is_open',
        )

        if any(field not in library for field in required_fields):
            raise ValueError('场馆记录缺少必要字段')

        if library['lib_floor'] == '0':
            continue

        output.append(library)

    return output

def get_libraries(cookie):
    """
    请求场馆列表
    """
    payload = {
        'operationName':'list',
        'query':LIBRARY_QUERY,
    }

    result = post_graghql(cookie, payload)
    return parse_libraries(result)