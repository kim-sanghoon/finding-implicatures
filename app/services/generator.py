from transformers import T5Tokenizer, T5ForConditionalGeneration
from typing import List

from app.utils.model_strings import make_input, convert_output
from app.core.settings import settings

class TextGenerator:
    def run_model(self, input_string: str, **generator_args) -> List[str]:
        input_ids = self.tokenizer.encode(input_string, return_tensors="pt")
        res = self.model.generate(input_ids, **generator_args)
        return self.tokenizer.batch_decode(res, skip_special_tokens=True)

    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained(settings.base_model)
        self.model = T5ForConditionalGeneration.from_pretrained(settings.base_model)
        self.model.eval()
    
    def predict(self, query: str) -> str:
        input_string = make_input(query)
        result = self.run_model(input_string)

        return convert_output(result[0])
