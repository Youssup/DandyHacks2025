import numpy as np

from sklearn.cluster import KMeans

# player data dict sample data
player_data = np.array([
    [1200],
    [1400],
    [1600],
    [1800],
    [2000],
    [2200],
])

# Define K-means with 2 clusters (teams)
kmeans = KMeans(n_clusters=2, random_state=42)

# Fit the data into the model (no training)
kmeans.fit(player_data)

# name the teams/clusters 0 or 1
labels = kmeans.labels_

# Divide the players into two teams
team1 = [player_data[i][0] for i in range(len(player_data)) if labels[i] == 0]
team2 = [player_data[i][0] for i in range(len(player_data)) if labels[i] == 1]


print("Team 1:", team1)
print("Team 2:", team2)