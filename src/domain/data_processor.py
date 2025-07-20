import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def preprocess_text(text):
    if not isinstance(text, str) or not text.strip():
        return ''
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('portuguese'))
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)


def combine_vaga_info(row):
    fields = ['titulo_vaga', 'principais_atividades', 'competencia_tecnicas_e_comportamentais', 'tipo_contratacao',
              'vaga_especifica_para_pcd', 'nivel profissional',	'nivel_academico', 'nivel_ingles']
    texts = [str(row.get(field, '')) for field in fields]
    return ' '.join(texts)
