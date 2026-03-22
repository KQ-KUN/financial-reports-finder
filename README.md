# Financial Reports Finder

一个用于快速查找美国上市公司最近财报链接的小项目。

## Features
- 输入股票代码查询公司财报
- 支持显示最近的 10-K、10-Q、20-F
- 返回 SEC 官方披露链接

## Tech Stack
- Python
- Flask
- Requests
- SEC EDGAR API

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

然后打开浏览器访问：

http://127.0.0.1:5000

## Example Tickers
- AAPL
- MSFT
- AMZN
- GOOGL
- META
- TSLA