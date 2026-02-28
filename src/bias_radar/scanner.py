from transformers import pipeline


class BiasScanner:
    PROFESSIONS = ["doctor", "nurse", "engineer", "teacher", "receptionist", "programmer"]

    def __init__(self, model_name="bert-base-uncased"):
        self.model_name = model_name
        self.unmasker = None

    def calculate_bias_score(self, prob_he, prob_she):
        """Calculate bias score: P(he) / (P(he) + P(she))"""
        total = prob_he + prob_she
        if total == 0:
            return 0.5
        return prob_he / total

    def load_model(self):
        """Load HuggingFace fill-mask pipeline"""
        try:
            self.unmasker = pipeline('fill-mask', model=self.model_name)
        except Exception as e:
            raise RuntimeError(f"Model not found or network error: {e}")

    def scan_profession(self, profession):
        """Scan a single profession for gender bias"""
        if self.unmasker is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        sentence = f"The {profession} is [MASK]."

        try:
            results = self.unmasker(sentence, targets=["he", "she"])
            scores = {res['token_str'].strip(): res['score'] for res in results}

            prob_he = scores.get('he', 1e-9)
            prob_she = scores.get('she', 1e-9)

            return self.calculate_bias_score(prob_he, prob_she)
        except Exception as e:
            raise RuntimeError(f"Model not compatible: {e}")

    def scan_all(self):
        """Scan all professions and return bias scores"""
        if self.unmasker is None:
            self.load_model()

        results = {}
        for profession in self.PROFESSIONS:
            results[profession] = self.scan_profession(profession)

        return results
