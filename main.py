import os
import json
import logging

from numpy import true_divide
import loggingHelper as lh
from storagehelper import StorageHelper
from flask import Flask, jsonify, request, Response
from performancestatistics import PerformanceStatistics


app = Flask(__name__)
debug_str = os.environ.get('DEBUG')
if debug_str is None or debug_str == "":
    isDebug = False
else:
    if debug_str.lower() == "true":
        isDebug = True
    else:
        isDebug = False
print ("isDebug = " + str(isDebug))
app.config["DEBUG"] = isDebug


def configure():
    print('Service starting')
    lh.configure()

    logger = logging.getLogger("analytics")
    logger.setLevel(logging.DEBUG)    
    logger.debug("Logging configured")

@app.route('/', methods=['GET'])
def home():
    resp = Response("<h1>Welcome to Performance Analytics</h1>",
        headers={"Access-Control-Allow-Origin": "*"},
        content_type="text/html",
        status=200
    )
    return resp

@app.route('/health', methods=['GET'])
def health():
    resp = Response("OK",
        headers={"Access-Control-Allow-Origin": "*"},
        content_type="text/html",
        status=200
    )
    return resp

@app.errorhandler(404)
def page_not_found(e):
    resp = Response("",
        headers={"Access-Control-Allow-Origin": "*"},
        status=404
    )
    return resp

@app.route('/devices/data', methods=['POST'])
def getData():
    body = PerformanceStatistics.getDataAsJson()
    dump = json.dumps(body)
    resp = Response(dump,
        headers={"Access-Control-Allow-Origin": "*"},
        content_type="application/json",
        status=200
    )

    return resp

@app.route('/devices/stats', methods=['POST'])
def getStats():

    if request.content_type == "application/json":
        #payload = request.get_json()
        summary_all, stats_all, summary_rng, stats_rng = PerformanceStatistics.getStatsAsJson()
        body = {}
        body['summary_all'] = summary_all
        body['stats_all'] = stats_all
        body['summary_rng'] = summary_rng
        body['stats_rng'] = stats_rng
        dump = json.dumps(body)
        resp = Response(dump,
            headers={"Access-Control-Allow-Origin": "*"},
            content_type="application/json",
            status=200
        )

        return resp
    else:
        body = PerformanceStatistics.getStatsAsText()
        resp = Response(body,
            headers={"Access-Control-Allow-Origin": "*"},
            content_type="text/html",
            status=200
        )

        return resp

@app.route('/devices', methods=['DELETE'])
def delete():
    results = StorageHelper.flushAll()
    body = {}
    body["ids"] = results
    dump = json.dumps(body)
    resp = Response(dump,
        headers={"Access-Control-Allow-Origin": "*"},
        content_type="application/json",
        status=200
    )
    return resp

# @app.route('/devices/ids', methods=['GET'])
# def getDevicesId():
#     return "GET All Devices Id", 200

# @app.route('/devices/<string:name>/location')
# def getDeviceLocation(name):
#     return "GET Device Location", 200

def create_app():
   return app

if __name__ == "__main__":
    configure()
    app.run(host='0.0.0.0', port=5972)

