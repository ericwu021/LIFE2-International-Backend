from flask import Flask,jsonify,request,render_template
from flask_cors import CORS
import datetime
from rank_support_module import *
import numpy as np
import os

app = Flask(__name__)
CORS(app)


@app.route("/get-time", methods=['GET'])
def index():
    data_output = {"value": str(datetime.datetime.now())}
    return jsonify(data_output)


@app.route("/rank", methods=['GET','POST'])
def receive_time():
  if request.method == 'POST':
    data_angular = str(request.data)[3:-2]
    data_angular = data_angular.replace('\"','')

    print (data_angular)
    cwid = data_angular.split(',')[0].upper()
    print (len(cwid),cwid)
    if (cwid == 'null') or (cwid == 'NULL') :
      cwid = 'VISITOR'

    start_date = data_angular.split(',')[1]
    df_outputs = score_cal_func(start_date,cwid)
    df_outputs = df_outputs.sort_values(by=['RANK'])

    df_outputs['SECONDS'] = df_outputs[['SECONDS']].applymap('{:,.6f}'.format)

    if cwid == 'VISITOR':
      df_outputs.loc[cwid,'CWID'] = '> NO CWID <'
      df_outputs.loc[cwid, 'RANK'] = '-'

    df_outputs.loc[df_outputs.CWID == cwid,'CWID'] = str('> ' + cwid + ' <')
    outputs = df_outputs.to_dict(orient='records')
    outputs = {"results": outputs}
    print (outputs)
    return jsonify(outputs)
