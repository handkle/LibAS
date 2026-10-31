# LibAS · 图书馆查询 Python 版

一个逐步迁移现有 C# 项目的 Python 学习项目，通过终端查询场馆与座位布局，并按座位名称完成本地选择。

## 已实现

- 输入自己的有效 Cookie，查询场馆列表。
- 显示场馆 ID、名称、楼层与开放状态。
- 输入场馆 ID，查询座位布局及座位总数、已使用数量、已预约数量。
- 筛选 `type` 为 `1` 或 `"1"` 的座位记录，预览前 10 条的名称、`key`、坐标和原始状态字段。
- 统计座位记录数量，以及具有非空名称和 `key` 的记录数量。
- 按名称从全部座位记录中查找座位，检查重名和无效 `key`，显示选择结果。
- 显示网络超时、HTTP 错误、网络连接错误及数据解析错误提示。

当前仅完成查询与本地选座，尚未实现预约记录查询、提交预约或取消预约。场馆开放状态和座位状态来自本次接口响应，本地选择成功不代表可以预约。

## 安装与环境管理

项目使用 uv 管理 Python 3.13 环境及依赖。以下命令适用于 Windows PowerShell，请在包含 `main.py` 的项目根目录执行。

首次使用 uv，可按 [官方安装说明](https://docs.astral.sh/uv/getting-started/installation/) 安装：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安装完成后重新打开终端，执行：

```powershell
uv --version
uv sync --locked
```

`uv sync --locked` 按 `uv.lock` 安装依赖到项目的 `.venv`；使用 `uv run` 时无需手动激活环境。当前项目指定 Python 3.13 系列，与迁移时使用的解释器版本系列一致。

本机 uv 安装在项目的 `.tools` 目录（已被 Git 忽略）。在本机项目根目录执行以下命令，即可在当前终端使用 `uv`；新终端需要再次执行。其他电脑请使用上面的官方安装方式。

```powershell
$env:Path = "$PWD\.tools;$env:Path"
$env:UV_CACHE_DIR = "$PWD\.uv-cache"
```

网络请求使用 `httpx`，测试使用 Python 自带的 `unittest`。直接依赖写在 `pyproject.toml`，完整版本由 `uv.lock` 锁定。

常用命令：

```powershell
uv add 包名
uv remove 包名
uv sync --locked
uv run python test.py
```

`requirements.txt` 是从锁文件生成的 pip 兼容清单，不再手工维护。依赖变更后可重新导出：

```powershell
uv export --locked --format requirements-txt --no-hashes --output-file requirements.txt
```

将 `pyproject.toml`、`uv.lock`、`.python-version` 和更新后的 `requirements.txt` 提交到版本管理；`.venv/` 继续忽略。PyCharm 的项目解释器可继续选择项目中的 `.venv\Scripts\python.exe`。

## 运行

```powershell
uv run python main.py
```

按顺序操作：

1. 输入自己的有效 Cookie。终端输入时不显示字符。
2. 查看场馆列表，输入其中一个场馆 ID。
3. 查看布局统计和前 10 条座位记录。
4. 输入座位名称。程序会在全部座位中匹配，不限于预览的 10 条。
5. 查看所选场馆、座位名称、座位 `key` 和坐标，程序随后结束。

Cookie 需要自行准备；当前没有自动登录或获取 Cookie 的流程。不要将真实 Cookie 写入源码或提交到 GitHub。

### 选择结果示例

以下为一次运行的结果节选，实际场馆、座位和状态以接口返回为准：

```text
请输入要选择的座位名称，例如 389：270

已选择：
场馆：212自习室
场馆 ID：126500
座位名称：270
座位 key：23,11
坐标：(11, 23)
本次布局响应显示场馆处于关闭状态。
已完成本地选择，尚未发送预约请求。
```

座位名称用于查找，`key` 直接取自接口返回。`status` 和 `seat_status` 当前按原始值显示，不作为可预约保证。

## 测试

```powershell
uv run python test.py
```

现有三个测试使用模拟数据验证场馆列表解析：

- 过滤楼层为字符串 `"0"` 的记录。
- 将 GraphQL 错误响应转换为 `ValueError`。
- 在响应缺少必要数据时抛出 `ValueError`。

测试不需要 Cookie，也不访问真实接口。当前测试未覆盖布局查询和座位选择流程。

## 项目文件

| 文件 | 职责 |
| --- | --- |
| `main.py` | 终端交互、场馆选择、座位预览、按名称选座与错误提示 |
| `api_client.py` | GraphQL 查询内容、场馆列表解析及布局响应检查 |
| `transport.py` | 使用 HTTPX 发送请求、检查 HTTP 状态并解析 JSON |
| `models.py` | 当前为空文件 |
| `test.py` | 场馆列表解析的单元测试 |
| `pyproject.toml` | 项目信息、Python 版本范围与直接依赖 |
| `uv.lock` | uv 生成的完整依赖锁文件 |
| `.python-version` | 项目默认 Python 版本系列 |
| `requirements.txt` | 从 uv.lock 导出的 pip 兼容清单 |
| `LICENSE.txt` | 保留的原项目许可证 |

## 代码流程

```text
main.py
  → get_libraries(cookie)
  → post_graghql(cookie, payload)
  → parse_libraries(result)
  → 显示场馆列表并读取场馆 ID
  → get_library_layout(cookie, library_id)
  → post_graghql(cookie, payload)
  → 检查布局响应并返回场馆数据
  → 筛选座位、显示预览、按名称查找
  → 显示本地选择结果
```

`post_graghql` 是当前源码中的函数名。

## 项目来源与许可

本项目基于 [EJianZQ/IGoLibrary](https://github.com/EJianZQ/IGoLibrary)
进行 Python 迁移与学习开发。

原项目采用 MIT License，原许可证全文保留于 [LICENSE.txt](LICENSE.txt)。
Python 迁移及后续修改由 handkle 完成。


