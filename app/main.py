import ray
from ray import serve
from transformers import T5Tokenizer, T5ForConditionalGeneration
from starlette.responses import JSONResponse

ray.init(address="auto", namespace="serve")
serve.start()

base_model = "allenai/unifiedqa-t5-large"
tokenizer = T5Tokenizer.from_pretrained(base_model)
model = T5ForConditionalGeneration.from_pretrained(base_model)

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


def run_model(input_string: str, **generator_args):
    input_ids = tokenizer.encode(input_string, return_tensors="pt")
    res = model.generate(input_ids, **generator_args)
    return tokenizer.batch_decode(res, skip_special_tokens=True)


@serve.deployment
def main(request):
    input_str = request.query_params['query']
    choices_str = "\\n (A) low air quality (B) low humidity (C) low brightness (D) low noise level (E) low security (F) low temperature (G) high air quality (H) high humidity (I) high brightness (J) high noise level (K) high security (L) high temperature"
    query_str = f"A man said {input_str}. Which of the followings is the problem of the man? {choices_str}"

    ret = run_model(query_str)[0]

    return JSONResponse({'predict': ret_dict[ret]})

main.deploy()