import nltk
from src.infra.models.load_model import load_model
from src.domain.data_processor import preprocess_text, combine_vaga_info

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

model, vectorizer = load_model()


class MatchProbability:

    def __init__(self):
        self.preprocess_text = preprocess_text
        self.combine_vaga_info = combine_vaga_info

    def predict(self, vaga_data: dict, curriculo_text: str) -> float:
        # Preparar features
        vaga_text = self.preprocess_text(self.combine_vaga_info(vaga_data))
        curriculo_text = self.preprocess_text(curriculo_text)
        combined_text = vaga_text + ' ' + curriculo_text

        # Verificar se há texto válido
        if not combined_text.strip():
            return 0.0

        # Transformar em vetores TF-IDF
        X = vectorizer.transform([combined_text])

        # Prever probabilidade
        probability = model.predict_proba(X)[0][1]  # Probabilidade da classe positiva (match)
        return probability
