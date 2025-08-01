from flask import Flask, jsonify
from irbank_scraper import get_financial_data

app = Flask(__name__)

@app.route('/')
def index():
    return 'IR Bank Financial API is running'

@app.route('/api/financials/<code>')
def get_financials(code):
    data = get_financial_data(code)
    return jsonify(data)

