from getpass import getpass
import httpx

from api_client import get_reservation

def main():
    cookie = getpass("请输入 Cookie：").strip()

    if not cookie:
        print("没有输入 Cookie，程序结束。")
        return

    try:
        reservation = get_reservation(cookie)

        if reservation is None:
            print("当前没有预约记录。")
            return

        print("\n当前预约：")
        print(f"场馆：{reservation['lib_name']}")
        print(f"场馆 ID：{reservation['lib_id']}")
        print(f"座位名称：{reservation['seat_name']}")
        print(f"座位 key：{reservation['seat_key']}")

        expiration = reservation.get("exp_date_str")

        if expiration:
            print(f"到期时间（接口返回）：{expiration}")
        else:
            print(f"到期时间戳：{reservation['exp_date']}")

    except httpx.TimeoutException:
        print("请求超时，请稍后重试。")
    except httpx.HTTPStatusError as exc:
        print(f"HTTP 请求失败：{exc.response.status_code}")
    except httpx.RequestError as exc:
        print(f"网络请求失败：{type(exc).__name__}：{exc}")
    except ValueError as exc:
        print(f"读取预约失败：{exc}")

if __name__ == "__main__":
    main()