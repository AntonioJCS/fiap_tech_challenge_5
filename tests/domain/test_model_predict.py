from unittest.mock import patch
from src.domain.model_predict import MatchProbability


@patch("src.domain.model_predict.model")
@patch("src.domain.model_predict.vectorizer")
def test_predict_retorna_probabilidade_valida(mock_vectorizer, mock_model):
    # Mock do TF-IDF e modelo
    mock_vectorizer.transform.return_value = "vetor"
    mock_model.predict_proba.return_value = [[0.3, 0.7]]  # Classe 1 (match) com 70%

    predictor = MatchProbability()

    vaga_data = {
        "titulo_vaga": "Desenvolvedor Python",
        "principais_atividades": "Construir APIs REST",
    }
    curriculo = "Tenho experiência com Django e Flask."

    prob = predictor.predict(vaga_data, curriculo)

    assert prob == 0.7
    mock_vectorizer.transform.assert_called_once()
    mock_model.predict_proba.assert_called_once()


@patch("src.domain.model_predict.model")
@patch("src.domain.model_predict.vectorizer")
def test_predict_retorna_zero_se_texto_vazio(mock_vectorizer, mock_model):
    predictor = MatchProbability()

    vaga_data = {}
    curriculo = ""

    prob = predictor.predict(vaga_data, curriculo)
    assert prob == 0.0

    mock_vectorizer.transform.assert_not_called()
    mock_model.predict_proba.assert_not_called()


@patch("src.domain.model_predict.model")
@patch("src.domain.model_predict.vectorizer")
def test_predict_limpa_e_combine_texto(mock_vectorizer, mock_model):
    # Testa se combina corretamente os textos pré-processados
    mock_vectorizer.transform.return_value = "vetor"
    mock_model.predict_proba.return_value = [[0.1, 0.9]]

    predictor = MatchProbability()

    # A entrada aqui importa pouco porque o preprocess_text é real
    vaga_data = {
        "titulo_vaga": "Desenvolvedor",
        "principais_atividades": "codar coisas"
    }
    curriculo = "gosto de programar"

    prob = predictor.predict(vaga_data, curriculo)
    assert 0 <= prob <= 1
