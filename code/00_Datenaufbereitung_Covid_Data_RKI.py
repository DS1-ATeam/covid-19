# -*- coding: utf-8 -*-
"""
@author: ATeam
"""

#########################
# Datenaufbereitung RKI #
#########################

############################
# Bibliotheken importieren #
############################

import pandas as pd
import numpy as np

import sqlalchemy as db

###########################################################
# Daten einlesen                                          #
###########################################################

# Quelle: # https://www-genesis.destatis.de/genesis/online#astructure

# RKI Datensatz
data = pd.read_csv("../data/00_RKI_COVID19_16_06_20.csv")

# Berlin zu SK Berlin zusammenfassen
data["Landkreis"]   = np.where(data.Landkreis.str.contains("Berlin"), 'SK Berlin', data.Landkreis)
data["IdLandkreis"] = np.where(data.Landkreis == "SK Berlin", 11000, data.IdLandkreis)

###########################################################
# Datensatz transformieren                                #
###########################################################

#################
# Altersgruppen #
#################

columns = ['Landkreis',
           'Altersgruppe',
           'AnzahlFall']

df = data[columns]

# Gruppieren nach Landkreis und Altersgruppe 
temp = df.groupby(['Landkreis', 'Altersgruppe']).sum()

# transponieren
data_frame = temp.unstack(level=-1).droplevel(level=0, axis=1)

# Missings mit 0 befüllen
data_frame.fillna(value=0, inplace=True)

# Altersgruppen zusammenfassen
data_frame["age_covid_0_34"]    = data_frame["A00-A04"] + data_frame["A05-A14"] + data_frame["A15-A34"]
data_frame["age_covid_35_59"]   = data_frame["A35-A59"]
data_frame["age_covid_60+"]     = data_frame["A60-A79"] + data_frame["A80+"]
data_frame["age_covid_unknown"] = data_frame["unbekannt"]

# Anzahl der Fälle pro Landkreis
data_frame["sum"] = data_frame["age_covid_0_34"] + data_frame["age_covid_35_59"] + data_frame["age_covid_60+"] + data_frame["age_covid_unknown"]

# Prozentanteil berechnen
data_frame["age_covid_0_34_%"]    = (data_frame["age_covid_0_34"]       / data_frame["sum"]) * 100
data_frame["age_covid_35_59_%"]   = (data_frame["age_covid_35_59"]      / data_frame["sum"]) * 100
data_frame["age_covid_60+_%"]     = (data_frame["age_covid_60+"]        / data_frame["sum"]) * 100
data_frame["age_covid_unknown_%"] = (data_frame["age_covid_unknown"]    / data_frame["sum"]) * 100

# unwichtige Spalten löschen
data_frame.drop(columns=["A00-A04", "A05-A14", "A15-A34", "A35-A59", "A60-A79",       "A80+",              "unbekannt",
                         "age_covid_0_34",     "age_covid_35_59",    "age_covid_60+", "age_covid_unknown", "sum"], inplace=True)

#############################
# Sterberate  pro Landkreis #
#############################

columns = ['Landkreis',
           'AnzahlTodesfall',
           'AnzahlFall']

df = data[columns]

# Gruppieren nach Landkreis
temp = df.groupby('Landkreis').sum()

# Sterberate pro Landkreis
temp['Sterberate_%'] = (temp.AnzahlTodesfall / temp.AnzahlFall)*100

# Daten mergen
data_frame = data_frame.merge(temp, left_index=True, right_index=True)

# unwichtige Spalten löschen
data_frame.drop(columns=["AnzahlTodesfall", "AnzahlFall"], inplace=True)


##############################
# IdLandkreis und Bundesland #
##############################

columns = ['Landkreis',
           'IdLandkreis',
           'Bundesland']

df = data[columns]

# Duplikate löschen: nur einmal Landkreis und dazugehöriges Bundesland
temp = df.drop_duplicates(keep='first',inplace=False)

# setze Landkreis als Index
temp.set_index(keys='Landkreis', drop=True, append=False, inplace=True, verify_integrity=False)

# Daten mergen
data_frame = data_frame.merge(temp, left_index=True, right_index=True)

###################
# nach Geschlecht #
###################

columns = ['Landkreis',
           'Geschlecht']

df = data[columns]

# Gruppieren nach Landkreis: Anzahl der Fälle nach Geschlecht pro Landkreis
temp = df.groupby('Landkreis')['Geschlecht'].value_counts()

# transponiere Zeilen zu Spalten
temp = temp.unstack(level=-1)

# Umbenennen der Spalten
temp.rename(columns={"M": "gender_m", "W": "gender_f", "unbekannt": "gender_unknown"}, inplace=True)

# Daten mergen
data_frame = data_frame.merge(temp, left_index=True, right_index=True)

# Missings mit 0 befüllen
data_frame["gender_m"].fillna(value=0, inplace=True)
data_frame["gender_f"].fillna(value=0, inplace=True)
data_frame["gender_unknown"].fillna(value=0, inplace=True)

# Anzahl aller Fälle berechnen
data_frame["sum_gender"] = data_frame["gender_m"] + data_frame["gender_f"] + data_frame["gender_unknown"]

# Prozentanteil berechnen
data_frame["gender_covid_m_%"]        = (data_frame["gender_m"] / data_frame["sum_gender"]) * 100
data_frame["gender_covid_f_%"]        = (data_frame["gender_f"] / data_frame["sum_gender"]) * 100
data_frame["gender_covid_unknown_%"]  = (data_frame["gender_unknown"] / data_frame["sum_gender"]) * 100

# unwichtige Spalten löschen
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

# Hinzufügen, ob Kreis Landkreis (LK) oder eine kreisfreie Stadt (SK) ist
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

# Spalten neu ordnen
data_frame = data_frame[cols]

# Umbenennen der Spalte IdLandkreis
data_frame.rename(columns={'IdLandkreis': 'ID_LK_SK'}, inplace=True)

#####################
# Daten exportieren #
#####################

data_frame.to_csv("../data/01_RKI_Kreise_Sterberate.csv")

#####################
# Datenbank beladen # 
#####################

engine  = db.create_engine('mysql://ateam:5araPGQ7TTjHSKo6BHxO4fdDk5C2MDKyQvnVC7Sb@37.221.198.242:3308/data_science')
con     = engine.connect()

data_frame.to_sql(name='kreise_sterberate',          con=engine, if_exists='replace',
                  dtype={"Landkreis":                db.types.NVARCHAR(length=100),
                         "ID_LK_SK":                 db.types.INTEGER(),
                         "LK_SK":                    db.types.NVARCHAR(length=5),
                         "Bundesland":               db.types.NVARCHAR(length=100),
                         "age_covid_0_34_%":         db.types.Float(precision=3, asdecimal=True),
                         "age_covid_35_59_%":        db.types.Float(precision=3, asdecimal=True),
                         "age_covid_60+_%":          db.types.Float(precision=3, asdecimal=True),
                         "age_covid_unknown_%":      db.types.Float(precision=3, asdecimal=True),
                         "gender_covid_f_%":         db.types.Float(precision=3, asdecimal=True),
                         "gender_covid_m_%":         db.types.Float(precision=3, asdecimal=True),
                         "gender_covid_unknown_%":   db.types.Float(precision=3, asdecimal=True),
                         "Sterberate_%":             db.types.Float(precision=3, asdecimal=True)})
