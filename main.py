from getpass import getpass
import httpx
from api_client import get_libraries

def main():
    print('场馆查询程序')
    print('请输入Cookie,输入时不显示字符.')

    cookie = getpass('Cookie:').strip()

    if not cookie:
        print('没有输入Cookie，程序结束.')
        return

    try:
        libraries = get_libraries(cookie)
    except httpx.TimeoutException:
        print('请求超时，请重试。')
        return
    except httpx.HTTPStatusError as exc:
        print('请求http失败，状态码：{exc.response.status_code}')
        return
    except httpx.RequestError:
        print('网络连接失败，请检查网络或代理设置')
        return
    except ValueError as exc:
        print(f'读取数据失败：{exc}')
        return
    if not libraries:
        print('请求完成，没有可显示场馆')
        return

    print(f"\n共获取到 {len(libraries)} 个场馆：")

    for library in libraries:
        status = 'Open' if library['is_open'] else 'Closed'

        print(
            f"ID：{library['lib_id']} | "
            f"名称：{library['lib_name']} | "
            f"楼层：{library['lib_floor']} | "
            f"状态：{status}"
        )

if __name__ == '__main__':
    main()