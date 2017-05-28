#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 20:25:04 2017
Modified on Wed May 24 @ around midnight

@author: mes & wes (humble research assistant)

Implement an XGBoost model for the Sberbank Housing Kaggle Competition.
It must be flexible in the sense of bringing in data
"""
#%%
from datetime import datetime
import pandas as pd
import numpy as np
import os
import sys
import time
#sys.path.append('/home/mes/venv/lib/python2.7/site-packages/')
import xgboost as xgb
## label encoding
import sklearn
from sklearn.grid_search import GridSearchCV   #Performing grid search
#import matplotlib.pyplot as plt


SUBSET = True

#%%
DIR_PATH = '../../../data/'
train_file = 'train_total.csv'
test_file = 'test_total.csv'

## loading data as Pandas dataframes
train_raw = pd.read_csv(os.path.join(DIR_PATH, train_file), 
                        header='infer', 
                        index_col='id',
                        parse_dates=['timestamp'])
test_raw = pd.read_csv(os.path.join(DIR_PATH, test_file), 
                       header='infer', 
                       index_col='id',
                       parse_dates=['timestamp'])

#%%
## Trim down the sub_area levels to the top 25 and put all others as there
## own separate level
freq_area = np.array(train_raw.loc[:, 'sub_area'].value_counts()[:25].index)

train_raw.loc[~train_raw['sub_area'].isin(freq_area), 'sub_area'] = 'other'
test_raw.loc[~test_raw['sub_area'].isin(freq_area), 'sub_area'] = 'other'

# Dummifying categorical variables for Xgboost to be able to analyze as numerical.
train_raw = pd.get_dummies(train_raw)
test_raw = pd.get_dummies(test_raw)

# Manually force dummification of numerical columns more akin to category.
train_raw = pd.get_dummies(train_raw, columns = {'material'})  
test_raw = pd.get_dummies(test_raw, columns = {'material'})

## time features, the timestamp as is makes the xgboost fail
train_raw.loc[:, 'year'] = train_raw.loc[:, 'timestamp'].apply(lambda x: x.strftime('%Y'))
train_raw.loc[:, 'month'] = train_raw.loc[:, 'timestamp'].apply(lambda x: x.strftime('%m'))

test_raw.loc[:, 'year'] = test_raw.loc[:, 'timestamp'].apply(lambda x: x.strftime('%Y'))
test_raw.loc[:, 'month'] = test_raw.loc[:, 'timestamp'].apply(lambda x: x.strftime('%m'))

## This allows the model to run over a subset of the entire data
if SUBSET:
    features = ['log_fullsq', 'log_lifesq', 'floor', 'max_floor', 'build_year', 'log_kitchsq', 
                'material_1.0', 'material_2.0', 'material_4.0', 'material_5.0', 'material_6.0',
                'ecology_excellent', 'ecology_good', 'ecology_no data', 'ecology_poor', 'ecology_satisfactory',
                'product_type_Investment','product_type_OwnerOccupier',
                'metro_min_avto',
                'metro_km_avto',
                'metro_min_walk',
                'metro_km_walk',
                'kindergarten_km',
                'school_km',
                'park_km',
                'green_zone_km',
                'industrial_km',
                'water_treatment_km',
                'incineration_km',
                'railroad_station_walk_km',
                'railroad_station_walk_min',
                'ID_railroad_station_walk',
                'railroad_station_avto_km',
                'railroad_station_avto_min',
                'public_transport_station_km',
                'public_transport_station_min_walk',
                'water_km',
                'sadovoe_km',
                'bulvar_ring_km',
                'kremlin_km',
                'big_road1_km',
                'big_road2_km',
                'railroad_km',
                'zd_vokzaly_avto_km',
                'oil_chemistry_km',
                'nuclear_reactor_km',
                'radiation_km',
                'power_transmission_line_km',
                'thermal_power_plant_km',
                'mosque_km',
                'theater_km',
                'museum_km',
                'exhibition_km',
                'catering_km',
                'green_part_500',
                'cafe_count_500',
                'cafe_sum_500_min_price_avg',
                'cafe_sum_500_max_price_avg',
                'cafe_avg_price_500',
                'cafe_count_500_na_price',
                'cafe_count_500_price_500',
                'cafe_count_500_price_1000',
                'cafe_count_500_price_1500',
                'cafe_count_500_price_2500',
                'cafe_count_500_price_4000',
                'cafe_count_500_price_high',
                'green_part_1000',
                'cafe_count_1000',
                'cafe_sum_1000_min_price_avg',
                'cafe_sum_1000_max_price_avg',
                'cafe_avg_price_1000',
                'cafe_count_1000_na_price',
                'cafe_count_1000_price_500',
                'cafe_count_1000_price_1000',
                'cafe_count_1000_price_1500',
                'cafe_count_1000_price_2500',
                'cafe_count_1000_price_4000',
                'cafe_count_1000_price_high',
                'sub_area_Bogorodskoe',
                "sub_area_Gol'janovo",
                'sub_area_Izmajlovo',
                'sub_area_Juzhnoe Butovo',
                'sub_area_Krjukovo',
                'sub_area_Ljublino',
                "sub_area_Mar'ino",
                'sub_area_Mitino',
                'sub_area_Nagatinskij Zaton',
                'sub_area_Nagornoe',
                'sub_area_Nekrasovka',
                'sub_area_Otradnoe',
                'sub_area_Poselenie Desjonovskoe',
                'sub_area_Poselenie Filimonkovskoe',
                'sub_area_Poselenie Moskovskij',
                'sub_area_Poselenie Shherbinka',
                'sub_area_Poselenie Sosenskoe',
                'sub_area_Poselenie Vnukovskoe',
                'sub_area_Poselenie Voskresenskoe',
                'sub_area_Severnoe Tushino',
                'sub_area_Solncevo',
                'sub_area_Strogino',
                "sub_area_Tekstil'shhiki",
                'sub_area_Tverskoe',
                'sub_area_Zapadnoe Degunino',
                'sub_area_other'] 

    train = train_raw[features]
    test = test_raw[features]
else:
    train = train_raw.copy()
    test = train_raw.copy()
    features = list(test.columns)


#%%    
#Must encode object columns for the model
#for f in train.columns:
#    if train[f].dtype=='object':
#        print('encoding training feature: {}'.format(f))
#        lbl = sklearn.preprocessing.LabelEncoder()
#        train.loc[:,f] = lbl.fit_transform(train.loc[:,f])
        
#for f in test.columns:
#    if test[f].dtype=='object':
#        print('encoding test feature: {}'.format(f))
#        lbl = sklearn.preprocessing.LabelEncoder()
#        test.loc[:,f] = lbl.fit_transform(test.loc[:,f])

#%%
# Convert data frames to numpy arrays
X_train = train.values
Y_train = train_raw['log_price'].values
X_test = test.values

#%%
# Subset to tune XGB 'num_boost_rounds'
size_ = 7000
X_train_sub, Y_train_sub = X_train[:-size_],  Y_train[:-size_]
X_val, Y_val = X_train[-size_:],  Y_train[-size_:]

dtrain = xgb.DMatrix(X_train, 
                    Y_train, 
                    feature_names=features)
dtrain_sub = xgb.DMatrix(X_train_sub, 
                        Y_train_sub, 
                        feature_names=features)
d_val = xgb.DMatrix(X_val, 
                    Y_val, 
                    feature_names=features)
dtest = xgb.DMatrix(X_test, 
                    feature_names=features)

#%%
#hyperparameters

gridsearch_params = {
    'max_depth' : [3,4,5,6,7,8],
    'min_child_weight' : [1,2,3,4,5],
    'learning_rate' : [.4],
    'subsample': [.8],
    'objective': ['reg:linear'],
    'silent': [1],
    'colsample_bytree': [0.8], 
    'n_estimators': [250],
}

"""
gridsearch_params = {
    'max_depth' : [3],
    'min_child_weight' : [1],
    'learning_rate' : [.4],
    'subsample': [.8],
    'objective': ['reg:linear'],
    'silent': [1],
    'colsample_bytree': [0.8], 
    'n_estimators': [250],
}
"""

#Tune the model
#sub_model = xgb.train(xgb_params, 
#                      dtrain_sub, 
#                      num_boost_round=2000,
#                      evals=[(d_val, 'val')],
#                      early_stopping_rounds=20, 
#                      verbose_eval=50)
print(datetime.now())

#cv = xgb.cv(xgb_params, dtrain, num_boost_round = 5000, nfold = 5, metrics = {"rmse"})
#output.write(str(cv))
#print(cv)



## Now let's run a grid search:

xgb_model = xgb.XGBRegressor()
opt_GBM = GridSearchCV(xgb_model,gridsearch_params, cv = 5, n_jobs = 4, verbose = 1) 
opt_GBM.fit(X_train, Y_train)  
print(opt_GBM.grid_scores_)
print(opt_GBM.best_estimator_)
print(opt_GBM.best_score_)
print(opt_GBM.best_params_)

print(datetime.now())

#%%
#Train the model
full_model = xgb.train(opt_GBM.best_params_, dtrain)
full_model.save_model('xgb0001.model')

#%%
#Create the importance plot (I wish I could do this remotely)
#fig, ax = plt.subplots(figsize=(12,18))
#xgb.plot_importance(model, max_num_features=50, height=0.8, ax=ax)
#plt.savefig('figure/xgb_importance_' + time.strftime('%Y%m%d-%H%M') + '.png') 

#predict the prices from the test data
y_pred = full_model.predict(dtest)

# Transform from ln(price) to regular price
y_pred = np.exp(y_pred)

#%%
#Write them to csv for submission
submit = pd.DataFrame({'id': np.array(test.index), 'price_doc': y_pred})
savefile = 'submissions/submission_xgb_' + time.strftime('%Y%m%d-%H%M') + '.csv'
submit.to_csv(savefile, index=False)
