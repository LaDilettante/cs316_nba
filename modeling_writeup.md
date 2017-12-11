# How to make predictions

- Load pickled model, e.g. `pickle.load(open('model/randomforest.pkl', 'rb'))`
- Use the `predict` to generate predictions `my_model.predict(X)`, where `X` is a nested list of features. Each element of the outer list is a player. Each element of the inner list is a feature of that player.

## Model without team features

col_point 	col_rebound 	col_assist 	col_steal 	col_block 	position_C 	position_C-F 	position_F 	position_F-C 	position_F-G 	position_G 	position_G-F

where col_point, col_rebound, etc. are that player's last year of college performance.

For example, for A.J. Price

`my_model.predict([[17.8, 4.2, 5.7, 0.8, 0.0, 0, 0, 0, 0, 0, 1, 0]]`

## Model with team features

col_point 	col_rebound 	col_assist 	col_steal 	col_block 	team_win_percentage 	team_point 	team_opponent_point 	team_rebound 	team_assist 	team_steal 	team_block 	position_C 	position_C-F 	position_F 	position_F-C 	position_F-G 	position_G 	position_G-F

where team_X are that team's performance during the player last college year

For example, for A.J. Price, Connecticut

`my_model.predict([[17.8, 4.2, 5.7, 0.8, 0.0, 0.529, 2380.0, 2266.0, 1338.0, 461.0 	220.0, 260.0, 0, 0, 0, 0, 0, 1, 0]])`

# Model building methodology

## Data description

Our goal is to predict a draftee's first year performance (i.e. average per game point, rebound, assist, steal, block -- average per game) in the NBA based on
- his last year's performance in college (i.e. point, rebound, assist, steal, block -- average per game)
- his position in the college team
- his college's performance during his last year (i.e. win percentage; average per game point, rebound, assist, steal, block)

## Model choice

To make these predictions, we train two models: 1) random forest, and 2) nearest neighbor. We use a random forest because of its tendency to make accurate, generalizable predictions across very different domains -- certainly a good default choice. We use a nearest neighbor model because we also want to show the user players that are similar to the player of their choosing.

## Model training

For each model, we choose its tuning parameter via grid search cross validation, i.e.:
- Creating a grid of parameter values. For example, for the random forest, we create a 3 x 3 grid for 2 parameters `n_estimator` and `min_samples_leaf` as `{'n_estimators': [100, 1000, 1000], 'min_samples_leaf': [1, 10, 100]}`
- Choosing the best parameter values in this grid via cross validation, i.e. 1) splitting the dataset into training data and testing data, 2) train a model for each set of parameter value using the training data, 3) evaluate the model's predictions using the testing data, 4) choose the model with the best predictions

We evaluate a model's prediction by its Mean Squared Error, which is appropriate because the metrics (points, assist, rebound, etc.) aren't too large, so there is no need for something like Mean Squared Log Error.

## Model result

As expected, the predictive performance of the random forest is slightly better than that of the nearest neighbor.

For example, to predict a player's rookie point per game:
- Random forest's average error (RMSE) = 4.14
- Nearest neighbor's average error (RMSE) = 4.59
As a comparison, median point per game as 4.4.

Given that a random forest takes a much longer time to run, a nearest neighbor model would suffice in most situations.
