# TSAG - Time Series Anomaly Generator
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/jetnew/tsag/blob/master/LICENSE.txt)

A time series anomaly generation tool for quickly generating anomalies in time series machine learning problems.

## Applications in Anomaly Detection

#### Model Evaluation

* The lack of labelled data severely hinders progress in anomaly detection development due to unreliable performance evaluation.
* TSAG generates different classes of anomalies to evaluate classification performance on different anomaly types.

#### Class Imbalance

* Many machine learning techniques require much anomalous training data to be sufficiently performant in anomaly classification.
* TSAG generates different types of anomalies, enabling Root Cause Analysis of detected anomalies.

### 

## Installation

```
pip install tsag
```

## Usage

#### Anomaly Template
```
# Create a reference template time series
n = 10
template = timeseries[:n]
```

#### Single Tranformation
```
from tsag import PointAnomaly

# Generate point anomaly
point_anomaly = PointAnomaly(template)
point_anomaly.plot()

# Insert generated anomaly into time series data
augmented_timeseries = point_anomaly.insert(timeseries, index=None)
```

#### Multiple Transformations

```
from tsag import FrequencyShiftAnomaly, AmplitudeShiftAnomaly, RangeShiftAnomaly, CompoundAnomaly

args = [
    # [Generator, {Arguments}],
    [FrequencyShiftAnomaly, {'ratio': 1/3}],
    [AmplitudeShiftAnomaly, {'ratio': 1/3}],
    [RangeShiftAnomaly, {'ratio': 1/2}],
]

# Generate compound anomaly
compound_anomaly = CompoundAnomaly(template, *args)
compound_anomaly.plot()

# Insert generated anomaly into time series data
augmented_timeseries = compound_anomaly.insert(template, index=None)
```