import numpy as np
import xgboost as xgb
import pandas as pd
import requests
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('pastnflseasonschedules.csv')

def pullDataFromYear(year, week):
    # r = requests.get('https://api.sportsdata.io/v3/nfl/scores/json/Scores/' + year + '?key=2c62d512a5c8434f89ea5d272d31531b')
    #
    # t = requests.get(' https://api.sportsdata.io/v3/nfl/scores/json/Standings/' + year + '?key=2c62d512a5c8434f89ea5d272d31531b')
    # # print(r.url)
    # r_dictionary = r.json()
    #
    # t_dictionary = t.json()
    # new_dict3 = {'WinningPercentage': ''}
    s = requests.get('https://api.sportsdata.io/v3/nfl/scores/json/TeamGameStats/'+ year + '/' + week + '?key=2c62d512a5c8434f89ea5d272d31531b')
    s_dictionary = s.json()
    new_dict = {'HomeTeam': '', 'AwayTeam': '','HomeScore': '', 'AwayScore': '', 'Date': '', 'PointSpread': '', 'Penalties': '', 'OpponentPenalties': '', 'TurnoverDifferential': '', 'OpponentTurnoverDifferential': ''}
    list_of_dicts_Scores = []
    for x in s_dictionary:
        # if not x['Opponent'] == 'BYE' or : and x['Team'] == 'NE' or x['Opponent'] == 'NE':
        new_dict['HomeTeam'] = x['Team']
        new_dict['HomeScore'] = x['Score']
        new_dict['AwayTeam'] = x['Opponent']
        new_dict['AwayScore'] = x['OpponentScore']
        new_dict['Date'] = x['Date']
        new_dict['PointSpread'] = x['PointSpread']
        new_dict['Penalties'] = x['Penalties']
        new_dict['OpponentPenalties'] = x['OpponentPenalties']
        new_dict['TurnoverDifferential'] = x['TurnoverDifferential']
        new_dict['OpponentTurnoverDifferential'] = x['OpponentTurnoverDifferential']
        list_of_dicts_Scores.append(new_dict)
        new_dict = {}
    return list_of_dicts_Scores
    
            

def display(y_pred,X_test):
    for g in range(len(y_pred)):
        win_prob = round(y_pred[g],2)
        away_team = X_test.reset_index().drop(columns = 'index').loc[g,'AwayTeam']
        home_team = X_test.reset_index().drop(columns = 'index').loc[g,'HomeTeam']
        print(f'The {away_team} have a probability of {win_prob} of beating the {home_team}.') 
   
msk = np.random.rand(len(df)) < 0.8

train_df = df[msk]
test_df = df[~msk]

X_train = train_df.drop(columns = ['AwayTeam', 'HomeTeam', 'Date','result'])
y_train = train_df[['result']] 
X_test = test_df.drop(columns = ['AwayTeam', 'HomeTeam', 'Date','result'])
y_test = test_df[['result']]

clf = LogisticRegression(penalty='l1', dual=False, tol=0.001, C=1.0, fit_intercept=True, 
                   intercept_scaling=1, class_weight='balanced', random_state=None, 
                   solver='liblinear', max_iter=1000, multi_class='ovr', verbose=0)

clf.fit(X_train, np.ravel(y_train.values))
y_pred = clf.predict_proba(X_test)
y_pred = y_pred[:,1]

display(y_pred,test_df)
accuracy_score(y_test,np.round(y_pred))

dtest = xgb.DMatrix(X_test, y_test, feature_names=X_test.columns)
dtrain = xgb.DMatrix(X_train, y_train,feature_names=X_train.columns)

param = {'verbosity':1, 
         'objective':'binary:hinge',
         'feature_selector': 'shuffle',
         'booster':'gblinear',
         'eval_metric' :'error',
         'learning_rate': 0.05}

evallist = [(dtrain, 'train'), (dtest, 'test')]

num_round = 1000
bst = xgb.train(param, dtrain, num_round, evallist)


X_test = pred_games_df.drop(columns = ['AwayTeam', 'HomeTeam', 'Date','result'])
y_pred = clf.predict_proba(X_test)
y_pred = y_pred[:,1]



if __name__ == "__main__":
    fieldNames = ['HomeTeam', 'HomeScore', 'AwayTeam', 'AwayScore', 'Date', 'PointSpread', 'OpponentPenalties', 'OpponentTurnoverDifferential', 'TurnoverDifferential', 'Penalties']
    with open(r'pastnflseasonschedules.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()
        # for i in range(1,17):
        #     listOf2019 = pullDataFromYear('2019', str(i))
        #     writer.writerows(listOf2019)
        # for i in range(1,17):
        #     listOf2020 = pullDataFromYear('2020', str(i))
        #     writer.writerows(listOf2020)
        # for i in range(1,17):
        listOf2021 = pullDataFromYear('2021', '10')
        writer.writerows(listOf2021)
        print(df)
        display(y_pred,pred_games_df)

