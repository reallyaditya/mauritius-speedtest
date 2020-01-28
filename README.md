# Mauritius Internet Speed Test

The aim of this project is to provide a simple python script to make several speedtests using the Speedtest-cli from Ookla and then return the result as a JSON file.

This script is currently being used to fetch data for the project below:

**[View the Live Website](https://mrsunshyne.github.io/mauritius-sea-cable/)**

## Data Source

The data source is in the following format:

```json
// file: all-servers.json
{
    "LION": "<SpeedtestResult>",
    "SAFE1": "<SpeedtestResult>",
    "SAFE2": "<SpeedtestResult>",
    "SAFE3": "<SpeedtestResult>",
    "MARS": "<SpeedtestResult>"
}
// Where Speedtest result has the following signature
Interface SpeedtestResult {
    "timestamp": "",
    "upload": "",
    "download": "",
    "ping": ""
}
```

## Project Dependencies

- Python 3
- Official Speedtest-cli from [Ookla](https://www.speedtest.net/apps/cli)

## Project setup

- Fork this repo to your account

- Git clone the fork to your local machine

- Having cloned the repo, change the path of the project directory accordingly in the `config.json` script.

```json
{
  "projectPath": "{insert path here}"
}
```

- Just run the script to make speedtests and gather results.

```bash
python3 speedtest.py
```

- Change the speed test server codes to the ones you want in `/data/servers.json`

```json
{
  "LION": { "madagascar": 7755 },
  "SAFE": { "india": 24682, "south_africa": 1285, "malaysia": 12544 },
  "MARS": { "rodrigues": 27454 }
}
```

- You can get a list of nearby speed test servers and their codes by running the command below:

```bash
speedtest --servers
```
