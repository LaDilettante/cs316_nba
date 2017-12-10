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
