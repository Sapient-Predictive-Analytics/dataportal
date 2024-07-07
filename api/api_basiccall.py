# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 16:04:39 2024

@author: tom
"""
import pandas as pd
import os.path
import sys
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Time Series API',
          description='A simple Time Series API')

ns = api.namespace('data', description='Time series operations')

# Sample time series data
modpath = os.path.dirname(os.path.abspath(sys.argv[0])) 
datapath = os.path.join(modpath, '../../dataportal/tokens/SNEK.csv') 
# Read CSV file into a DataFrame
time_series_data = pd.read_csv('data.csv')
time_series_data.set_index('date', inplace=True)

date_model = api.model('DateModel', {
    'date': fields.String(required=True, description='The date'),
})

@ns.route('/')
class DataResource(Resource):
    @api.doc(params={'date': 'The date for the data'})
    @api.response(200, 'Success')
    @api.response(404, 'Date not found')
    def get(self):
        """Fetch the data for a given date"""
        date = request.args.get('date')
        if date in time_series_data:
            return jsonify({date: time_series_data[date]})
        else:
            return jsonify({"error": "Date not found"}), 404
        
@app.route('/data', methods=['GET'])
def get_data():
    date = request.args.get('date')
    if date in time_series_data:
        return jsonify({date: time_series_data[date]})
    else:
        return jsonify({"error": "Date not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)