# KMeans Clustering Method Proposition de réflexion
# Inertia : Sum of squared distances between observations and their closest centroid

# BASELINE CLUSTERS
# La consommation en kcal/jour est de :
DIETARY_KCAL_DAY = 2500
NUTRI_NEEDS_DINER = 0,30
# la consommation équilibrée et les équivalences en kcal/gr sont :
GLUCIDS_PER_DAY = 0,50
GR_GLUCID_KCAL = 4
PROTEINS-PER_DAY = 0,30
GR_PROTEIN_KCAL = 4
LIPIDS-PER-DAY = 0,20
GR_LIPID_KCAL = 9
# Il resort la cible '3 centroids' :
'target_cluster_carbohydrates_100g' = 93.75  # g/diner
'target_cluster_proteins_100g' =  56.25 # g/diner
'target_cluster_fat_100g' = 16,66 # g/diner
# L'OMS recommande de consommer moins 5 g de sel/jour (réalité entre 8 et 19 g/jour)
'target_cluster_salt_100' = 1.5 # g/diner

# SCENARIO.1 KMEAN km3 {carbohydrates_100g, proteins_100g, fat_100g}
# Dataset
import pandas as pd
import numpy as np

# Convert the Numpy Array to a DataFrame
X_np = pd.DataFrame(X_pd)
X_nutri = X_np['carbohydrates_100g', 'proteins_100g', 'fat_100g']
# y_pred_nutri?

# Fit K-means n_clusters=3
from sklearn.cluster import KMeans
km3 = KMeans(n_clusters=3, random_state=42)
km3.fit(X_nutri)

# Centroids with n_clusters=3
km3.cluster_centers_.shape  # => (3,3)?

# Prediction n_clusters=3
import pandas as pd
y_pred_nutri = km3.predict(X_nutri)

# Accuracy n_clusters=3
from sklearn.metrics import accuracy_score
accuracy_score(y_pred_nutri, y)  # => 0.75?

# Inertia n_clusters=3
inertia_nutri3 = KMeans(n_clusters=3, random_state=42).fit(X_nutri).inertia_
	 # => inertia_nutri3 = 10000.00?


# SCENARIO2 Hierarchical Clustering
# cluster.hierarchy
# https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html
# linkage
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html#scipy.cluster.hierarchy.linkage
# dendogram
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html#scipy.cluster.hierarchy.dendrogram

from scipy.cluster.hierarchy import dendrogram, linkage
