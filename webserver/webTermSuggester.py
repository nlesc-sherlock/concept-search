#!/usr/bin/env python
################################################################################
#    Created by Oscar Martinez                                                 #
#    o.rubi@esciencecenter.nl                                                  #
################################################################################
from flask import Flask, Response, request, jsonify
from TermSuggester import TermSuggester, SearchMethodAggregation
from elsearch import ELSearch
from wnsearch import WNSearch
import MakeChart

app = Flask(__name__)

searchMethodClasses = (ELSearch, WNSearch)
initializeParameters = ((None, False),([]))
ts = TermSuggester(searchMethodClasses, initializeParameters)

@app.route('/')
def api_root():
    return 'Welcome to TermSuggester Web API'

@app.errorhandler(404)
def api_error(error=None):
    message = {
            'status': 404,
            'message': 'Error: ' + error,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route("/suggester", methods = ['GET',])
def api_term():
    if request.method == 'GET':
        if 'term' in request.args:
            if 'agg-method' in request.args:
                aggMethod = str(request.args['agg-method']).strip()
                if aggMethod == 'sum':
                    aggMethod = SearchMethodAggregation.SumMethod
                elif aggMethod == 'average':
                    aggMethod = SearchMethodAggregation.AverageMethod
                else:
                    return api_error('specify correct aggregation method: sum or average')
            else:
                # Default aggragation method
                aggMethod = SearchMethodAggregation.SumMethod
            
            if 'methods' in request.args:
                try:
                    methods = str(request.args['methods']).split(',')
                    for i in range(len(methods)):
                        methods[i] = int(methods[i])
                except:
                    return api_error('specify correct method. Example: 1,2')
            else:
                methods = None
            data = ts.getSuggestions(str(request.args['term']), aggMethod, methods)
            resp = Response(MakeChart.dict2bar(data), status=200, mimetype='application/json')
            return resp
        else:
            return api_error('a term is required')




if __name__ == "__main__":
    app.run(debug=True)