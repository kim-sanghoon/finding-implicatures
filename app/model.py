from transformers import T5Tokenizer, T5ForConditionalGeneration

class UnifiedQA:
    base_model = "allenai/unifiedqa-t5-large"
    ret_dict = {
        'low air quality': 'LowAirQuality',
        'low humidity': 'LowHumidity',
        'low brightness': 'LowBrightness',
        'low noise level': 'LowNoise',
        'low security': 'LowSecurity',
        'low temperature': 'LowTemperature',
        'high air quality': 'HighAirQuality',
        'high humidity': 'HighHumidity',
        'high brightness': 'HighBrightness',
        'high noise level': 'HighNoise',
        'high security': 'HighSecurity',
        'high temperature': 'HighTemperature'
    }

    def run_model(self, input_string: str, **generator_args) -> list[str]:
        input_ids = self.tokenizer.encode(input_string, return_tensors="pt")
        res = self.model.generate(input_ids, **generator_args)
        return self.tokenizer.batch_decode(res, skip_special_tokens=True)

    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained(self.base_model)
        self.model = T5ForConditionalGeneration.from_pretrained(self.base_model)
        self.model.eval()
    
    def predict(self, query: str) -> str:
        input_str = query
        choices_str = "\\n (A) low air quality (B) low humidity (C) low brightness (D) low noise level (E) low security (F) low temperature (G) high air quality (H) high humidity (I) high brightness (J) high noise level (K) high security (L) high temperature"
        query_str = f"A man said {input_str}. Which of the followings is the problem of the man? {choices_str}"

        ret = self.run_model(query_str)[0]
        return self.ret_dict[ret]
