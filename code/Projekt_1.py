# -*- coding: utf-8 -*-
"""
Created on Sat May 23 21:18:30 2020

@author: Stefan Klug
"""

import pandas as pd
import numpy  as np

from sklearn.linear_model import LinearRegression

#import matplotlib.pyplot as plt

##################
# Daten einlesen #
##################

data = pd.read_csv("C:/Users/Stefan Klug/OneDrive - Johann Wolfgang Goethe Universität/Master/Data_Science/Projekt/RKI_COVID19.csv")

############################
# Datensatz transformieren #
############################

#################
# Altersgruppen #
#################

columns = ['Landkreis',
           'Altersgruppe',
           'AnzahlFall']

df = data[columns]

tt = df.groupby(['Landkreis', 'Altersgruppe']).sum()

data_frame = tt.unstack(level=-1).droplevel(level=0, axis=1)

data_frame.rename(columns={"A00-A04":   "group_A00-A04",
                           "A05-A14":   "group_A05-A14",
                           "A15-A34":   "group_A15-A34",
                           "A35-A59":   "group_A35-A59",
                           "A60-A79":   "group_A60-A79",
                           "A80+":      "group_A80+",
                           "unbekannt": "group_unknown"}, inplace=True)

##############
# Sterberate #
##############

columns = ['Landkreis',
           'AnzahlTodesfall',
           'AnzahlFall']

df = data[columns]

tt = df.groupby('Landkreis').sum()

tt['Sterberate_%'] = (tt.AnzahlTodesfall / tt.AnzahlFall)*100

data_frame = data_frame.merge(tt, left_index=True, right_index=True)

##############################
# IdLandkreis und Bundesland #
##############################

columns = ['Landkreis',
           'IdLandkreis',
           'Bundesland']

df = data[columns]

tt = df.drop_duplicates(keep='first',inplace=False)

tt.set_index(keys='Landkreis', drop=True, append=False, inplace=True, verify_integrity=False)

data_frame = data_frame.merge(tt, left_index=True, right_index=True)

###################
# nach Geschlecht #
###################

columns = ['Landkreis',
           'Geschlecht']

df = data[columns]

tt = df.groupby('Landkreis')['Geschlecht'].value_counts()

tt = tt.unstack(level=-1)

tt.rename(columns={"M": "gender_m", "W": "gender_f", "unbekannt": "gender_unknown"}, inplace=True)

data_frame = data_frame.merge(tt, left_index=True, right_index=True)

##############
# LK oder SK #
##############

# Region Hannover zu LK Hannover ändern -> war früher ein Landkreis
# https://de.wikipedia.org/wiki/Region_Hannover

data_frame.rename(index={'Region Hannover':'LK Hannover'}, inplace=True)

# StadtRegion Aachen zu LK Aachen ändern -> war früher ein Landkreis bzw. wurde mir der Stadt Aachen zusammengelegt
# https://de.wikipedia.org/wiki/Kreis_Aachen

data_frame.rename(index={'StadtRegion Aachen':'LK Aachen'}, inplace=True)

data_frame['LK_SK'] = data_frame.index.str[:2]

##############
# neu ordnen #
##############

cols = ['IdLandkreis',
        'LK_SK',
        'Bundesland',
        'group_A00-A04',
        'group_A05-A14',
        'group_A15-A34',
        'group_A35-A59',
        'group_A60-A79',
        'group_A80+',
        'group_unknown',
        'gender_m',
        'gender_f',
        'gender_unknown',
        'AnzahlFall',
        #'AnzahlTodesfall',
        'Sterberate_%']

data_frame = data_frame[cols]

#################################
# Missing Values mit 0 befüllen #
#################################

cols = ['group_A00-A04',
        'group_A05-A14',
        'group_A15-A34',
        'group_A35-A59',
        'group_A60-A79',
        'group_A80+',
        'group_unknown',
        'gender_m',
        'gender_f',
        'gender_unknown',
        'AnzahlFall']

for col in cols:
    data_frame[col].fillna(value=0, inplace=True)
    
    
sterberate_bundesland = data_frame.groupby('Bundesland')['Sterberate_%'].mean()

sterberate_LK_SK = data_frame.groupby('LK_SK')['Sterberate_%'].mean()

###################
# Dummy Codierung #
###################

dummies_LK = pd.get_dummies(data_frame['LK_SK'])

dummies_Bundesland = pd.get_dummies(data_frame['Bundesland'])

data_frame['LK_SK'] = dummies_LK.LK

for col in dummies_Bundesland.columns:
    data_frame[col] = dummies_Bundesland[col]
    

cols_input = [#'IdLandkreis',
              'LK_SK',
              'Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen',
              'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen',
              'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen',
              'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen',
              'group_A00-A04',
              'group_A05-A14',
              'group_A15-A34',
              'group_A35-A59',
              'group_A60-A79',
              'group_A80+',
              'group_unknown',
              'gender_m',
              'gender_f',
              'gender_unknown',
              'AnzahlFall']

X = data_frame[cols_input]
y = data_frame['Sterberate_%']*10

reg = LinearRegression().fit(X, y)
reg.score(X, y)

coefficients = pd.concat([pd.DataFrame(X.columns),pd.DataFrame(np.transpose(reg.coef_))], axis = 1)

#tt.reset_index(level=0, inplace=True)
#tt.reset_index(level=0, inplace=True)
#transposed = tt.groupby('Landkreis')['Altersgruppe'].apply(lambda tt: tt.reset_index(drop=True)).unstack()



#tt_transposed = tt['Altersgruppe'].transpose()

#test = data[['Bundesland', 'AnzahlFall']]

#tt = test.groupby(['Bundesland']).sum()
