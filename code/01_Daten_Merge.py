# -*- coding: utf-8 -*-
"""
Created on Thu May 28 23:35:21 2020

@author: Stefan Klug
"""

import pandas as pd
import sqlalchemy as db

##################
# Daten einlesen #
##################

kreise_sterberate = pd.read_csv("../data/01_RKI_Kreise_Sterberate.csv")

kreise_altersverteilung = pd.read_csv("../data/01_Kreise_Altersverteilung_Fläche.csv")

kreise_AOK = pd.read_csv("../data/01_AOK_aufbereitet.csv")

# unwichtige Spalten löschen
kreise_altersverteilung.drop(['Unnamed: 0'], axis=1, inplace=True)
kreise_AOK.drop(['Unnamed: 0', 'Kreisname'], axis=1, inplace=True)

################
# Daten mergen #
################

# Daten mergen
df_merge = pd.merge(kreise_altersverteilung, kreise_sterberate, on='ID_LK_SK')

# Daten mergen
df_merge = pd.merge(df_merge, kreise_AOK, on='ID_LK_SK')

#####################
# Daten exportieren #
#####################

df_merge.to_csv("../data/02_Daten_merged.csv")

#####################
# Datenbank beladen # 
#####################

engine  = db.create_engine('mysql://ateam:5araPGQ7TTjHSKo6BHxO4fdDk5C2MDKyQvnVC7Sb@37.221.198.242:3308/data_science')
con     = engine.connect()

df_merge.to_sql(name='Gesamt',                     con=engine, if_exists='replace',
                dtype={"ID_LK_SK":                 db.types.INTEGER(),
                       "LK_SK":                    db.types.NVARCHAR(length=5),
                       "Landkreis":                db.types.NVARCHAR(length=100),
                       "Bundesland":               db.types.NVARCHAR(length=100),
                       "age_covid_0_34_%":         db.types.Float(precision=3, asdecimal=True),
                       "age_covid_35_59_%":        db.types.Float(precision=3, asdecimal=True),
                       "age_covid_60+_%":          db.types.Float(precision=3, asdecimal=True),
                       "age_covid_unknown_%":      db.types.Float(precision=3, asdecimal=True),
                       "gender_covid_f_%":         db.types.Float(precision=3, asdecimal=True),
                       "gender_covid_m_%":         db.types.Float(precision=3, asdecimal=True),
                       "gender_covid_unknown_%":   db.types.Float(precision=3, asdecimal=True),
                       "Sterberate_%":             db.types.Float(precision=3, asdecimal=True),
                       "age_0_34_%":               db.types.Float(precision=3, asdecimal=True),
                       "age_35_59_%":              db.types.Float(precision=3, asdecimal=True),
                       "age_60+_%":                db.types.Float(precision=3, asdecimal=True),
                       "Einw_pro_qm":              db.types.Float(precision=3, asdecimal=True),
                       "Prävalenz (Anteil mit mindestens einer Vorerkrankung in %)": db.types.Float(precision=3, asdecimal=True),
                       "Prävalenz-Schätzwerte plausibles Intervall Untergrenze":     db.types.Float(precision=3, asdecimal=True),
                       "Prävalenz-Schätzwerte plausibles Intervall Obergrenze":      db.types.Float(precision=3, asdecimal=True)})
