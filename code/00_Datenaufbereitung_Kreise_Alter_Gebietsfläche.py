# -*- coding: utf-8 -*-
"""
Created on Tue May 26 21:36:49 2020

@author: Stefan Klug
"""

import pandas as pd

import sqlalchemy as db

##################
# Daten einlesen #
##################

# Datensatz Geschlecht, Alter
data = pd.read_csv("../data/00_Kreise_Alter_Geschlecht.csv", sep=';')

# Datensatz Kreise Gebietsfläche
data_flaeche = pd.read_csv("../data/00_Kreise_Gebietsfläche.csv", sep=';', decimal=",")

#####################
# Daten aggregieren #
#####################

# Altersgruppen zusammenfassen
data["age_0_5"]     = data["unter_3_m"] + data["3_6_m"]   + data["unter_3_w"] + data["3_6_w"]
data["age_6_14"]    = data["6_10_m"]    + data["10_15_m"] + data["6_10_w"]    + data["10_15_w"]
data["age_15_34"]   = data["15_18_m"]   + data["18_20_m"] + data["20_25_m"]   + data["25_30_m"]  + data["30_35_m"] + data["15_18_w"] + data["18_20_w"] + data["20_25_w"] + data["25_30_w"] + data["30_35_w"]
data["age_35_59"]   = data["35_ 40_m"]  + data["40_45_m"] + data["45_ 50_m"]  + data["50_ 55_m"] + data["55_60_m"] + data["35_40_w"] + data["40_45_w"] + data["45_50_w"] + data["50_55_w"] + data["55_60_w"]
data["age_60_75"]   = data["60_65_m"]   + data["65_75_m"] + data["60_65_w"]   + data["65_75_w"]
data["age_75+"]     = data["75_m"]      + data["75_w"]

# aggregierte Altersgruppen in neuen Data Frame kopieren
data_new = data[["ID_LK_SK","age_0_5", "age_6_14" , "age_15_34", "age_35_59", "age_60_75", "age_75+" ]]

# Altersgruppen zusammenfassen
data_new['age_0_34'] = data_new['age_0_5'] + data_new['age_6_14']  + data_new['age_15_34']   
data_new['age_60+']  = data_new['age_60_75'] + data_new['age_75+']

# Summe aller Einwohner pro Kreis
data_new['sum']      = data_new['age_0_34'] + data_new['age_35_59'] + data_new['age_60+']

# relativen Anteil berechnen
data_new['age_0_34_%']  = (data_new['age_0_34']  / data_new['sum']) * 100
data_new['age_35_59_%'] = (data_new['age_35_59'] / data_new['sum']) * 100
data_new['age_60+_%']   = (data_new['age_60+']   / data_new['sum']) * 100

##############################
# Gebietsfläche mit einfügen #
##############################

# Daten mergen
data_new = pd.merge(data_new, data_flaeche, on='ID_LK_SK')

# Einwohner pro Quadratkilometer berechnen
data_new['Einw_pro_qm'] = data_new['sum'] / data_new['Flaeche_in_qm']

#################
# fertigstellen #
#################

# nur notwendige Spalten auswählen
data_new_final = data_new[['ID_LK_SK' ,'age_0_34_%', 'age_35_59_%' , 'age_60+_%', 'Einw_pro_qm']]

# Missing Values mit 0 befüllen
data_new_final.fillna(0, inplace=True)

#####################
# Daten exportieren #
#####################

data_new_final.to_csv("../data/01_Kreise_Altersverteilung_Fläche.csv")

#####################
# Datenbank beladen # 
#####################

engine  = db.create_engine('mysql://ateam:5araPGQ7TTjHSKo6BHxO4fdDk5C2MDKyQvnVC7Sb@37.221.198.242:3308/data_science')
con     = engine.connect()

data_new_final.to_sql(name='kreise_altersverteilung', con=engine, if_exists='replace',
                      dtype={"ID_LK_SK":              db.types.INTEGER(),
                             "age_0_34_%":            db.types.Float(precision=3, asdecimal=True),
                             "age_35_59_%":           db.types.Float(precision=3, asdecimal=True),
                             "age_60+_%":             db.types.Float(precision=3, asdecimal=True),
                             "Einw_pro_qm":           db.types.Float(precision=3, asdecimal=True)})

