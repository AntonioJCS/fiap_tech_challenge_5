from unittest.mock import patch
from src.domain.data_processor import preprocess_text, combine_vaga_info


@patch('src.domain.data_processor.word_tokenize')
@patch('src.domain.data_processor.stopwords.words')
def test_preprocess_text_removes_stopwords_and_punctuation(mock_stopwords, mock_tokenize):
    text = "Olá, esta é uma frase de teste!"
    mock_tokenize.return_value = ['olá', 'esta', 'frase', 'teste']
    mock_stopwords.return_value = ['esta', 'é', 'uma', 'de']

    result = preprocess_text(text)

    assert result == 'olá frase teste'
    mock_tokenize.assert_called_once()
    mock_stopwords.assert_called_once_with('portuguese')


def test_preprocess_text_handles_non_string():
    assert preprocess_text(None) == ''
    assert preprocess_text(123) == ''
    assert preprocess_text('   ') == ''


def test_combine_vaga_info_completo():
    row = {
        'titulo_vaga': 'Engenheiro',
        'principais_atividades': 'Desenvolver sistemas',
        'competencia_tecnicas_e_comportamentais': 'Python',
        'tipo_contratacao': 'CLT',
        'vaga_especifica_para_pcd': 'Não',
        'nivel profissional': 'Sênior',
        'nivel_academico': 'Superior completo',
        'nivel_ingles': 'Intermediário'
    }
    result = combine_vaga_info(row)
    assert result == 'Engenheiro Desenvolver sistemas Python CLT Não Sênior Superior completo Intermediário'


def test_combine_vaga_info_parcial():
    row = {
        'titulo_vaga': 'Engenheiro',
        'principais_atividades': 'Desenvolver sistemas'
    }
    result = combine_vaga_info(row)
    assert 'Engenheiro Desenvolver sistemas' in result
    assert len(result.split()) >= 2  # Deve conter ao menos os campos preenchidos


def test_combine_vaga_info_com_campos_vazios():
    row = {}
    result = combine_vaga_info(row)
    assert result == ' ' * 7  # São 8 campos esperados => 7 espaços
