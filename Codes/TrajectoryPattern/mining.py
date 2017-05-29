# def dbscan(dim):
#     # dbscan cluster algorithm,
#     # dim(2), location(x, y)
#     # dim(3), location+time
#     pass

# def main():
#     # read location
#     file = open('../../inputfiles/Kaohsiung2014_case.csv')
#     lines = file.readlines()

#     print(len(lines))
#     file.close()

#     '''
#     too dark
#     '''
#     pass

# if __name__ == '__main__':
#     main()

print(__doc__)

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler



# file = open('../../inputfiles/Kaohsiung2014_case.csv')
# lines = file.readlines()

# print(len(lines))
# file.close()

# t = [[2,3], [4,5], [10,11]]

# a = np.array( t )

# print(t)
# print(a)

# # while 1:
# #     pass

centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

# X = [[1 1], [-1 -1], [1 -1]]

db = DBSCAN(eps=0.3, min_samples=10).fit(X)
# print(db.labels_)

X = StandardScaler().fit_transform(X)

# db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# # Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
# print(len(set(labels)))
# print(n_clusters_)
# print('Estimated number of clusters: %d' % n_clusters_)
# print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
# print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
# print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
# print("Adjusted Rand Index: %0.3f"
#       % metrics.adjusted_rand_score(labels_true, labels))
# print("Adjusted Mutual Information: %0.3f"
#       % metrics.adjusted_mutual_info_score(labels_true, labels))
# print("Silhouette Coefficient: %0.3f"
#       % metrics.silhouette_score(X, labels))

import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()

# print(X)
# print(type(X))
# print(len(X))
# # plt.plot(X, 'o')
# # plt.show()
# lat = []
# lon = []
# for x in a:
#     lat.append(x[0])
#     lon.append(x[1])

# print(lat)
# print(lon)
# plt.plot(lat, lon, 'o')
# plt.show()