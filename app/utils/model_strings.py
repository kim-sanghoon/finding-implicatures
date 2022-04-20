output_classes = {
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

def make_input(input_str: str) -> str:
    query = f"A man said {input_str}. Which of the followings is the problem of the man?"
    # choices = "(A) low air quality (B) low humidity (C) low brightness (D) low noise level (E) low security (F) low temperature (G) high air quality (H) high humidity (I) high brightness (J) high noise level (K) high security (L) high temperature"
    choices_list, i = [], 0

    for output_class in output_classes.keys():
        choices_list.append(f"({chr(65 + i)}) {output_class}")

    return query + ' \\n ' + " ".join(choices_list)

def convert_output(output_class: str) -> str:
    return output_classes[output_class]
