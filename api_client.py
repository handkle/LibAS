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

LIBRARY_LAYOUT_QUERY = """
query libLayout($libId: Int, $libType: Int) {
  userAuth {
    reserve {
      libs(libType: $libType, libId: $libId) {
        lib_id
        lib_name
        lib_floor
        is_open
        lib_layout {
          seats_total
          seats_booking
          seats_used
          seats {
            x
            y
            key
            type
            name
            seat_status
            status
          }
        }
      }
    }
  }
}
"""

def get_library_layout(cookie, library_id):
    """查询指定场馆布局"""
    payload = {
        "operationName": "libLayout",
        "query": LIBRARY_LAYOUT_QUERY,
        "variables": {
            "libId": library_id,
        },
    }

    result = post_graghql(cookie, payload)

    if result.get('errors'):
        raise ValueError("服务端返回 GraphQL 错误，未取得布局")

    try:
        libraries = result['data']['userAuth']['reserve']['libs']

        if not isinstance(libraries,list) or not libraries:
            raise ValueError("服务端没有返回场馆布局")

        library = libraries[0]

        if library['lib_id'] != library_id:
            raise ValueError("返回的场馆 ID 与请求不一致")

        layout = library['lib_layout']

        if not isinstance(layout,dict):
            raise ValueError("布局格式不正确")

        for field in ['seats_total',  'seats_used', 'seats_booking']:
            if field not in layout:
                raise ValueError(f"布局缺少字段：{field}")

        if not isinstance(layout.get("seats"),list):
            raise ValueError("布局中的 seats 不是列表")

    except (KeyError, TypeError) as exc:
        raise ValueError("场馆布局响应结构不符合预期")from exc

    return library
