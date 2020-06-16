# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 23:48:24 2020

@author: Stefan Klug
"""
############################
# Bibliotheken importieren #
############################

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor
#from lib.data.DataPreProcessor import DataPreProcessor

import pandas as pd
from itertools import combinations


##################
# Daten einlesen #
##################

df = pd.read_csv("../data/02_Daten_merged.csv")

#pre_processor = DataPreProcessor()
#features_raw, targets_raw = pre_processor.split_features(), [)

################################
# mögliche Features für Modell #
################################

columns =  ["age_0_34_%",
            "age_35_59_%",
            "age_60+_%",
            "Einw_pro_qm",
            "LK_SK",
            "Bundesland",
            "age_covid_0_34_%",
            "age_covid_35_59_%",
            "age_covid_60+_%",
            "age_covid_unknown_%",
            "gender_covid_f_%",
            "gender_covid_m_%",
            "gender_covid_unknown_%",
            "Prävalenz",
            "Prävalenz_plausibles_Intervall_untere_Grenze",
            "Prävalenz_plausibles_Intervall_obere_Grenze",
            "Bluthochdruck",
            "KHK",
            "Herzinfarkt",
            "Herzinsuffizienz",
            "Schlaganfall",
            "Diabetes",
            "Asthma",
            "COPD",
            "Krebs",
            "Lebererkrankungen",
            "Immunschwäche"]

#####################
# Daten für Modelle #
#####################

features_raw = df[columns]

############################
# Zielvariable der Modelle #
############################

targets_raw  = df["Sterberate_%"]

###################
# Dummy Codierung #
###################

# 0/1 Dummy Codierung von LK_SK
features_raw = features_raw.join(pd.get_dummies(features_raw["LK_SK"]))

# 0/1 Dummy Codierung von Bundesland 
features_raw = features_raw.join(pd.get_dummies(features_raw["Bundesland"]))

# unnötige Spalten löschen --> wurden als Dummy codiert
features_raw.drop(["LK_SK", "Bundesland"], axis=1, inplace=True)

# in Prozent umrechenen
#for el in features_raw.columns:
#    if features_raw[el].dtypes == 'float64':
#        features_raw[el] = features_raw[el] / 100


####################
# Train_Test Split #
####################

# 80% Trainingsdaten und 20% Testdaten
X_train, X_test, y_train, y_test = train_test_split(features_raw, 
                                                    targets_raw, 
                                                    test_size = 0.2, 
                                                    random_state = 0)

######################
# Feature Selecetion #
######################

# gernze Bereich der Features ein

regr = RandomForestRegressor(max_depth=None,
                             min_samples_leaf=25,
                             n_estimators=100,
                             n_jobs=-1,
                             random_state=0)
regr.fit(X_train, y_train)
print("\nScore Trainingsdaten", regr.score(X_train, y_train))
print("Score Testdaten", regr.score(X_test, y_test))

# Feature Importance
fea_impor_ran_for_alle = pd.DataFrame(regr.feature_importances_.transpose(), X_train.columns, columns=['Feature_Importance'])
fea_impor_ran_for_alle.sort_values(by='Feature_Importance', ascending=False, inplace=True)

print("\nFeature Importance:")
print(fea_impor_ran_for_alle)

####################################################
# Bestes Modell mit sechs Einflussvariablen finden #
####################################################

# diese Features haben für min_samples_leaf=25 eine Feature Importance > 0
# finde nun das beste Modell, das aus 6 dieser 21 Features besteht 

X_21 =  ["age_0_34_%",
         "age_35_59_%",
         "age_60+_%",
         "age_covid_0_34_%",
         "age_covid_35_59_%",
         "age_covid_60+_%",
         "Asthma",
         "Bluthochdruck",
         "COPD",
         "Diabetes",
         "Einw_pro_qm",
         "gender_covid_f_%",
         "gender_covid_m_%",
         "Herzinsuffizienz",
         "Immunschwäche",
         "KHK",
         "Krebs",
         "Lebererkrankungen",
         "Prävalenz",
         "Prävalenz_plausibles_Intervall_untere_Grenze",
         "Prävalenz_plausibles_Intervall_obere_Grenze"]

# alle Kombinationen mit 6 aus 21 Features: 6 aus 21 = 54264 Kombinationen
kombinationen = list(combinations(X_21, 6))

# Liste für alle 54264 Kombinationen
kombinationen_6 = []

# Kombinationen liegen als Tupel in kombinationen vor 
# füge alle Kombinationen in eine Liste
for k in kombinationen:
    kombinationen_6.append(list(k))

# Liste für alle 54264 Ergebnisse
ergebnisse = []

# Modell für jede der 54264 Kombinationen schätzen
for komb in kombinationen_6:
    
    # Datensatz auf mögliche Variablen begrenzen
    train_df_6_komb = X_train[komb]  
    test_df_6_komb  = X_test[komb]
    
    # Modelldefinition
    regr = RandomForestRegressor(n_estimators       = 100,
                                 max_depth          = None,
                                 n_jobs             = -1, 
                                 random_state       = 0)

    # Modelltraining
    regr.fit(train_df_6_komb, y_train)
    
    # Accuracy Ratios Trainings- und Testdaten
    ar_train_6_komb = regr.score(train_df_6_komb, y_train)
    ar_test_6_komb  = regr.score(test_df_6_komb,  y_test)
    
    # Feature Importance
    fea_import_ran_for_6_komb = pd.DataFrame(regr.feature_importances_.transpose(), train_df_6_komb.columns, columns=['Feature_Importance'])
    fea_import_ran_for_6_komb.sort_values(by='Feature_Importance', ascending=False, inplace=True)
    
    # Ergebnisse in Liste einfügen
    ergebnisse.append([komb, [ar_train_6_komb, ar_test_6_komb], [fea_import_ran_for_6_komb]])

########################
# bestes Modell finden #
########################
    
hoechste_ar = 0
# suche Modell mit höchstem Score auf Testdaten
for x in range(0, len(ergebnisse)):
    if ergebnisse[x][1][1] > hoechste_ar:
        hoechste_ar = ergebnisse[x][1][1]
        position  = x

print('-----------------------------')
print('Bestes Modell mit 6 Features')        
print('-----------------------------')
print(ergebnisse[position])
print("\n")


hoechste_ar = 0
# suche Modell mit höchstem Score auf Testdaten
for x in range(0, len(ergebnisse)):
    if (ergebnisse[x][1][1] > hoechste_ar) and ('age_covid_60+_%' not in ergebnisse[x][0]):
        hoechste_ar = ergebnisse[x][1][1]
        position  = x

print('--------------------------------------------------')
print('Bestes Modell mit 6 Features ohne age_covid_60+_%')        
print('--------------------------------------------------')
print(ergebnisse[position])




