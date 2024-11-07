# spellcheck.py

import re
from nltk.tokenize import word_tokenize
from transformers import pipeline, AutoModelForMaskedLM, AutoTokenizer

class AdvancedSpellChecker:
    def __init__(self):
        # Load a pre-trained model for masked language modeling
        model_name = "bert-base-uncased"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForMaskedLM.from_pretrained(model_name)
        self.nlp_fill_mask = pipeline("fill-mask", model=self.model, tokenizer=self.tokenizer)

    def check_text(self, text):
        # Tokenize the text and check for misspelled words (simplified)
        words = word_tokenize(text)
        return words

    def get_corrections(self, text):
        # Process each word and suggest corrections based on context
        words = self.check_text(text)
        corrections = []

        for idx, word in enumerate(words):
            if not word.isalpha():  # Skip punctuation and non-alphabetic characters
                continue

            # Generate masked text to provide context-aware suggestions
            masked_text = text.replace(word, self.tokenizer.mask_token, 1)
            predictions = self.nlp_fill_mask(masked_text)

            # Collect suggestions for the masked word
            suggestions = [pred["token_str"] for pred in predictions[:3]]  # Top 3 suggestions

            if suggestions and word not in suggestions:
                corrections.append({
                    'word': word,
                    'context': masked_text,
                    'suggestions': suggestions
                })

        return corrections
