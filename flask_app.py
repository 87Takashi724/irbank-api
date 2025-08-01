from flask import Flask, jsonify, request
import requests
import pandas as pd
import io

app = Flask(__name__)

@app.route("/")
def index():
    return "IR Bank API サービス稼働中"

@app.route("/debug")
def debug():
    try:
        res = requests.get("https://irbank.net/download/fy-profit-and-loss.json")
        data = res.text  # JSONテキストのまま取得
        return jsonify({"raw": data[:200]})  # 先頭200文字だけ表示（全体が大きいので）
    except Exception as e:
        return jsonify({"error": str(e)}), 500

