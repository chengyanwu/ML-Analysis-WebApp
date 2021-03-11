import pandas as pd
import numpy as np
import mpld3
from sklearn.preprocessing import StandardScaler
import io


import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
plt.switch_backend('Agg')
def run_algo1(file_path):
    #1. load data
    df = pd.read_csv('./phase1/diabetes.csv')
    xs = df.drop('Outcome', 1)
    ys = df['Outcome']
    from sklearn.model_selection import train_test_split
    #4. data-splitting
    random_state = 42
    xtrain, xtest, ytrain, ytest = train_test_split(xs, ys, test_size=0.5, random_state= random_state)
    sc = StandardScaler()
    xtrain = sc.fit_transform(xtrain)
    xtest = sc.fit_transform(xtest)
    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier(max_depth=10, random_state = random_state)
    clf.fit(xtrain, ytrain)
    # Load file_path instead of unknowns.csv
    # Do the same processing you did to
    # get your unknowns.csv results from your model.
    # Get the figure object Matplotlib will be working with:
    fig = plt.figure()
    # Scatterplot your results, as per
    # # #any of your scatterplots from homework 1. Make sure to use plt.xlabel(), plt.ylabel() and plt.title() to give clear labeling!
    unknown = pd.read_csv(file_path)
    unknown_tranformed = sc.fit_transform(unknown)
    pred = np.round(clf.predict(unknown_tranformed))
    #print(pred)
    plt.scatter(unknown['Glucose'][pred==1], unknown['BloodPressure'][pred==1], label='Positive')
    plt.scatter(unknown['Glucose'][pred==0], unknown['BloodPressure'][pred==0], label = 'Negative')
    plt.legend()
    plt.xlabel('Glucose')
    plt.ylabel('BloodPressure')
    plt.title('Classification Results on Diabetes data with Decision Tree')
#    html_str = mpld3.fig_to_html(fig)
#    Html_file= open("index.html","w")
#    Html_file.write(html_str)
#    Html_file.close()
    return mpld3.fig_to_html(fig)
    
def run_algo2(file_path):
    df = pd.read_csv('./phase1/white_wine.csv')
    xs = df.drop('quality', 1)
    ys = df['quality']
    #4. data-splitting
    from sklearn.model_selection import train_test_split
    random_state = 42
    xtrain, xtest, ytrain, ytest = train_test_split(xs, ys, test_size=0.5, random_state= random_state)
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    xtrain = sc.fit_transform(xtrain)
    xtest = sc.fit_transform(xtest)
    from sklearn import svm
    clf = svm.SVC(C = 1.3, gamma =  1.3, kernel= 'rbf').fit(xtrain, ytrain)
    clf = svm.SVC().fit(xtrain, ytrain)
    # Load file_path instead of unknowns.csv
    # Do the same processing you did to
    # get your unknowns.csv results from your model.
    # Get the figure object Matplotlib will be working with:
    #fig = plt.figure()
    # Scatterplot your results, as per
    # # #any of your scatterplots from homework 1. Make sure to use plt.xlabel(), plt.ylabel() and plt.title() to give clear labeling!
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    unknown = pd.read_csv(file_path)
    unknown_tranformed = sc.fit_transform(unknown)
    pred = np.round(clf.predict(unknown_tranformed))
    unknown['quality'] = pred;
    
    unknown.plot.scatter(x= 'alcohol', y='pH', s=2.5,c = 'quality', colormap = 'plasma')
    #plt.scatter(unknown['alcohol'], unknown['pH'], s=10, c=unknown['quality'] , cmap = "viridis_r")
    plt.legend()
    plt.xlabel('Alcohol')
    plt.ylabel('pH')
    plt.title('Regression Results on Wine Data with SVC')
    return mpld3.fig_to_html(plt.gcf())
    
def run_algo3(file_path):
    import plotly.express as px

    df = pd.read_csv(file_path)
    name = df['Player']
    select_feature = ['AST', 'PTS', 'TRB']
    outliner_fraction = 0.05
    data = df[select_feature]

    from sklearn.svm import OneClassSVM
    svm = OneClassSVM(nu=outliner_fraction).fit(data)

    scores = svm.decision_function(data)
    inde = np.argsort(scores)[:3]
    topthree = df.iloc[inde]

    outliers = scores < 0

    res = np.where(scores < 0, 'Outliers', 'Inliers')
    res[inde] = 'Top3'
    s = np.where(scores < 0, 2, 1)
    s[inde] = 5

    outliers_without_top_three = outliers.copy()
    outliers_without_top_three[inde] = False

    name = name.iloc[inde]

    data['res'] = res
    data['s'] = s

    fig = px.scatter_3d(data, x='AST', y='PTS', z='TRB', color='res', opacity=0.7, size=s)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    import plotly.io as pio

    return pio.to_html(fig)

'''
import pandas as pd
unknown = pd.read_csv("unknowns.csv")
print(unknown)
pred = clf.predict(unknown)
prediction = pd.DataFrame(pred, columns=['predictions'].to_csv('prediction.csv', index = False))
print(clf.score(xtest, ytest))
'''


