from flask import Flask,render_template,send_file
import matplotlib.pyplot as plt
import pandas as pn
import io
from io import BytesIO
from sklearn.model_selection import  train_test_split
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import requests
import json
import base64
app = Flask(__name__)


@app.route('/')
def hello_world():
    data=pn.read_csv("location.csv")
    traindata = pn.concat([data['Longitude'], data['Latitude']], axis=1)

    kmeans = KMeans(n_clusters=3, random_state=0).fit(traindata)

    print(kmeans.labels_)

    i=plt.plot(traindata['Longitude'], traindata['Latitude'], 'ro')

    plt.show()
    y = [0] * 3
    for i in range(len(kmeans.labels_)):
        if (kmeans.labels_[i] == 0):
            plt.scatter(traindata['Longitude'][i], traindata['Latitude'][i], c='r', marker="*")
        elif (kmeans.labels_[i] == 1):
            plt.scatter(traindata['Longitude'][i], traindata['Latitude'][i], c='y', marker="o")
        elif (kmeans.labels_[i] == 2):
            plt.scatter(traindata['Longitude'][i], traindata['Latitude'][i], c='g', marker=",")
        y[kmeans.labels_[i]] = y[kmeans.labels_[i]] + 1

    model = DBSCAN(eps=2, min_samples=2).fit(traindata)
    print(model.labels_)


    x = kmeans.cluster_centers_

    for i in x:
        plt.scatter(i[0], i[1], c='r', marker="*")
    image = BytesIO()
    plt.savefig(image)
    image.seek(0)
    plot_url = base64.b64encode(image.getvalue()).decode()
    plt.show()

    print("The rescue teams need to be sent to the following places immediately")
    a = max(y)
    for i in range(len(y)):
        if (y[i] == a):
            decidingvar=x[i]
            print(x[i])

    return render_template("index.html",plot_url=plot_url,decidingvar=decidingvar)
@app.route("/decision")
def decisiontaker():
    d=["burger","bun","cream"]
    return render_template("loc.html",d=d)

if __name__ == '__main__':
    app.run()
