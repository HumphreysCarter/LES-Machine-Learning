# Environmental Analysis and Prediction of Lake-Effect Snow Events Downwind of Lake Ontario with Machine Learning

**Carter J. Humphreys**

Email: [chumphre@oswego.edu](mailto:chumphre@oswego.edu) | GitHub:[@HumphreysCarter](https://github.com/HumphreysCarter) | Website: [carterhumphreys.com](http://carterhumphreys.com/)

## About
Prediction of lake-effect snow (LES) storms prove significant challenges for forecasters, particularly with intensity and positioning of LES bands. High-resolution mesoscale modeling improves upon the predictability of LES position and intensity, however seemingly subtle fluctuations in the atmospheric characteristics of these intense mesoscale snow bands have profound effects on the storm total precipitation. With advancements in computing, particularly with the development of machine learning and neural networks, connections between environmental conditions and LES band characteristics can be made. This research investigated band position and intensity of warning-level LES events occurring downwind of Lake Ontario in upstate New York.

A 40-case dataset of LES events from the 2015-2016 to 2019-2020 winter seasons that either had a Lake Effect Snow Warning in effect or warning-level snowfall was observed (a maximum snowfall report of at least 7” [17.8 cm] was used as a proxy for warning criteria) was constructed using NWS Storm Data and a text archive of NWS warnings. Hourly environmental conditions from various BUFKIT stations near Lake Ontario were compiled for each case. These conditions were then matched with band position (latitude and longitude coordinates) and radar reflectivity factor from nearby National Weather Service (NWS) radars. Several machine learning schemes were implemented on the dataset using scikit-learn to link environmental conditions to band position.

The results of this model demonstrate the ability for LES prediction using machine learning techniques to improve upon the guidance provided by operation forecast models and provide additional guidance for forecasters.

## Installation
```
git clone https://github.com/HumphreysCarter/LES-Machine-Learning.git
```

## Dependencies
* Python 3.7
* scikit-learn-0.23.2
* joblib-0.17.0
* MetPy
* arm_pyart
* cartopy
