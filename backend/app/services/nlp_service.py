import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class NLPCleaningService:
    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))

        tokens = word_tokenize(text)

        stop_words = set(stopwords.words("english"))
        cleaned_tokens = [t for t in tokens if t not in stop_words]

        return " ".join(cleaned_tokens)
