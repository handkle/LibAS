from getpass import getpass
import httpx
from api_client import get_libraries, get_library_layout

def main():
    print('场馆与座位布局查询程序')
    print('请输入Cookie,输入时不显示字符.')

    cookie = getpass('Cookie:').strip()

    if not cookie:
        print('没有输入Cookie，程序结束.')
        return

    try:
        libraries = get_libraries(cookie)

        if not libraries:
            print("没有可显示的场馆。")

        print(f"\n共获取到 {len(libraries)} 个场馆：")

        for library in libraries:
            status = 'Open' if library['is_open'] else 'Closed'

            print(
                f"ID：{library['lib_id']} | "
                f"名称：{library['lib_name']} | "
                f"楼层：{library['lib_floor']} | "
                f"状态：{status}"
            )

        text = input("\n请输入要查询的场馆 ID：").strip()

        try:
            library_id = int(text)

        except ValueError:
            print("场馆 ID 必须是整数，例如 126500。")
            return

        selected = None

        for library in libraries:
            if library['lib_id'] == library_id:
                selected = library
                break

        if selected is None:
            print('这个 ID 不在刚才显示的场馆列表中')
            return

        library = get_library_layout(cookie,library_id)
        layout = library['lib_layout']


        print(f"\n场馆：{library['lib_name']}")
        print(f"座位总数：{layout['seats_total']}")
        print(f"已使用数量：{layout['seats_used']}")
        print(f"已预约数量：{layout['seats_booking']}")

        seats=[]
        print('\n座位记录')

        for item in layout['seats']:
            if not isinstance(item, dict):
                continue

            if item.get('type') not in (1,'1'):
                continue
            seats.append(item)
        preview = seats[:10]
        print('\n座位记录（最多显示前 10 条）：')

        for seat in preview:
            name = seat.get('name') or '未提供'
            seat_key = seat.get('key') or '未提供'
            print(
                f"名称：{name} | "
                f"key：{seat_key} | "
                f"坐标：({seat.get('x')}, {seat.get('y')}) | "
                f"status：{seat.get('status')} | "
                f"seat_status：{seat.get('seat_status')}"
            )

        print(
            f"\n共找到 {len(seats)} 条座位记录，"
            f"本次显示 {len(preview)} 条。"
        )
        named_count = 0
        keyed_count = 0

        for seat in seats:
            if seat.get('name'):
                named_count += 1

            if seat.get('key'):
                keyed_count += 1

        print(f"有名称的座位记录：{named_count} 条")
        print(f"有 key 的座位记录：{keyed_count} 条")

        target_name = input(
            "\n请输入要选择的座位名称，例如 389："
        ).strip()

        if not target_name:
            print("没有输入座位名称，程序结束。")
            return

        matchs = []

        for seat in seats:
            name = seat.get('name')
            if name is not None and str(name).strip() == target_name:
                matchs.append(seat)

        if not matchs:
            print(f"当前场馆中没有找到名称为 {target_name} 的座位。")
            return

        if len(matchs) > 1:
            print('找到多个同名座位，本次未确定选择。')
            return

        selected_seat = matchs[0]
        seat_key = selected_seat.get('key')

        if not isinstance(seat_key, str) or not seat_key.strip():
            print("这个座位缺少有效的 key，无法完成选择。")
            return


        print("\n已选择：")
        print(f"场馆：{library['lib_name']}")
        print(f"场馆 ID：{library_id}")
        print(f"座位名称：{selected_seat['name']}")
        print(f"座位 key：{seat_key}")
        print(
            f"坐标："
            f"({selected_seat.get('x')}, {selected_seat.get('y')})"
        )

        if not library['is_open']:
            print("本次布局响应显示场馆处于关闭状态。")

        print("已完成本地选择，尚未发送预约请求。")
    except httpx.TimeoutException:
        print("请求超时，请稍后重新运行。")
    except httpx.HTTPStatusError as exc:
        print(f"HTTP 请求失败：{exc.response.status_code}")
    except httpx.RequestError as exc:
        print(f"网络请求失败：{type(exc).__name__}：{exc}")
    except ValueError as exc:
        print(f"读取数据失败：{exc}")
if __name__ == '__main__':
    main()