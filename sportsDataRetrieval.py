'''
Created on Oct 26, 2021

@author: wvoli
'''

import requests
import csv

    
    # f = open('C:\Users\wvoli\Desktop\pastnflseasonschedules.csv', 'w')
    # writer = csv.writer(f)
def pullDataFromYear(year):
    r = requests.get('https://api.sportsdata.io/v3/nfl/scores/json/Scores/' + year + '?key=2c62d512a5c8434f89ea5d272d31531b')
    # print(r.url)
    r_dictionary = r.json()
    new_dict = {'HomeTeam': '', 'AwayTeam': '','HomeScore': '', 'AwayScore': '', 'Date': '', 'PointSpread': ''}
    list_of_dicts = []
    for x in r_dictionary:
        if not x['AwayTeam'] == 'BYE' and x['HomeTeam'] == 'NE' or x['AwayTeam'] == 'NE':
            new_dict['HomeTeam'] = x['HomeTeam']
            new_dict['HomeScore'] = x['HomeScore']
            new_dict['AwayTeam'] = x['AwayTeam']
            new_dict['AwayScore'] = x['AwayScore']
            new_dict['Date'] = x['Date']
            new_dict['PointSpread'] = x['PointSpread']
            list_of_dicts.append(new_dict)
            new_dict = {}
    return list_of_dicts
        
# print(list_of_dicts)
if __name__ == "__main__":
    listOf2019 = pullDataFromYear('2019')
    listOf2020 = pullDataFromYear('2020')
    listOf2021 = pullDataFromYear('2021')
    fieldNames = ['HomeTeam', 'HomeScore', 'AwayTeam', 'AwayScore', 'Date', 'PointSpread']
    with open(r'C:\Users\wvoli\Desktop\pastnflseasonschedules.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(listOf2019)
        writer.writerows(listOf2020)
        writer.writerows(listOf2021)
        
            
            