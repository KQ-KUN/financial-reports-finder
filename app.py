from flask import Flask, render_template, request
import requests

app = Flask(__name__)

HEADERS = {
    "User-Agent": "FinancialReportsFinder/1.0 contact@example.com",
    "Accept-Encoding": "gzip, deflate",
    "Host": "data.sec.gov"
}

# 支持查询的公司列表（30家）
COMPANY_MAP = [
    {"ticker": "AAPL", "title": "Apple Inc.", "aliases": ["APPLE", "APPLE INC", "苹果"], "cik": "0000320193"},
    {"ticker": "MSFT", "title": "Microsoft Corp", "aliases": ["MICROSOFT", "MICROSOFT CORP", "微软"], "cik": "0000789019"},
    {"ticker": "AMZN", "title": "Amazon.com, Inc.", "aliases": ["AMAZON", "AMAZON.COM", "亚马逊"], "cik": "0001018724"},
    {"ticker": "META", "title": "Meta Platforms, Inc.", "aliases": ["META", "FACEBOOK", "META PLATFORMS", "脸书"], "cik": "0001326801"},
    {"ticker": "TSLA", "title": "Tesla, Inc.", "aliases": ["TESLA", "特斯拉"], "cik": "0001318605"},
    {"ticker": "GOOGL", "title": "Alphabet Inc.", "aliases": ["GOOGLE", "ALPHABET", "谷歌"], "cik": "0001652044"},
    {"ticker": "NVDA", "title": "NVIDIA CORP", "aliases": ["NVIDIA", "英伟达"], "cik": "0001045810"},
    {"ticker": "NFLX", "title": "Netflix, Inc.", "aliases": ["NETFLIX", "奈飞"], "cik": "0001065280"},
    {"ticker": "INTC", "title": "Intel Corp", "aliases": ["INTEL", "英特尔"], "cik": "0000050863"},
    {"ticker": "AMD", "title": "ADVANCED MICRO DEVICES INC", "aliases": ["AMD"], "cik": "0000002488"},

    {"ticker": "ORCL", "title": "Oracle Corp", "aliases": ["ORACLE"], "cik": "0001341439"},
    {"ticker": "ADBE", "title": "Adobe Inc.", "aliases": ["ADOBE"], "cik": "0000796343"},
    {"ticker": "CSCO", "title": "Cisco Systems, Inc.", "aliases": ["CISCO"], "cik": "0000858877"},
    {"ticker": "QCOM", "title": "QUALCOMM INC/DE", "aliases": ["QUALCOMM"], "cik": "0000804328"},
    {"ticker": "CRM", "title": "Salesforce, Inc.", "aliases": ["SALESFORCE"], "cik": "0001108524"},
    {"ticker": "UBER", "title": "Uber Technologies, Inc", "aliases": ["UBER"], "cik": "0001543151"},
    {"ticker": "ABNB", "title": "Airbnb, Inc.", "aliases": ["AIRBNB"], "cik": "0001559720"},
    {"ticker": "PLTR", "title": "Palantir Technologies Inc.", "aliases": ["PALANTIR"], "cik": "0001321655"},
    {"ticker": "PYPL", "title": "PayPal Holdings, Inc.", "aliases": ["PAYPAL"], "cik": "0001633917"},
    {"ticker": "SHOP", "title": "SHOPIFY INC.", "aliases": ["SHOPIFY"], "cik": "0001594805"},

    {"ticker": "WMT", "title": "Walmart Inc.", "aliases": ["WALMART"], "cik": "0000104169"},
    {"ticker": "COST", "title": "Costco Wholesale Corp /new", "aliases": ["COSTCO"], "cik": "0000909832"},
    {"ticker": "MCD", "title": "McDONALDS CORP", "aliases": ["MCDONALDS", "麦当劳"], "cik": "0000063908"},
    {"ticker": "KO", "title": "CocaCola Co", "aliases": ["COCA COLA", "COCACOLA", "可口可乐"], "cik": "0000021344"},
    {"ticker": "SBUX", "title": "Starbucks Corp", "aliases": ["STARBUCKS", "星巴克"], "cik": "0000829224"},
    {"ticker": "NKE", "title": "NIKE, Inc.", "aliases": ["NIKE", "耐克"], "cik": "0000320187"},
    {"ticker": "DIS", "title": "Walt Disney Co", "aliases": ["DISNEY", "迪士尼"], "cik": "0001744489"},
    {"ticker": "JPM", "title": "JPMORGAN CHASE & CO", "aliases": ["JPMORGAN", "JPM"], "cik": "0000019617"},
    {"ticker": "V", "title": "VISA INC.", "aliases": ["VISA"], "cik": "0001403161"},
    {"ticker": "MA", "title": "Mastercard Inc", "aliases": ["MASTERCARD"], "cik": "0001141391"}
]


def get_company_list_for_display():
    company_list = []
    for company in COMPANY_MAP:
        company_list.append({
            "ticker": company["ticker"],
            "title": company["title"]
        })
    company_list.sort(key=lambda x: x["ticker"])
    return company_list


def find_company(query):
    query = query.strip()
    if not query:
        return None

    query_upper = query.upper()

    # 1. 精确匹配 ticker
    for company in COMPANY_MAP:
        if company["ticker"] == query_upper:
            return company

    # 2. 精确匹配正式公司名
    for company in COMPANY_MAP:
        if company["title"].upper() == query_upper:
            return company

    # 3. 匹配别名
    for company in COMPANY_MAP:
        if query_upper in company["aliases"]:
            return company

    # 4. 模糊匹配公司名
    for company in COMPANY_MAP:
        if query_upper in company["title"].upper():
            return company

    return None


def get_company_filings(query):
    company = find_company(query)

    if not company:
        return {
            "error": f"未找到与“{query}”对应的公司。请尝试输入股票代码（如 AAPL）或下方名单中的公司名称。"
        }

    ticker = company["ticker"]
    cik = company["cik"]
    company_name = company["title"]

    url = f"https://data.sec.gov/submissions/CIK{cik}.json"

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return {"error": f"获取财报数据失败：{str(e)}"}

    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accession_numbers = recent.get("accessionNumber", [])
    primary_documents = recent.get("primaryDocument", [])

    annual_reports = []
    quarterly_reports = []
    other_reports = []

    for i in range(len(forms)):
        form = forms[i]

        if form not in ["10-K", "10-Q", "20-F", "6-K"]:
            continue

        accession_no_dash = accession_numbers[i].replace("-", "")
        primary_doc = primary_documents[i]

        filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_no_dash}/{primary_doc}"
        filing_detail_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_no_dash}/{accession_numbers[i]}-index.htm"

        filing_item = {
            "company": company_name,
            "ticker": ticker,
            "form": form,
            "date": dates[i],
            "url": filing_url,
            "detail_url": filing_detail_url
        }

        if form in ["10-K", "20-F"]:
            annual_reports.append(filing_item)
        elif form == "10-Q":
            quarterly_reports.append(filing_item)
        else:
            other_reports.append(filing_item)

        if len(annual_reports) + len(quarterly_reports) + len(other_reports) >= 12:
            break

    return {
        "company": company_name,
        "ticker": ticker,
        "annual_reports": annual_reports,
        "quarterly_reports": quarterly_reports,
        "other_reports": other_reports
    }


@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    keyword = ""
    company_list = get_company_list_for_display()

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        if keyword:
            data = get_company_filings(keyword)
        else:
            data = {"error": "请输入股票代码或公司名称。"}

    return render_template(
        "index.html",
        data=data,
        keyword=keyword,
        company_list=company_list
    )


if __name__ == "__main__":
    app.run(debug=True)