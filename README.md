# 美股上市公司财报查询工具

一个面向中文用户的美股财报查询网页工具，支持通过**股票代码**或**公司名称**，快速查询美国上市公司近期在 **SEC** 官方披露的财报信息。

## 项目简介

本项目旨在帮助用户更方便地获取美国上市公司的公开财报信息。  
用户可以输入股票代码（如 `AAPL`、`MSFT`）或公司名称（如 `Apple`、`Microsoft`），快速查看公司近期披露的年报、季报及其他财务文件，并直接跳转到 SEC 官方原文页面。

## 主要功能

- 支持通过**股票代码**搜索公司财报
- 支持通过**公司名称**搜索公司财报
- 展示近期财报信息，包括：
  - 年报（10-K / 20-F）
  - 季报（10-Q）
  - 其他财务披露（6-K 等）
- 支持打开：
  - 财报原文链接
  - SEC 明细页
- 首页展示**支持查询的公司名单**
- 前端为**中文界面**，更适合内地用户使用
- 已部署为可在线访问的网页应用

## 当前支持查询的公司

目前支持约 30 家热门美股公司，包括但不限于：

- Apple
- Microsoft
- Amazon
- Meta
- Tesla
- Alphabet / Google
- NVIDIA
- Netflix
- Intel
- AMD
- Oracle
- Adobe
- Cisco
- Qualcomm
- Salesforce
- Uber
- Airbnb
- Palantir
- PayPal
- Shopify
- Walmart
- Costco
- McDonald's
- Coca-Cola
- Starbucks
- Nike
- Disney
- JPMorgan
- Visa
- Mastercard

## 技术栈

- Python
- Flask
- Requests
- HTML / CSS
- SEC EDGAR API
- Render（部署）

## 数据来源

本项目财报数据来自 **SEC EDGAR** 官方公开披露接口。  
公司财报信息通过 SEC 的公司 filings 接口获取，并在前端进行分类展示。

## 页面功能说明

首页主要包含以下几个部分：

- 搜索框：输入股票代码或公司名称进行查询
- 工具说明：介绍支持的功能和数据来源
- 支持查询的公司名单：帮助用户快速了解可查询范围
- 财报结果区：按“年报 / 季报 / 其他财务披露”分类展示结果