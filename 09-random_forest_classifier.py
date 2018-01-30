#!usr/bin/env python3
#-*- coding:utf-8 -*-

import pandas
import numpy
import os
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

trainFile = r'D:\刘井平学长\数据记录\dataset.csv'
pwd = os.getcwd()
os.chdir(os.path.dirname(trainFile))
data = pandas.read_csv(os.path.basename(trainFile),usecols = [0,1,2,3,4,5])
label = pandas.read_csv(os.path.basename(trainFile),usecols = [6,])
os.chdir(pwd)

#选择K个最好的特征，返回选择特征后的数据
feature = SelectKBest(chi2, k=6).fit_transform(data,label)

data_train,data_test,label_train,label_test = cross_validation.train_test_split(data,label,test_size = 0.4,random_state = 0)
rf = RandomForestClassifier(n_estimators = 100,max_features = 'sqrt',max_depth = None,min_sample_split = 1)
rf.fit(data_train,label_train)
print(rf.score(data_test,label_test))
