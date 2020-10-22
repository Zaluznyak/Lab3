# -*- coding: utf-8 -*-
"""
Created on Tue Oct 6 17:15:21 2020

@author: Сергей
"""

import requests
import json
import time
import re
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup as bs
from collections import Counter
 
""" ПАРСИНГ """
# def getPage(page = 0):
#     """
#     Создаем метод для получения страницы со списком вакансий.
#     Аргументы:
#         page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
#     """
     
#     # Справочник для параметров GET-запроса
#     params = {
#         'text': 'NAME:IT', # Текст фильтра. В имени должно быть слово "Аналитик"
#         'area': [1,2], # Поиск ощуществляется по вакансиям города Москва,СПБ
#         'page': page, # Индекс страницы поиска на HH
#         'per_page': 100 # Кол-во вакансий на 1 странице
#     }
     
     
#     req = requests.get('https://api.hh.ru/vacancies', params) # Посылаем запрос к API
#     data = req.content.decode() # Декодируем его ответ, чтобы Кириллица отображалась корректно
#     req.close()
#     return data


# def ReadWriteVac(clmn, vacance):
#     req = requests.get(f'https://api.hh.ru/vacancies/{vacance["id"]}') 
#     data = req.content.decode()
#     jsObj1 = json.loads(data)
#     o = t = u = -10
#     flag = True
#     try:
#         Vname = jsObj1['name']
#         city = None
#         minSalary = None
#         maxSalary = None
#         Cname = None
#         skills = ''
#         exp = None
#         employ = None
#         jobgraph = None
#         desc = None
#         duties = None
#         terms = None
#         requirements = None
#         date = jsObj1['published_at']

        
#         for i in jsObj1['key_skills']:
#             skills+=f' {i["name"]};'
#         if jsObj1['area'] is not None:
#             city = jsObj1['area']['name']
#         if jsObj1['salary'] is not None:
#             minSalary = jsObj1['salary']['from']
#             maxSalary = jsObj1['salary']['to']
#         if jsObj1['employer'] is not None:
#             Cname = jsObj1['employer']['name']
#         if jsObj1['experience'] is not None:
#             exp = jsObj1['experience']['name']
#         if jsObj1['employment'] is not None:
#             employ = jsObj1['employment']['name']
#         if jsObj1['schedule'] is not None:
#             jobgraph = jsObj1['schedule']['name']
        
#         descrip = jsObj1['description']
#         soup = bs(descrip, "html.parser")
#         for p in soup:
#             if (flag and str(p).lower().find('обязанности')==-1 and 
#                         str(p).lower().find('условия')==-1 and 
#                         str(p).lower().find('обязанности')==-1):
#                         desc = re.sub('<[^<]+?>', ' ', str(p))
#                         flag = False
#             if (o==-1):
#                 duties = re.sub('<[^<]+?>', ' ', str(p))
#             if (t==-1):
#                 requirements = re.sub('<[^<]+?>', ' ', str(p))
#             if (u==-1):
#                 terms = re.sub('<[^<]+?>', ' ', str(p))
            
#             if str(p).lower().find('обязанности')!=-1:
#                 o=1
#             if str(p).lower().find('требования')!=-1:
#                 t=1
#             if str(p).lower().find('условия')!=-1:
#                 u=1
#             o-=1
#             t-=1
#             u-=1
#     except:
#         print('Пропущена запись')
#     req.close()
#     return [pd.Series([Vname, city, minSalary, maxSalary,
#             date, exp, employ, jobgraph, desc,
#             duties, requirements, terms, skills], index = clmn)]
# df = pd.DataFrame({
#      'Vac_name':[],
#      'City':[],
#      'From_salary':[],
#      'To_salary':[],
#      'Date':[],
#      'Expirience':[],
#      'Employment':[],
#      'Work_schedule':[],
#      'Descriptions':[],
#      'Duties':[],
#      'Requiremenst':[],
#      'Terms':[],
#      'Key_skills':[]
#       })
# # Считываем первые 2000 вакансий
# clmn = df.columns
# for page in range(0, 20):
#     jsObj = json.loads(getPage(page))    
#     for item in jsObj['items']:
#        df = df.append(ReadWriteVac(clmn,item), ignore_index=True)
#     if (jsObj['pages'] - page) <= 1:
#         break
#     time.sleep(0.5)
#     print((page+1)*100,' получено')
# df.to_csv('kek.csv')  
# print('Старницы поиска собраны')
"""end ПАРСИНГ"""

""" Работа с готовым csv после парсинга """
print('~~~ЧАСТЬ 2~~~')
df = pd.read_csv('kek.csv')
df['From_salary'] = df['From_salary'].fillna(0)
df['To_salary'] = df['To_salary'].fillna(df['From_salary'])
df = df.sort_values(by='To_salary')
df = df.sort_values(by='From_salary')
max_values=[20000, 60000, 100000,
            140000, 180000, 220000,
            260000, 300000, 340000,
            380000]
df_arr = []
""" 10 групп по максимальной ЗП """
for value in max_values:
    if value == 380000:
        df_arr.append(df[(df['To_salary'] >= value)])
        break
    df_arr.append(df[(df['To_salary'] >= value) & (df['To_salary'] < (value + 40000))])

""" Подсчет для каждой группы """
index=-1
for df_ in df_arr:
    index+=1
    if index!=9:
        print(f'~~~ГРУППА {max_values[index]}-{max_values[index]+40000}~~~')
    else:
        print(f'~~~ГРУППА {max_values[index]}- ... ~~~')
    print('Задание a')
    uniq = df_['Vac_name'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Vac_name'].str.lower() == value])
        print(f' У {value} - {cnt} повт.')
    print('Задание b')
    date_arr = []
    for date in df_['Date']:
        delta = dt.date.today() - dt.datetime.strptime(date.split('T')[0], "%Y-%m-%d").date()
        date_arr.append(int(str(delta).split()[0]))
    print(f'max = {max(date_arr)} min ='
          f' {min(date_arr)} avg = {sum(date_arr)/len(date_arr)}')
    print('Задание c')
    uniq = df_['Expirience'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Expirience'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    print('Задание d')
    uniq = df_['Employment'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Employment'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    print('Задание e')
    uniq = df_['Work_schedule'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Work_schedule'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    print('Задание f')
    key_skills = []
    for value in df_['Key_skills']:
        val_arr = str(value).split(';')
        for v in val_arr:
            key_skills.append(v.lower())
    key_skills = [value for value in key_skills if value]
    print(Counter(key_skills))
print('~~~Часть 3~~~')

df_arr = []
uniq = df['Vac_name'].str.lower().unique()
"""Группы по имю вакансии """
for value in uniq:
    df_arr.append(df[(df['Vac_name'].str.lower() == value)])
for df_ in df_arr:
    print(f'~~~ВАКАНСИЯ {df_["Vac_name"].values[0]}~~~')
    print('Задание 1')
    max_uniq = df_['To_salary'].unique()
    min_uniq = df_['From_salary'].unique()
    for value in max_uniq:
        cnt = len(df_.loc[df['To_salary'] == value])
        print(f' У max {value} - {cnt} повт.')
    for value in min_uniq:
        cnt = len(df_.loc[df['From_salary'] == value])
        print(f' У min {value} - {cnt} повт.')

    print('Задание 2')
    date_arr = []
    for date in df_['Date']:
        delta = dt.date.today() - dt.datetime.strptime(date.split('T')[0], "%Y-%m-%d").date()
        date_arr.append(int(str(delta).split()[0]))
    print(f'max = {max(date_arr)} min ='
          f' {min(date_arr)} avg = {sum(date_arr)/len(date_arr)}')

    print('Задание 3')
    uniq = df_['Expirience'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Expirience'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    
    print('Задание 4')
    uniq = df_['Employment'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Employment'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    
    print('Задание 5')
    uniq = df_['Work_schedule'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Work_schedule'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    
    print('Задание 6')
    key_skills = []
    for value in df_['Key_skills']:
        val_arr = str(value).split(';')
        for v in val_arr:
            key_skills.append(v.lower())
    key_skills = [value for value in key_skills if value]
    print(Counter(key_skills))
print('~~~The END~~~')
