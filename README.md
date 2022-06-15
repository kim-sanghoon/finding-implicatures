# Finding Implicatures from User Utterances

This application aims to find implicatures from user utterances in smart home environments.<br />
According to the [smart home ontology](http://elite.polito.it/ontologies/eupont.owl) proposed by Corno et al., there are six categories of environment properties in a smart home: air quality, brightness, humidity, noise level, security, and temperature.<br />
Powered by the [Google T5 large model pretrained with UnifiedQA dataset](https://github.com/allenai/unifiedqa), this application returns if exactly one of these properties is too low or high.
That is, the output of the application is one of the followings: `LowAirQuality`, `LowBrightness`, `LowHumidity`, `LowNoise`, `LowSecurity`, `LowTemperature`, `HighAirQuality`, `HighBrightness`, `HighHumidity`, `HighNoise`, `HighSecurity`, or `HighTemperature`.

## Starting the application

Before you start the application, please configure the environment variables on `.env` file.

| Environment Variable | Description |
|----------------------|-------------|
| `BASE_MODEL`         | The base language model for the application. |
| `PORT`               | The port number for the application. |
| `CACHE_DIR`          | The cache directory of the huggingface transformers library. |

The easiest way to prepare the application is to use Docker.
The following command will create a Docker image.

```bash
docker-compose -f docker/Dockerfile --env-file ./.env build
```

After the build is complete, please run the following command to execute the application.

```bash
docker-compose -f docker/Dockerfile --env-file ./.env up
```

The application could take some time (possibly < 1 min.) to initialize the NLP model.
It could take much longer time for the first run because the application downloads required cache files.

## Outputs

Predicted implicatures will be returned in JSON format, with `predict` field. For example, the response for the following request,
```
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"query": "I feel vulnerable in this room"}' \
  localhost:8000
```
should return the response of `{"predict": "LowSecurity"}` (assuming that the `PORT` is set to 8000).

## Samples

Here are some sample inputs and outputs with `BASE_MODEL="allenai/unifiedqa-t5-large"`.

| Input | Output |
|-------|--------|
| The wind from the air conditioner is not that chilling. | HighTemperature |
| The room condition makes me sweat. | HighHumidity |
| Feeling like someone is here. | LowSecurity |
| I think the room is too bright now. | HighBrightness |
| I want to breathe some fresh air. | LowAirQuality |
| The sound is irritating me. | HighNoise |

## Limitations

It is surprising that the NLP model works quite well without any fine-tuning.
However, the application will not properly working with some inputs, such as

- Input: "Where did the sound come from"
    - Expected Output: HighNoise
    - Actual Output: LowNoise
- Input: "I feel that I have to wear a mask"
    - Expected Output: LowAirQuality
    - Actual Output: HighSecurity
- Input: "The air is so soggy"
    - Expected Output: HighHumidity
    - Actual Output: LowHumidity
