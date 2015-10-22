#!/usr/bin/env python
################################################################################
#    Created by Oscar Martinez                                                 #
#    o.rubi@esciencecenter.nl                                                  #
################################################################################
from flask import Flask, request, jsonify
from flask.ext.cors import CORS
from TermSuggester import TermSuggester, SearchMethodAggregation
from elsearch import ELSearch
from wnsearch import WNSearch

app = Flask(__name__)
CORS(app)

searchMethodClasses = (ELSearch, WNSearch)
initializeParameters = ((None, False),([]))
ts = TermSuggester(searchMethodClasses, initializeParameters)

@app.route("/suggester", methods = ['GET',])
def api_term():
    if request.method == 'GET':
        if 'term' in request.args:
            data = ts.getSuggestions(str(request.args['term']), SearchMethodAggregation.SumMethod)
            resp = jsonify(data)
            resp.status_code = 200
            return resp
        else:
            return 'Error: Need to specif a term!'




if __name__ == "__main__":
    app.run(debug=True)
