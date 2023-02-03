# -*- coding: utf-8 -*-
"""서울시 따릉이 대여량 예측.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14lzwujSCU_V1WOhRjV_FBvIAbki67ocg
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import missingno as msno
import warnings
from scipy.stats import probplot
# %matplotlib inline
warnings.filterwarnings('ignore')
import pandas as pd #판다스 패키지 불러오기
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor #랜덤 포레스트 불러오기

train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')
submission = pd.read_csv('submission.csv')

train_df.head()

train_df.describe()

test_df.describe()

train_df.isnull().sum()

train_df.shape

test_df.isnull().sum()

test_df.shape

fig, ax = plt.subplots(1, 1, figsize=(10,10))
corrmat = train_df.corr(method='spearman')
indexes = corrmat.nlargest(n=11, columns='count').index
corrmat = train_df[indexes].corr(method='spearman')
sns.heatmap(data=corrmat, annot=True, cbar=True, fmt='.2f', ax=ax)

"""count와 관련된 상관관계 분석
- hour변수가 가장 큰 양의 상관관계 보임
- hour_bef_temperature (빌린날의 온도) 역시 강한 상관관계를 보임
- hour_bef_humidity (습도) 반대로 음의 상관관계를 나타냄
"""

train_df.info()

test_df.info()

train_df['hour_bef_temperature'] = train_df['hour_bef_temperature'].fillna(value = train_df['hour_bef_temperature'].mean())

train_df.isna().sum()

train_isna_sum = train_df.isna().sum()

train_isna_sum[train_isna_sum != 0].index

na_columns = train_isna_sum[train_isna_sum != 0].index

def fill_bicycle_na(df, column) :
    
    df[column] = df[column].fillna(value = df[column].mean())

fill_bicycle_na(train_df, 'hour_bef_precipitation')

for col in na_columns:
    
    fill_bicycle_na(train_df, col)

train_df.isna().sum()

test_isna_sum = test_df.isna().sum()

test_na_columns = test_isna_sum[test_isna_sum != 0].index

for col in test_na_columns:
    fill_bicycle_na(test_df, col)

test_df.isna().sum()

train_df.columns

obj_columns = ['hour_bef_temperature', 'hour_bef_precipitation',
               'hour_bef_windspeed', 'hour_bef_humidity', 'hour_bef_ozone',
               'hour_bef_pm10', 'hour_bef_pm2.5']

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(train_df[obj_columns])
train_df[obj_columns] = scaler.transform(train_df[obj_columns])
test_df[obj_columns] = scaler.transform(test_df[obj_columns])

train_df

target = train_df['count']

#train_df = pd.concat([pd.get_dummies(train_df['hour'], prefix='hour'), train_df], axis=1)

#test_df = pd.concat([pd.get_dummies(test_df['hour'], prefix='hour'), test_df], axis=1)

#train_df.drop(columns='hour', inplace=True)
#test_df.drop(columns='hour', inplace=True)

#X = train_df.drop(columns='count').to_numpy()
#y = train_df['count'].to_numpy()
#X_test = test_df.to_numpy() # 테스트 데이터(문제만 있음, 정답은 맞춰야함)

#from sklearn.model_selection import train_test_split, KFold
#kfold = KFold(n_splits=10, shuffle=False)

"""교차검증"""

#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import mean_squared_error
#test_predictions = []
#val_scores = []
#for trn_idx, val_idx in kfold.split(X,y):
#     X_train, y_train = X[trn_idx], y[trn_idx]
#    X_val, y_val = X[val_idx], y[val_idx]
#    model = LinearRegression()
#    model.fit(X_train, y_train)
#    val_pred = np.power(model.predict(X_val), 3).astype(int)#시각화
#    val_true = np.power(y_val, 3)#시각화
#    val_score = np.sqrt(mean_squared_error(val_true, val_pred))
#    val_scores.append(val_score)
#    test_pred = model.predict(X_test)
#    #test_pred = np.power(test_pred, 3).astype(int)
#    test_predictions.append(test_pred)

#test_predictions = np.array(test_predictions)
#test_predictions = np.mean(test_predictions, axis=0)

#val_scores

#np.mean(val_scores)

#X_train.shape, X_val.shape

#test_pred = test_predictions

#submission = pd.read_csv('submission.csv')

#submission

#submission['count'] = test_pred
#submission['count'] = np.round(submission['count']).astype(int)
#submission

"""모델"""

#Modelling
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

import numpy as np

#K-fold
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

#kNN
clf = KNeighborsClassifier(n_neighbors = 13)
scoring = 'accuracy'
score = cross_val_score(clf, train_df, train_df['count'], cv=k_fold, n_jobs=1, scoring=scoring)
print(score)
print(round(np.mean(score)*100, 2))

#Decision Tree
clf = DecisionTreeClassifier()
scoring = 'accuracy'
score = cross_val_score(clf, train_df, train_df['count'], cv=k_fold, n_jobs=1, scoring=scoring)
print(score)
print(round(np.mean(score)*100, 2))

#Random Forest
clf = RandomForestClassifier(n_estimators=13)
scoring = 'accuracy'
score = cross_val_score(clf, train_df, train_df['count'], cv=k_fold, n_jobs=1, scoring=scoring)
print(score)
print(round(np.mean(score)*100, 2))

#Naive Bayes
clf = GaussianNB()
scoring = 'accuracy'
score = cross_val_score(clf, train_df, train_df['count'], cv=k_fold, n_jobs=1, scoring=scoring)
print(score)
print(round(np.mean(score)*100, 2))

#SVC
clf = SVC()
scoring = 'accuracy'
score = cross_val_score(clf, train_df, train_df['count'], cv=k_fold, n_jobs=1, scoring=scoring)
print(score)
print(round(np.mean(score)*100, 2))

#Testing
train_df = train_df.drop("id", axis=1).copy()
train_df = train_df.drop("count", axis=1).copy()
test_data = test_df.drop("id", axis=1).copy()

#KNN
clf = KNeighborsClassifier(n_neighbors = 13)
clf.fit(train_df, target)
prediction = clf.predict(test_data)
submission['count'] = prediction
submission.to_csv('KNN.csv', index=False)

#Decision Tree
clf = DecisionTreeClassifier()
clf.fit(train_df, target)
prediction = clf.predict(test_data)
submission['count'] = prediction
submission.to_csv('DecisiontreeClassifier.csv', index=False)

#Random Forest
clf = RandomForestClassifier(n_estimators=13)
clf.fit(train_df, target)
prediction = clf.predict(test_data)
submission['count'] = prediction
submission.to_csv('RandomForest.csv', index=False)

#Naive Bayes
clf = GaussianNB()
clf.fit(train_df, target)
prediction = clf.predict(test_data)
submission['count'] = prediction
submission.to_csv('NaiveBayes.csv', index=False)

#SVC
clf = SVC()
clf.fit(train_df, target)
prediction = clf.predict(test_data)
submission['count'] = prediction
submission.to_csv('SVC.csv', index=False)

"""Decision Tree이 예측력이 가장 높게 나타남

모델구축
"""

features = ['hour', 'hour_bef_temperature', 'hour_bef_windspeed']

X_train = train_df[features]
Y_train = target

X_test = test_df[features]

print(X_train.shape)
print(Y_train.shape)
print(X_test.shape)

model100 = RandomForestRegressor(n_estimators=100, random_state=0)   # Decision Tree 모델을 여러 개 모아서 만든 것 = Random Forest
model100_5 = RandomForestRegressor(n_estimators=100, max_depth = 5, random_state=0)
model200 = RandomForestRegressor(n_estimators=200)

"""n_estimators : 의사결정나무의 수 (디폴트 100)

random_state : 부트스트랩을 조정하는 역할을 함. 이번 실습에서는 0으로 고정하여 어떠한 환경에서도 똑같은 결과값이 나오도록 할것이다.

max_depth : 노드의 깊이를 지정. 모델의 과대적합(over fitting)을 방지하기 위해 사용
"""

import sklearn
from sklearn.tree import DecisionTreeClassifier

model_dtc = DecisionTreeClassifier(random_state=0)
model_dtr = DecisionTreeRegressor()

"""모델 학습 및 검증"""

model100.fit(X_train, Y_train)
model100_5.fit(X_train, Y_train)
model200.fit(X_train, Y_train)

model_dtc.fit(X_train, Y_train)
model_dtr.fit(X_train, Y_train)

"""모델 예측"""

ypred1 = model100.predict(X_test)
ypred2 = model100_5.predict(X_test)
ypred3 = model200.predict(X_test)

ypred4 = model_dtc.predict(X_test)
ypred5 = model_dtr.predict(X_test)

submission['count'] = ypred1
submission.to_csv('model100.csv', index=False)
     

submission['count'] = ypred2
submission.to_csv('model100_5.csv', index=False)
     

submission['count'] = ypred3
submission.to_csv('model200.csv', index=False)
     

submission['count'] = ypred4
submission.to_csv('model_dtc.csv', index=False)
     

submission['count'] = ypred5
submission.to_csv('model_dtr.csv', index=False)

"""결과 model200의 예측치가 가장 높은 것으로 나타남."""