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
    choices_str = "\\n (A) low air quality (B) low humidity (C) low brightness (D) low noise level (E) low security (F) low temperature (G) high air quality (H) high humidity (I) high brightness (J) high noise level (K) high security (L) high temperature"
    query_str = 'A man said {}. Which of the followings is the problem of the man? '.format(input_str) + choices_str

    ret = run_model(query_str)[0]

    return jsonify({'predict': ret_dict[ret]})
