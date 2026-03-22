from flask import Flask, render_template, request
import requests

app = Flask(__name__)

HEADERS = {
    "User-Agent": "student-project your_email@example.com"
}

CIK_MAP = {
    "AAPL": "0000320193",
    "MSFT": "0000789019",
    "GOOGL": "0001652044",
    "AMZN": "0001018724",
    "META": "0001326801",
    "TSLA": "0001318605"
}


def get_company_filings(ticker):
    ticker = ticker.upper().strip()
    cik = CIK_MAP.get(ticker)

    if not cik:
        return {"error": f"暂不支持 {ticker}，请先试试 AAPL、MSFT、AMZN"}

    url = f"https://data.sec.gov/submissions/CIK{cik}.json"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return {"error": f"获取数据失败：{str(e)}"}

    company_name = data.get("name", ticker)
    recent = data.get("filings", {}).get("recent", {})

    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accession_numbers = recent.get("accessionNumber", [])
    primary_documents = recent.get("primaryDocument", [])

    results = []

    for i in range(len(forms)):
        form = forms[i]
        if form in ["10-K", "10-Q", "20-F"]:
            accession = accession_numbers[i].replace("-", "")
            primary_doc = primary_documents[i]
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{primary_doc}"

            results.append({
                "company": company_name,
                "ticker": ticker,
                "form": form,
                "date": dates[i],
                "url": filing_url
            })

        if len(results) >= 10:
            break

    return {"company": company_name, "ticker": ticker, "filings": results}


@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        ticker = request.form.get("ticker", "")
        data = get_company_filings(ticker)
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)