import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
np.random.seed(2)


def add_noise(data):
    """
    :param data: dataset as numpy array of shape (n, 2)
    :return: data + noise, where noise~N(0,0.001^2)
    """
    noise = np.random.normal(loc=0, scale=0.001, size=data.shape)
    return data + noise


def choose_initial_centroids(data, k):
    """
    :param data: dataset as numpy array of shape (n, 2)
    :param k: number of clusters
    :return: numpy array of k random items from dataset
    """
    n = data.shape[0]
    indices = np.random.choice(range(n), k, replace=False)
    return data[indices]


# ====================
def transform_data(df, features):
    """
    Performs the following transformations on df:
        - selecting relevant features
        - scaling
        - adding noise
    :param df: dataframe as was read from the original csv.
    :param features: list of 2 features from the dataframe
    :return: transformed data as numpy array of shape (n, 2)
    """

    hum = df[features[0]]
    cnt = df[features[1]]
    data = np.array([hum, cnt], dtype=float).T

    sum_hum = 0
    sum_cnt = 0
    for hum in data[0]:
        sum_hum += hum
    for cnt in data[1]:
        sum_cnt += cnt

    for i in range(data):
        data[i][0] = (data[i][0] - min(hum))/sum_hum
        data[i][1] = (data[i][1] - min(cnt))/sum_cnt

    return add_noise(data)


def kmeans(data, k):
    """
    Running kmeans clustering algorithm.
    :param data: numpy array of shape (n, 2)
    :param k: desired number of cluster
    :return:
    * labels - numpy array of size n, where each entry is the predicted label (cluster number)
    * centroids - numpy array of shape (k, 2), centroid for each cluster.
    """
    prev_centroids = choose_initial_centroids(data, k)
    labels = np.array(np.zeros(shape=(data)), dtype=float)

    while True:
        for i in range(data):
            labels[i] = find_closest_centroid(prev_centroids, data[i])

        current_centroids = recompute_centroids(labels, data, k)

        if np.array_equal(prev_centroids, current_centroids):
            break

    return labels, current_centroids


def find_closest_centroid(centroids, point):
    """

    :param centroids:
    :param point:
    :return:
    """
    distances = np.array(np.zeros(shape=(centroids)), dtype=float)
    for i in range(centroids):
        distances[i] = dist(centroids[i], point)

    min = 2
    index = 0
    for i in range(distances):
        if distances[i] < min:
            min = distances[i]
            index = i
    return index


def visualize_results(data, labels, centroids, path):
    """
    Visualizing results of the kmeans model, and saving the figure.
    :param data: data as numpy array of shape (n, 2)
    :param labels: the final labels of kmeans, as numpy array of size n
    :param centroids: the final centroids of kmeans, as numpy array of shape (k, 2)
    :param path: path to save the figure to.
    """

    clusters_find = find_clusters(len(labels), labels, len(data))
    clusters = []
    for i in range(len(labels)):
        clusters[i] = find_cluster_i(data, clusters_find[i])

    colors = np.array(['purple', 'yellow', 'blue', 'red', 'green'])
    plt.figure(figsize=(18,8))
    for cluster in clusters:
        plt.scatter(cluster[0], cluster[1], c=colors[i])

    plt.xlabel('cnt')
    plt.ylabel('hum')
    plt.title('Results for kmeans with k = ' + str(len(centroids)))

    plt.savefig(path)


def find_cluster_i(data, cluster_i):
    cluster = (-1) * np.ones(shape=(len(data), 2), dtype=float)
    j = 0
    for i in cluster_i:
        cluster[j][0] = data[i][0]
        cluster[j][1] = data[i][1]
        j += 1

    return cluster

def find_clusters(k, labels, length):
    clusters = np.zeros(shape=(k, length), dtype=int)
    count = np.zeros(shape=(k), dtype=int)
    for i in range(length):
        clusters[labels[i]][count[labels[i]]] = i
        count[labels[i]] += 1

    return clusters


def dist(x, y):
    """
    Euclidean distance between vectors x, y
    :param x: numpy array of size n
    :param y: numpy array of size n
    :return: the euclidean distance
    """
    sum = np.array(np.zeros(shape=(x)), dtype=float)
    for i in range(x):
        sum[i] = (x[i] - y[i]) ** 2

    return np.sqrt(np.array([np.sum(sum)], dtype=float))


def assign_to_clusters(data, centroids):
    """
    Assign each data point to a cluster based on current centroids
    :param data: data as numpy array of shape (n, 2)
    :param centroids: current centroids as numpy array of shape (k, 2)
    :return: numpy array of size n
    """
    pass
    # return labels


def recompute_centroids(data, labels, k):
    """
    Recomputes new centroids based on the current assignment
    :param data: data as numpy array of shape (n, 2)
    :param labels: current assignments to clusters for each data point, as numpy array of size n
    :param k: number of clusters
    :return: numpy array of shape (k, 2)
    """
    centroids = np.array(np.zeros(shape=(k, 2)), dtype=float)
    count = np.array(np.zeros(shape=(k)), dtype=int)
    sum = np.array(np.zeros(shape=(k, 2)), dtype=float)

    for i in range(data):
        count[labels[i]] += 1
        sum[labels[i]][0] += data[i][0]
        sum[labels[i]][1] += data[i][1]

    for i in range(k):
        centroids[i][0] = sum[i][0] / count[i]
        centroids[i][1] = sum[i][1] / count[i]

    return centroids

