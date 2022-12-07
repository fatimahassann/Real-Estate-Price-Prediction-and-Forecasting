from datascience import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from scipy.stats import norm
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.decomposition import PCA
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
import category_encoders as ce
from yellowbrick.regressor import ResidualsPlot
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import xgboost as xgb
from xgboost.sklearn import XGBRegressor
from sklearn.metrics import r2_score
from sklearn import metrics
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import max_error
"""Importing the dataset

"""
df =''
regr=''
def getsellerencoding(df,srole):
  x=''
  for i in range(0,(df.shape[0])):
    if df['Seller Role'].iloc[i]==srole:
      x=df['seller_LE'].iloc[i]
      print(df['seller_LE'].iloc[i])
      break
  return x

def gettypeencoding(df,type):
  x=''
  for i in range(0,(df.shape[0])):
    if df['Building Type'].iloc[i]==type:
      x=df['type_LE'].iloc[i]
      print(df['type_LE'].iloc[i])
      break
  return x

def getfinishtypeencoding(df,finishtype):
  x=''
  for i in range(0,(df.shape[0])):
    if df['Finish Type'].iloc[i]==finishtype:
      x=df['finish_type_LE'].iloc[i]
      print(df['finish_type_LE'].iloc[i])
      break
  return x

def getviewencoding(df,view):
  x=''
  for i in range(0,(df.shape[0])):
    if df['View'].iloc[i]==view:
      x=df['view_LE'].iloc[i]
      print(df['view_LE'].iloc[i])
      break
  return x

def getage(year):
  return 2022-year

def getAddressencoding(df,address):
  x=''
  for i in range(0,(df.shape[0])):
    if df['Address'].iloc[i]==address:
      x=df['Address_LE'].iloc[i]
      print(df['Address_LE'].iloc[i])
      break
  return x

def getpaymentecoding(df,payement):
  x=''
  for i in range(0,(df.shape[0])):
    if df['Payment Method'].iloc[i]==payement:
      x=df['payement_LE'].iloc[i]
      print(df['payement_LE'].iloc[i])
      break
  return x

def preparemodel():

    global df
    global regr

    df = pd.read_csv("dsNOV.csv", encoding='cp1252') # Read CSV into dataframe

    """# DATA ANALYSIS

    Analyze the dataset.

    Missing data
    """

    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    missing_data.head(20)

    """# Data Cleaning

    Remove duplicates
    """

    df = df.drop_duplicates(keep=False)

    """Removing Extra Columns"""

    df.drop('Unnamed: 16', axis=1, inplace=True)

    df.drop('Publish Date', axis=1, inplace=True)

    df.drop('Mortgage', axis=1, inplace=True)

    """Filling missing values"""

    df['Floor']=df['Floor'].fillna('0')

    """Cleaning Area and removing outliers """

    df=df.drop(df.loc[df['Area'].isnull()].index)

    df.loc[ df['Area'] == ' three hundred fifty', 'Area'] = '350'
    df.loc[ df['Area'] == 'three hundred fifty', 'Area'] = '350'

    print(df['Area'].unique())

    df.loc[df['Area'].isna()]


    df['Area'] = df['Area'].astype(int)

    df = df[df['Area']<1500]
    df = df[df['Area']>25]

    """Calculating the Price"""

    df.drop(df.loc[df['Price Per Meter']=='0.78261'].index, inplace=True)

    df['Price Per Meter'] == '.78261'
    df.loc[ df['Price Per Meter'] == '.78261', 'Price Per Meter'] = '78261'
    df.loc[ df['Price Per Meter'] == '40 698', 'Price Per Meter'] = '40698'

    df['Price Per Meter'] = df['Price Per Meter'].astype(int)

    df['Price_NEW'] = df['Area']*df['Price Per Meter']

    df.drop('Price', axis=1, inplace=True)
    df.drop('Price Per Meter', axis=1, inplace=True)

    df = df[df['Price_NEW']<50000000]
    df = df[df['Price_NEW']>100000]

    """Date cleaning"""

    df['Age'] = 2022 - df['Year Built / Deliver Year']

    df['Age'].dtype

    df.loc[df['Age']<=80]

    df.loc[df['Age'].isna()]

    df['Age'] = df['Age'].fillna(df['Age'].median())

    df['Age'] = df['Age'].astype(int)

    df.drop('Year Built / Deliver Year', axis=1, inplace=True)

    """Number of Rooms"""

    df.loc[df['Room'].isna()]

    df.loc[ df['Room'] == ' label.rooms.plus10', 'Room'] = '10'
    df.loc[ df['Room'] == 'label.rooms.plus10', 'Room'] = '10'

    df.loc[ df['Room'] == '.+3.', 'Room'] = '3'
    df.loc[ df['Room'] == ' 15th', 'Room'] = '15'
    df.loc[ df['Room'] == '15th', 'Room'] = '15'

    df = df.drop(df[df['Room']=='180'].index)
    df = df.drop(df[df['Listing ID']==' EG-3584724'].index)

    df['Room']= df['Room'].fillna(df['Room'].median())

    df['Room'] = df['Room'].astype(int)

    df = df[df['Room']<=20]

    """Number of Bathrooms"""

    print(df['Baths'].unique())

    df.loc[df['Baths']=='label.rooms.plus10']

    df.loc[ df['Baths'] == ' 15th', 'Baths'] = '15'
    df.loc[ df['Baths'] == '15th', 'Baths'] = '15'

    df = df.drop(df[df['Baths']==' label.rooms.plus10'].index)
    df = df.drop(df[df['Listing ID']=='EG-3427274'].index)
    df = df.drop(df[df['Baths']=='label.rooms.plus10'].index)

    df['Baths']= df['Baths'].fillna(df['Baths'].median())

    df['Baths'] = df['Baths'].astype(int)

    df = df[df['Baths']<=10]
    df = df[df['Baths']>0]

    """#ENCODING

    Doing enconding for categorical values in the dataset
    """

    label_encoder = preprocessing.LabelEncoder()
    
    df['seller_LE']= label_encoder.fit_transform(df['Seller Role'])
    df['type_LE']= label_encoder.fit_transform(df['Building Type'])
    df['finish_type_LE']= label_encoder.fit_transform(df['Finish Type'])
    df['view_LE']= label_encoder.fit_transform(df['View'])
    df['payement_LE']= label_encoder.fit_transform(df['Payment Method'])

    """#Address

    extracting the area
    """

    areas = ["New Cairo", "Fifth Settlement", "North Coast", "Sheikh Zayed", "Heliopolis", "Smouha", "Nasr City", "Dokki", "Sherouk", "Giza", "6th of October", "Mokattam", "Zamalek", "New Alamein", "Maadi", "Alexandria", "Manial", "Mohandessin","Greater Cairo", "New Administrative Capital" , "Gouna", "Ain Sokhna","Hurghada","Obour","Tanta","Mansoura","Assuit"]

    df["Address"] = df["Address"].astype(str)

    df["new_address"] = df.apply(lambda col: [area for area in areas if area in col["Address"]], axis=1)

    print(df['new_address'])

    count = 0
    for i in df['new_address']:
        if i == []:
            count+=1

    count

    df['new_address'] = df['new_address'].astype(str)

    df['new_address'].dtype

    df['new_address'] = [e.split(',')[0]+"]" if ',' in e else e for e in df['new_address']]

    print(df['new_address'].unique())

    df.drop(df.loc[df['new_address']=='[]'].index, inplace=True)

    """new address encoding"""

    df['Address_LE']= label_encoder.fit_transform(df['new_address'])

    print(df['Address_LE'].unique())

    """#Regression principles

    Checking for multicollinearity
    """

    c = [
        'seller_LE',
        'type_LE',
        'finish_type_LE', 
        'view_LE',
        'Area', 
        'Age',
        'Room',
        'Baths', 
        'payement_LE',
        'Address_LE'
        ]
    x=df[c]


    vif_data = pd.DataFrame()
    vif_data["feature"] = x.columns
    vif_data["VIF"] = [variance_inflation_factor(x.values, i) for i in range(len(x.columns))]

    vif_data

    y=df['Price_NEW']

    regr= LinearRegression()
    x_tr, x_te, y_tr, y_te = train_test_split(x, y,test_size=0.2,random_state = 4)
    regr.fit(x_tr,y_tr)

    y_pred = regr.predict(x_te)

    error= y_te-y_pred

    np.round(np.sum(error),2),np.round(np.mean(error),2)

    """#Deep Model"""



    c = ['seller_LE', 'type_LE', 'finish_type_LE', 'view_LE', 'Area', 'Age', 'Room', 'Baths', 'payement_LE', 'Address_LE']
    x=df[c]
    y=df['Price_NEW']

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.1)


    scaler = StandardScaler().fit(pd.concat([X_train,X_test],axis=0))
    # X_train = pd.DataFrame(scaler.fit_transform(X_train), columns = X_train.columns)
    # X_test = pd.DataFrame(scaler.transform(X_test), columns = X_test.columns)

    # X_train

    # X_train[:5]

    """XG boost"""

    params = {
        'nthread':[4], 
        'objective':['reg:linear'],
        'learning_rate': [0.03], 
        'max_depth': [20],
        'min_child_weight': [4],
        'silent': [1],
        'subsample': [0.7],
        'colsample_bytree': [0.7],
        'n_estimators': [500], 
            }

    regr = XGBRegressor(random_state=2)
    regr = GridSearchCV(regr, params, cv=5)
    regr.fit(X_train, y_train)

    # regr.predict(X_test)


    # preds = regr.predict(X_test)

    # for pred, target in zip(preds,y_test):
    #     print("Prediction:{} - Target: {}".format(pred,target))

    # scores = regr.score(X_test,y_test)

    # print(regr.best_score_)
    # print(regr.best_params_)

    # preds = regr.predict(X_test)

    # train_preds = regr.predict(X_train)

    # print(r2_score(train_preds, y_train))
    

    # accuracy = explained_variance_score(y_test, preds)



    # max_error(y_test, preds)

    # df.reset_index(drop=True)
def runmodel(srole,btype,finishtype,view,area,year,rooms,baths,payment,Address):

    srole=getsellerencoding(df,srole)
    btype= gettypeencoding(df,btype)
    finishtype=getfinishtypeencoding(df,finishtype)
    view=getviewencoding(df,view)
    Age=getage(year)
    Address=getAddressencoding(df,Address)
    payment=getpaymentecoding(df,payment)
    # x={'Area':[200], 'finish_type_LE':[finishtype], 'Room':[4], 'Age':[Age], 'type_LE':[btype],
    #     'Baths':[4], 'view_LE':[view], 'seller_LE':[srole], 'payement_LE':[payement], 'Address_LE':[Address]}
    x={'seller_LE':[srole], 'type_LE':[btype], 'finish_type_LE':[finishtype],'view_LE':[view], 'Area':[area], 'Age':[Age], 'Room':[rooms],  
        'Baths':[baths],  'payement_LE':[payment], 'Address_LE':[Address]}

    x=pd.DataFrame(x)
    new = regr.predict(x)
    print(new[0])
    return new[0]



if __name__ == '__main__':
    runmodel()