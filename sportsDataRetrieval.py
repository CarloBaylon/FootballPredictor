'''
Created on Oct 26, 2021

@author: wvoli
'''

import requests
import csv

    
    # f = open('C:\Users\wvoli\Desktop\pastnflseasonschedules.csv', 'w')
    # writer = csv.writer(f)
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
    new_dict = {'HomeTeam': '', 'AwayTeam': '','HomeScore': '', 'AwayScore': '', 'Date': '', 'PointSpread': '', 'Penalties': '', 'OpponentPenalties': '', 'TurnoverDifferential': '', 'OpponentTurnoverDifferential': '', 'result': ''}
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
        if x['Score'] <= x['OpponentScore']:
            new_dict['result'] = 1
        else: 
            new_dict['result'] = 0
        list_of_dicts_Scores.append(new_dict)
        new_dict = {}
    return list_of_dicts_Scores
    
    # list_of_dicts_Standings = []
    # for z in t_dictionary:
    #     if not z['AwayTeam'] == 'BYE' and z['HomeTeam'] == 'NE' or z['AwayTeam'] == 'NE':
    #         new_dict3['WinningPercentage'] = z['WinningPercentage']
    #         list_of_dicts_Standings.append(new_dict3)
    #         new_dict3 = {}
    # return list_of_dicts_Standings
# print(list_of_dicts)

# def pullTeamStats(year, week):
#     s = requests.get( 'https://api.sportsdata.io/v3/nfl/scores/json/TeamGameStats/' + year + '?key=2c62d512a5c8434f89ea5d272d31531b')
#     s_dictionary = s.json()
#
#     new_dict2 = {'Penalties': '', 'OpponentPenalties': '', 'TurnoverDifferential': '', 'OpponentTurnoverDifferential': ''}
#
#     list_of_dicts_team = []
#     for y in s_dictionary:
#         if not y['Opponent'] == 'BYE' and y['Team'] == 'NE' or y['Opponent'] == 'NE':
#
#             list_of_dicts_team.append(new_dict2)
#             new_dict2 = {}
#     return list_of_dicts_team
            
if __name__ == "__main__":
    fieldNames = ['HomeTeam', 'HomeScore', 'AwayTeam', 'AwayScore', 'Date', 'PointSpread', 'OpponentPenalties', 'OpponentTurnoverDifferential', 'TurnoverDifferential', 'Penalties', 'result']
    with open(r'C:\Users\wvoli\Desktop\pastnflseasonschedules.csv', 'w', encoding='UTF8', newline='') as f:
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
    
        
            
            