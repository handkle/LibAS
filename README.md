# 图书馆查询 Python 版

一个逐步迁移现有 C# 项目的 Python 学习项目。

## 已实现

- 使用 Cookie 查询场馆列表
- 在终端显示场馆 ID、名称、楼层和开放状态

## 安装

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 运行

```powershell
.\.venv\Scripts\python.exe main.py
```

按提示输入自己的有效 Cookie。

## 测试

```powershell
.\.venv\Scripts\python.exe test.py
```

## 项目文件

- main.py：程序入口和终端交互
- api_client.py：接口查询与响应解析
- transport.py：HTTP 请求
- test.py：解析逻辑测试

## 项目来源

本项目参考现有 C# 项目进行 Python 迁移。