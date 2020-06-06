# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 19:16:04 2020

@author: Stefan Klug
"""


import sqlalchemy as db
import pandas as pd

##################
# Daten einlesen #
##################

kreise_sterberate       = pd.read_csv("../data/01_RKI_Kreise_Sterberate.csv")

kreise_altersverteilung = pd.read_csv("../data/01_Kreise_Altersverteilung_Fläche.csv")

kreise_AOK              = pd.read_csv("../data/01_AOK_aufbereitet.csv")

gesamt                  = pd.read_csv("../data/02_Daten_merged.csv")

kreise_altersverteilung.drop(columns='Unnamed: 0', inplace=True)
kreise_AOK.drop(columns='Unnamed: 0', inplace=True)
gesamt.drop(columns='Unnamed: 0', inplace=True)

############################
# Verbindung mit Datenbank #
############################

engine  = db.create_engine('mysql://ateam:5araPGQ7TTjHSKo6BHxO4fdDk5C2MDKyQvnVC7Sb@37.221.198.242:3308/data_science')
con     = engine.connect()

#########################
# beladen der Datenbank #
#########################

kreise_sterberate.to_sql(name='kreise_sterberate',          con=engine, if_exists='replace',
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

kreise_altersverteilung.to_sql(name='kreise_altersverteilung', con=engine, if_exists='replace',
                               dtype={"ID_LK_SK":              db.types.INTEGER(),
                                      "age_0_34_%":            db.types.Float(precision=3, asdecimal=True),
                                      "age_35_59_%":           db.types.Float(precision=3, asdecimal=True),
                                      "age_60+_%":             db.types.Float(precision=3, asdecimal=True),
                                      "Einw_pro_qm":           db.types.Float(precision=3, asdecimal=True)})

kreise_AOK.to_sql(name='kreise_AOK', con=engine, if_exists='replace',
                  dtype={"ID_LK_SK":                                                   db.types.INTEGER(),
                         "Kreisname":                                                  db.types.NVARCHAR(length=150),
                         "Prävalenz (Anteil mit mindestens einer Vorerkrankung in %)": db.types.Float(precision=3, asdecimal=True),
                         "Prävalenz-Schätzwerte plausibles Intervall Untergrenze":     db.types.Float(precision=3, asdecimal=True),
                         "Prävalenz-Schätzwerte plausibles Intervall Obergrenze":      db.types.Float(precision=3, asdecimal=True)})

gesamt.to_sql(name='Gesamt',                     con=engine, if_exists='replace',
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

########################
# Test: Daten auslesen #
########################

metadata    = db.MetaData()
table       = db.Table('kreise_sterberate', metadata, autoload=True, autoload_with=engine)
query       = db.select([table])
results     = con.execute(query).fetchall()
df          = pd.DataFrame(results)
df.columns  = results[0].keys()
df.info()

