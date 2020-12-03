from transformers import T5Config, T5Tokenizer, T5ForConditionalGeneration
from transformers.modeling_t5 import load_tf_weights_in_t5
from flask import Flask, request, jsonify

app = Flask(__name__)

base_model = "t5-large"
tokenizer = T5Tokenizer.from_pretrained(base_model)
model = T5ForConditionalGeneration(T5Config.from_pretrained(base_model))

load_tf_weights_in_t5(model, None, "/data/")
model.eval()

ret_dict = {
    'too low air quality': 'LowAirQuality',
    'too low humidity': 'LowHumidity',
    'too low brightness': 'LowBrightness',
    'too low noise level': 'LowNoise',
    'too low security': 'LowSecurity',
    'too low temperature': 'LowTemperature',
    'too high air quality': 'HighAirQuality',
    'too high humidity': 'HighHumidity',
    'too high brightness': 'HighBrightness',
    'too high noise level': 'HighNoise',
    'too high security': 'HighSecurity',
    'too high temperature': 'HighTemperature'
}


def run_model(input_string, **generator_args):
    input_ids = tokenizer.encode(input_string, return_tensors="pt")
    res = model.generate(input_ids, **generator_args)
    return [tokenizer.decode(x) for x in res]


@app.route('/', methods=['POST'])
def main():
    req = request.get_json()
    
    if req is None or 'query' not in req:
        return jsonify({'predict': None, 'error': 'Query not found.'})
    
    input_str = req['query']
    choices_str = "\\n (A) too low air quality (B) too low humidity (C) too low brightness (D) too low noise level (E) too low security (F) too low temperature (G) too high air quality (H) too high humidity (I) too high brightness (J) too high noise level (K) too high security (L) too high temperature"
    query_str = 'The man felt uncomfortable in this room, and said "{}." Which of the following room conditions made the man uncomfortable? '.format(input_str) + choices_str

    ret = run_model(query_str)[0]

    return jsonify({'predict': ret_dict[ret]})
