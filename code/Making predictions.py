
# coding: utf-8

# In[1]:


import pickle


# In[3]:


randomforest_point = pickle.load(open('../model/randomforest_point.pkl', 'rb'))
randomforest_team_point = pickle.load(open('../model/randomforest_team_point.pkl', 'rb'))


# In[4]:


nn_point = pickle.load(open('../model/nearestneighbor_point.pkl', 'rb'))
nn_team_point = pickle.load(open('../model/nearestneighbor_team_point.pkl', 'rb'))


# In[5]:


training_data = pickle.load(open('../model/training_data.pkl', 'rb'))
training_data_team = pickle.load(open('../model/training_data_team.pkl', 'rb'))


# In[8]:


# Features used to train model (without team data)
training_data.head()


# In[14]:


# Prediction for A.J. Hammons's points
print(randomforest_point.predict([[16.6, 11.4, 0.7, 0.6, 4.7, 1, 0, 0, 0, 0, 0, 0]]))
print(nn_point.predict([[16.6, 11.4, 0.7, 0.6, 4.7, 1, 0, 0, 0, 0, 0, 0]]))


# In[26]:


# Get A.J. Hammons nearest neighbors in terms of points

# Get the neighbor indices, i.e. their row number in the training dataset
neighbor_indices = nn_point.kneighbors(X=[[16.6, 11.4, 0.7, 0.6, 4.7, 1, 0, 0, 0, 0, 0, 0]], n_neighbors=5, return_distance=False)
training_data.iloc[neighbor_indices[0], :].index.values


# In[12]:


# Features used to train model (with team data)
training_data_team.head()


# In[29]:


# Prediction for A.J. Hammons's points
print(randomforest_team_point.predict([[16.6, 11.4, 0.7, 0.6, 4.7, 0.618, 2375.0, 2195.0, 1249.0, 505.0, 185.0, 177.0, 1, 0, 0, 0, 0, 0, 0]]))

