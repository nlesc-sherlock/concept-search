#!/usr/bin/env python
################################################################################
#    Created by Oscar Martinez                                                 #
#    o.rubi@esciencecenter.nl                                                  #
################################################################################
import traceback
from flask import Flask, Response, request, jsonify
from flask.ext.cors import CORS, cross_origin
from TermSuggestionsAggregator import TermSuggestionsAggregator, Aggregation
from elsearch import ELSearch
from wnsearch import WNSearch
import MakeChart

app = Flask(__name__)
CORS(app)

methodsConfigurationDict = {1: (WNSearch, ()),
                            2: (ELSearch, ())}
methodsInstances = {}
for mKey in methodsConfigurationDict:
    methodsInstances[mKey] = methodsConfigurationDict[mKey][0](*methodsConfigurationDict[mKey][1])
ts = TermSuggestionsAggregator()

@app.route('/')
def api_root():
    m = {}
    for methodKey in sorted(methodsConfigurationDict.keys()):
        m[methodKey ] = (methodsConfigurationDict[methodKey][0].__name__, methodsConfigurationDict[methodKey][1])
    return jsonify(m)

@app.errorhandler(404)
@cross_origin(supports_credentials=True)
def api_error(error=None):
    message = {
            'status': 404,
            'message': 'Error: ' + error,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route("/suggester", methods = ['GET',])
@cross_origin(supports_credentials=True)
def api_term():
    if request.method == 'GET':
        if 'term' in request.args:
            if 'agg-method' in request.args:
                aggMethod = str(request.args['agg-method']).strip()
                if aggMethod == 'sum':
                    aggMethod = Aggregation.Sum
                elif aggMethod == 'average':
                    aggMethod = Aggregation.Average
                else:
                    return api_error('specify correct aggregation method: sum or average')
            else:
                # Default aggragation method
                aggMethod = Aggregation.Sum

            if 'methods' in request.args:
                try:
                    methods = []
                    methodsKeys = str(request.args['methods']).split(',')
                    for methodKey in methodsKeys:
                        methods.append(methodsInstances[int(methodKey)])
                except Exception, err:
                    return api_error('specify correct method. Example: 1,2\n' + traceback.format_exc())
            else:
                methods = methodsInstances.values()
            
            # Get the suggestions
            data = ts.getSuggestions(str(request.args['term']), methods, aggMethod)
            resp = Response(MakeChart.dict2bar(data), status=200, mimetype='application/json')
            return resp
        else:
            return api_error('a term is required')




if __name__ == "__main__":
    app.run(debug=True)