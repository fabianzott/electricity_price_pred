# electricty_price_pred

## Introduction

`electricty_price_pred` is a machine learning project aimed at predicting the electricity spot prices in Germany for the next day (Day-Ahead Price, 15-min intervals) utilizing an array of data sources, including net electricity generation figures from Germany, commodity prices, weather conditions, economic indicators, and information pertaining to events like public holidays.

Key data sources for this project encompass the Fraunhofer Institute for Solar Energy Systems (Fraunhofer-Institut für Solare Energiesysteme ISE), the Federal Statistical Office of Germany (Statistisches Bundesamt), and publicly available weather data.

The project's fundamental approach involves retrieving data stored on Google BigQuery. This data then undergoes a series of processing steps, including preprocessing, scaling, and the application of various machine learning models for training. The ultimate goal is to forecast future electricity prices in Germany with a model that can integrate real-time data updates to improve prediction accuracy.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Dependencies](#dependencies)
5. [Configuration](#configuration)
6. [Documentation](#documentation)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)
9. [Contributors](#contributors)
10. [License](#license)


## Features

- Integration with Google BigQuery for data handling.
- Comprehensive data sources including electricity generation, commodity prices, weather, economic indicators, and event/holiday data.
- Evaluation of Machine Learning models for accurate Day-Ahead price predictions.

## Dependencies

The project relies on several Python libraries, as listed in the `requirements.txt` file:

- `pandas_gbq`
- `google.cloud`
- `pytest`
- `seaborn`
- `numpy` (version 1.23.5)
- `pandas` (version 1.5.3)
- `scipy` (version 1.10.0)
- `scikit-learn` (version 1.3.1)
- `google-cloud-bigquery`

## Contributors

- Fabian Zott
- Nepomuk Mylius
- Oleksandr Orlov

## License

The license for this project will be determined and added at a later stage.

---

This README is a preliminary draft and will be updated as the `electricty_price_pred` project progresses. For any further information or updates, please refer to the project repository on GitHub.
