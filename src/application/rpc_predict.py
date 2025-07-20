from jsonrpc import dispatcher, JSONRPCResponseManager
from flask.views import View
from flask import request
from werkzeug.wrappers import Response

from src.domain.model_predict import MatchProbability

predict = MatchProbability().predict


@dispatcher.add_method
def candidate_match(vaga_data: dict, curriculo_text: str):
    probability = predict(vaga_data=vaga_data, curriculo_text=curriculo_text)
    return {'probabilidade de match': round(probability * 100, 2)}


class RpcPredict(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        dispatcher["ping"] = lambda: "pong"

        try:
            response = JSONRPCResponseManager.handle(request.data, dispatcher)
        except Exception as e:
            raise e

        return Response(response.json, mimetype='application/json')
