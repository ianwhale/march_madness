# CSE802 Project

This is a project focused on predicting the outcome of the NCAA Tournament using past regular season data.

# Description of Experiments

#### Adaboost

See `adaboost.py`. The properties of the Adaboost algorithm allow us to easily determine the most
important features to prediction with this simple ensemble method. 

#### Correlation

See `cov_plot.py`. A simple exploration into the correlation of our feature set.

#### Ensemble Tournnament Scoring

See `ensemble_serial.py`. This script uses the ensemble methods trained in `adaboost.py` and
`random_forest.py` to predict the 2017 NCAA Tournament in serial. Meaning, the games are predicted
in their tournament format as if we were building a bracket.

#### Principal Component Analysis

See `pca.py`. We compute and plot the two largest principal components.
Surprisingly, 99.8% of the variance in the data is account for by these two components.

#### Random Forest

See `random_forest.py`. With a bit more extra computation, the feature importances
can be calculated using the average out of bag error of each feature. Luckily, 
Sklearn implements this functionality.

#### Glicko-2 Rating Deviation

See `rd_experiment.py`. The Glicko-2 rating metric assumes a team's true skill is normally distributed.
In this experiment we explore how variable the average Glicko distribution becomes when considering 
data from further back in time. We conclude that it is actually more likely using as much data as 
possible---and therefore data from further in the past---is more beneficial. 

#### Spending Experiment

See `spending_experiment.py`. A simple experiment to see how well correlated the
all-time rating (calculated with Glicko-2 beginning from 1985) of the top 25 
teams is with Men's Basketball spending. We remove a few outliers through Tukey fences and show, unsurprisingly, 
a correlation of `r = 0.6058` between Glicko-2 and 2017 Men's Basketball spending.
