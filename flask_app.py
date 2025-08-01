from flask import Flask, request, jsonify
import requests
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return "IR Bank API is up and running!"

@app.route("/irbank/financial", methods=["GET"])
def get_financial():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "code parameter is required"}), 400

    # IRバンク通期損益データ取得
    url = "https://irbank.net/download/fy-profit-and-loss.json"
    res = requests.get(url)
    res.raise_for_status()

    df = pd.DataFrame(res.json())
    matched = df[df["証券コード"].astype(str) == str(code)]

    return jsonify(matched.to_dict(orient="records"))

@app.route("/debug", methods=["GET"])
def debug():
    # JSON構造確認用のデバッグ用エンドポイント
    url = "https://irbank.net/download/fy-profit-and-loss.json"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    return jsonify({
        "columns": list(df.columns),
        "num_records": len(df),
        "sample_first_3": df.head(3).to_dict(orient="records")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
