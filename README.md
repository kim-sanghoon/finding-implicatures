# Finding Implicatures from User Utterances

This application aims to find implicatures from user utterances in smart home environments.<br />
According to the [smart home ontology](http://elite.polito.it/ontologies/eupont.owl) proposed by Corno et al., there are six categories of environment properties in a smart home: air quality, brightness, humidity, noise level, security, and temperature.<br />
This application returns if exactly one of these properties is too low or high.
That is, the output of the application is one of the followings: `LowAirQuality`, `LowBrightness`, `LowHumidity`, `LowNoise`, `LowSecurity`, `LowTemperature`, `HighAirQuality`, `HighBrightness`, `HighHumidity`, `HighNoise`, `HighSecurity`, or `HighTemperature`.

## Preparing the application

This application uses the [Google T5 large model pretrained with UnifiedQA dataset](https://github.com/allenai/unifiedqa).<br />
Please download the model checkpoint files and locate them in `/data` directory.
There should be five files in the directory as follows:
```
/data
  checkpoint
  model.ckpt-1120700.data-00000-of-00002
  model.ckpt-1120700.data-00001-of-00002
  model.ckpt-1120700.index
  model.ckpt-1120700.meta
```

After the files are ready, you have to build the container to execute the application.<br />
Please type `sudo docker build -t implicature .` to build.

## Starting the application

To start the application after the container is successfully built, please type `sudo ./run-docker.sh`.

- It will execute the application in the background. If you want to check the application in the foreground, modify the argument `-d` to `-it` in the line 4 of the `run-docker.sh` file.
- The default port of the application is set to 444. If you want to access the application in the other port, modify the first 444 to the other numbers (such as 80, 443, etc.) in the line 10 of the `run-docker.sh` file.

The application could take some time (possibly < 1 min.) to initialize the NLP model. Currently, it takes about 10 sec. on my machine.<br />
It could take much longer for the first initialization because the application downloads required cache files.

## Outputs

Predicted implicatures will be returned in JSON format, with `predict` field. For example, the response for the following request,
```
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"query": "I feel vulnerable in this room"}' \
  localhost:444
```
should return the response of `{"predict": "LowSecurity"}`.

If the request does not contain any query string, it would return `null`.

## Samples

Here are some sample inputs and outputs.

| Input | Output |
|-------|--------|
| The wind from the air conditioner is not that chilling. | HighTemperature |
| The room condition makes me sweat. | HighHumidity |
| Feeling like someone is here. | LowSecurity |
| I think the room is too bright now. | HighBrightness |
| I want to breathe some fresh air. | LowAirQuality |

## Limitations

It is surprising that the NLP model works quite well without any fine-tuning.
However, the application will not properly working with confusing inputs, such as

- Input: "Where did the sound come from"
    - Expected Output: HighNoise
    - Actual Output: LowNoise
- Input: "I feel that I have to wear a mask"
    - Expected Output: LowAirQuality
    - Actual Output: HighSecurity

