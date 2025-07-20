import pytest
from unittest import mock
from src.infra.models.load_model import load_model


@mock.patch("src.infra.models.load_model.joblib.load")
def test_load_model_returns_model_and_vectorizer(mock_joblib_load):
    # Mock dos objetos que seriam carregados
    mock_model = mock.Mock()
    mock_vectorizer = mock.Mock()

    # Definir a ordem de retorno do joblib.load
    mock_joblib_load.side_effect = [mock_model, mock_vectorizer]

    model, vectorizer = load_model()

    assert model == mock_model
    assert vectorizer == mock_vectorizer
    assert mock_joblib_load.call_count == 2


@mock.patch("src.infra.models.load_model.joblib.load")
def test_load_model_raises_if_file_missing(mock_joblib_load):
    # Simula erro ao carregar arquivo
    mock_joblib_load.side_effect = FileNotFoundError("Arquivo não encontrado")

    with pytest.raises(FileNotFoundError):
        load_model()
