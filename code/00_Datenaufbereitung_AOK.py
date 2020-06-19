# -*- coding: utf-8 -*-
"""
Created on Thu May 28 09:45:21 2020

@author: Luis Hohmann
"""

import pandas as pd
import sqlalchemy as db

################################################################################
# AOK Daten: 00_Anteil_Einwohner_Deutschland_mit_ausgewaehlten_Vorerkrankungen # 
################################################################################

##################
# Daten einlesen #
##################

df = pd.read_csv(filepath_or_buffer="../data/00_Anteil_Einwohner_Deutschland_mit_ausgewaehlten_Vorerkrankungen.csv", sep=';') 

###############################
# Objekt zu flaot formatieren #
###############################

df["Prävalenz"] = df["Prävalenz"].str.replace(',','.').astype(float)

##################################################
# Intervall in obere und untere Grenze aufteilen #
##################################################

# Intervall bei '-' aufteilen
split = df["plausibles Intervall"].str.split(" - ", n=-1, expand = True)

# obere und untere Grenze des Intervalls in Datensatz einfügen
df["Prävalenz_plausibles_Intervall_untere_Grenze"] = split[0].str.replace(',','.').astype(float)
df["Prävalenz_plausibles_Intervall_obere_Grenze"]  = split[1].str.replace(',','.').astype(float)

########################
# Datensatz bearbeiten #
########################

# Spalten löschen
df.drop(columns=['plausibles Intervall', 'Patientenanzahl (gerundet)', 'BL', 'BL_NAME', 'KREIS_NAME'], inplace=True)

# Spalte umbenennen
df.rename(columns={"KREIS": "ID_LK_SK"}, inplace=True)

#####################
# Daten exportieren #
#####################

df.to_csv("../data/01_AOK_ausgewaehlten_Vorerkrankungen.csv")

#####################
# Datenbank beladen # 
#####################

engine = db.create_engine('mysql://ateam:5araPGQ7TTjHSKo6BHxO4fdDk5C2MDKyQvnVC7Sb@37.221.198.242:3308/data_science')
con    = engine.connect()

df.to_sql(name='AOK_ausgewaehlten_Vorerkrankungen', con=engine, if_exists='replace',
          dtype={"ID_LK_SK":                                     db.types.INTEGER(),
                 "Prävalenz":                                    db.types.Float(precision=3, asdecimal=True),
                 "Prävalenz_plausibles_Intervall_untere_Grenze": db.types.Float(precision=3, asdecimal=True),
                 "Prävalenz_plausibles_Intervall_obere_Grenze":  db.types.Float(precision=3, asdecimal=True)})

########################################################################################################################################
# AOK Daten: 00_Anteil_Einwohner_Deutschland_mit_mindestens_einer_Vorerkrankung _mit_erhöhtem_Risiko_für_schwere_Verläufe_von_COVID-19 # 
########################################################################################################################################

##################
# Daten einlesen #
##################

df2 = pd.read_csv(filepath_or_buffer="../data/00_Anteil_Einwohner_Deutschland_mit_mindestens_einer_Vorerkrankung _mit_erhöhtem_Risiko_für_schwere_Verläufe_von_COVID-19.csv", sep=';') 

################################
# Objekte zu flaot formatieren #
################################

df2["Bluthochdruck"]     = df2["Bluthochdruck"].str.replace(',','.').astype(float)
df2["KHK"]               = df2["KHK"].str.replace(',','.').astype(float)
df2["Herzinfarkt"]       = df2["Herzinfarkt"].str.replace(',','.').astype(float)
df2["Herzinsuffizienz"]  = df2["Herzinsuffizienz"].str.replace(',','.').astype(float)
df2["Schlaganfall"]      = df2["Schlaganfall"].str.replace(',','.').astype(float)
df2["Diabetes"]          = df2["Diabetes"].str.replace(',','.').astype(float)
df2["Asthma"]            = df2["Asthma"].str.replace(',','.').astype(float)
df2["COPD"]              = df2["COPD"].str.replace(',','.').astype(float)
df2["Krebs"]             = df2["Krebs"].str.replace(',','.').astype(float)
df2["Lebererkrankungen"] = df2["Lebererkrankungen"].str.replace(',','.').astype(float)
df2["Immunschwäche"]     = df2["Immunschwäche"].str.replace(',','.').astype(float)

########################
# Datensatz bearbeiten #
########################

# Spalten löschen
df2.drop(columns=['BL', 'BL_NAME', 'KREIS_NAME'], inplace=True)

# Spalte umbenennen
df2.rename(columns={"KREIS": "ID_LK_SK"}, inplace=True)

#####################
# Daten exportieren #
#####################

df2.to_csv("../data/01_AOK_mindestens_eine_Vorerkrankung_schwere_Verläufe.csv")

#####################
# Datenbank beladen # 
#####################

engine = db.create_engine('mysql://ateam:5araPGQ7TTjHSKo6BHxO4fdDk5C2MDKyQvnVC7Sb@37.221.198.242:3308/data_science')
con    = engine.connect()

df2.to_sql(name='AOK_mindestens_eine_Vorerkrankung_schwere_Verläufe', con=engine, if_exists='replace',
           dtype={"ID_LK_SK":             db.types.INTEGER(),
                  "Bluthochdruck":     db.types.Float(precision=3, asdecimal=True),
                  "KHK":               db.types.Float(precision=3, asdecimal=True),
                  "Herzinfarkt":       db.types.Float(precision=3, asdecimal=True),
                  "Herzinsuffizienz":  db.types.Float(precision=3, asdecimal=True),
                  "Schlaganfall":      db.types.Float(precision=3, asdecimal=True),
                  "Diabetes":          db.types.Float(precision=3, asdecimal=True),
                  "Asthma":            db.types.Float(precision=3, asdecimal=True),
                  "COPD":              db.types.Float(precision=3, asdecimal=True),
                  "Krebs":             db.types.Float(precision=3, asdecimal=True),
                  "Lebererkrankungen": db.types.Float(precision=3, asdecimal=True),
                  "Immunschwäche":     db.types.Float(precision=3, asdecimal=True)})

