import json
import pytest
from unittest.mock import patch
from flask import Flask

from src.application.rpc_predict import RpcPredict, candidate_match


@patch("src.application.rpc_predict")
def test_scikit_learn_retorna_probabilidade(mock_predict):
    mock_predict.return_value = 0.7234

    vaga_data = {"titulo_vaga": "Engenheiro"}
    curriculo_text = "Experiência com Python"

    result = candidate_match(vaga_data, curriculo_text)

    assert "probabilidade de match" in result
    assert result["probabilidade de match"] == 95.33


@pytest.fixture
def client():
    app = Flask(__name__)
    app.add_url_rule('/rpc', view_func=RpcPredict.as_view('rpc_predict'))
    return app.test_client()


@patch("src.application.rpc_predict")
def test_rpc_predict_endpoint(mock_predict, client):
    mock_predict.return_value = 0.55

    payload = {
        "jsonrpc": "2.0",
        "method": "candidate_match",
        "params": {
            "vaga_data": {"titulo_vaga": "Desenvolvedor"},
            "curriculo_text": "Experiência com Django"
        },
        "id": 1
    }

    response = client.post('/rpc', data=json.dumps(payload), content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)

    assert "result" in data
    assert data["result"] == {"probabilidade de match": 86.33}
    assert data["id"] == 1


def test_ping_endpoint(client):
    payload = {
        "jsonrpc": "2.0",
        "method": "ping",
        "params": [],
        "id": 99
    }

    response = client.post('/rpc', data=json.dumps(payload), content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)

    assert data["result"] == "pong"
    assert data["id"] == 99
