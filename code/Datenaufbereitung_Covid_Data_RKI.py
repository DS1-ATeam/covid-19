# -*- coding: utf-8 -*-
"""
Created on Tue May 26 21:27:31 2020

@author: Stefan Klug
"""

import pandas as pd

##################
# Daten einlesen #
##################

# RKI Datensatz
data = pd.read_csv("C:/Users/Stefan Klug/data-science-project/data/RKI_COVID19.csv")

# https://www-genesis.destatis.de/genesis/online#astructure


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

temp = df.groupby(['Landkreis', 'Altersgruppe']).sum()

data_frame = temp.unstack(level=-1).droplevel(level=0, axis=1)

#data_frame.rename(columns={"A00-A04":   "group_A00-A04",
#                           "A05-A14":   "group_A05-A14",
#                           "A15-A34":   "group_A15-A34",
#                           "A35-A59":   "group_A35-A59",
#                           "A60-A79":   "group_A60-A79",
#                           "A80+":      "group_A80+",
#                           "unbekannt": "group_unknown"}, inplace=True)

# Missings mit 0 befüllen
data_frame.fillna(value=0, inplace=True)

data_frame["age_covid_0_34"]    = data_frame["A00-A04"] + data_frame["A05-A14"] + data_frame["A15-A34"]

data_frame["age_covid_35_59"]   = data_frame["A35-A59"]

data_frame["age_covid_60+"]     = data_frame["A60-A79"] + data_frame["A80+"]

data_frame["age_covid_unknown"] = data_frame["unbekannt"]

data_frame["sum"] = data_frame["age_covid_0_34"] + data_frame["age_covid_35_59"] + data_frame["age_covid_60+"] + data_frame["age_covid_unknown"]

data_frame["age_covid_0_34_%"]    = (data_frame["age_covid_0_34"]       / data_frame["sum"]) * 100

data_frame["age_covid_35_59_%"]   = (data_frame["age_covid_35_59"]      / data_frame["sum"]) * 100

data_frame["age_covid_60+_%"]     = (data_frame["age_covid_60+"]        / data_frame["sum"]) * 100

data_frame["age_covid_unknown_%"] = (data_frame["age_covid_unknown"]    / data_frame["sum"]) * 100

data_frame.drop(columns=["A00-A04", "A05-A14", "A15-A34", "A35-A59", "A60-A79", "A80+", "unbekannt",
                         "age_covid_0_34", "age_covid_35_59", "age_covid_60+", "age_covid_unknown", "sum"], inplace=True)


##############
# Sterberate #
##############

columns = ['Landkreis',
           'AnzahlTodesfall',
           'AnzahlFall']

df = data[columns]

temp = df.groupby('Landkreis').sum()

temp['Sterberate_%'] = (temp.AnzahlTodesfall / temp.AnzahlFall)*100

data_frame = data_frame.merge(temp, left_index=True, right_index=True)

data_frame.drop(columns=["AnzahlTodesfall", "AnzahlFall"], inplace=True)

##############################
# IdLandkreis und Bundesland #
##############################

columns = ['Landkreis',
           'IdLandkreis',
           'Bundesland']

df = data[columns]

temp = df.drop_duplicates(keep='first',inplace=False)

temp.set_index(keys='Landkreis', drop=True, append=False, inplace=True, verify_integrity=False)

data_frame = data_frame.merge(temp, left_index=True, right_index=True)

###################
# nach Geschlecht #
###################

columns = ['Landkreis',
           'Geschlecht']

df = data[columns]

temp = df.groupby('Landkreis')['Geschlecht'].value_counts()

temp = temp.unstack(level=-1)

temp.rename(columns={"M": "gender_m", "W": "gender_f", "unbekannt": "gender_unknown"}, inplace=True)

data_frame = data_frame.merge(temp, left_index=True, right_index=True)

# Missings mit 0 befüllen
data_frame["gender_m"].fillna(value=0, inplace=True)
data_frame["gender_f"].fillna(value=0, inplace=True)
data_frame["gender_unknown"].fillna(value=0, inplace=True)

data_frame["sum_gender"] = data_frame["gender_m"] + data_frame["gender_f"] + data_frame["gender_unknown"]

data_frame["gender_covid_m_%"]        = (data_frame["gender_m"] / data_frame["sum_gender"]) * 100

data_frame["gender_covid_f_%"]        = (data_frame["gender_f"] / data_frame["sum_gender"]) * 100

data_frame["gender_covid_unknown_%"]  = (data_frame["gender_unknown"] / data_frame["sum_gender"]) * 100

data_frame.drop(columns=["sum_gender", "gender_m", "gender_f", "gender_unknown"], inplace=True)

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
        'age_covid_0_34_%',
        'age_covid_35_59_%',
        'age_covid_60+_%',
        'age_covid_unknown_%',
        'gender_covid_f_%',
        'gender_covid_m_%',
        'gender_covid_unknown_%',
        'Sterberate_%']

data_frame = data_frame[cols]

data_frame.rename(columns={'IdLandkreis': 'ID_LK_SK'}, inplace=True)

data_frame.to_csv("C:/Users/Stefan Klug/data-science-project/data/Kreise_Sterberate.csv")