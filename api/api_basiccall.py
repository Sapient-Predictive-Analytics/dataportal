# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 16:04:39 2024

@author: tom
"""
import pandas as pd
import os.path
import sys
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample time series data
modpath = os.path.dirname(os.path.abspath(sys.argv[0])) 
datapath = os.path.join(modpath, '../../dataportal/tokens/SNEK.csv') 
time_series_data = pd.read_csv(datapath)

@app.route('/data', methods=['GET'])
def get_data():
    date = request.args.get('date')
    if date in time_series_data:
        return jsonify({date: time_series_data[date]})
    else:
        return jsonify({"error": "Date not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)