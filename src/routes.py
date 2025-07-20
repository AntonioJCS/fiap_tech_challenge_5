from flask import current_app as app
from src.application.rpc_predict import RpcPredict

app.add_url_rule('/predict/', view_func=RpcPredict.as_view('rpc_predict'))
