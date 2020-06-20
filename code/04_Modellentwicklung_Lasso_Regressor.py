# -*- coding: utf-8 -*-
"""
@author: ATeam
"""

###########################
# Modell Lasso-Regression #
###########################

############################
# Bibliotheken importieren #
############################

from sklearn.model_selection import train_test_split

from sklearn.linear_model import Lasso, LassoCV

from sklearn.preprocessing import StandardScaler

import pandas as pd
pd.options.mode.chained_assignment = None

from itertools import combinations

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime

##################
# Daten einlesen #
##################

df = pd.read_csv("../data/02_Daten_merged.csv")

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

######################################
# metrische Features standardisieren #
######################################

metrisch = []

for col in features_raw.columns:
    if features_raw[col].dtypes == 'float64':
        print("Col:", col)
        features_raw[col] = features_raw[col]/100
        metrisch.append(col)

StaSca = StandardScaler()        
features_raw[metrisch] = StaSca.fit_transform(features_raw[metrisch])

###################
# Dummy Codierung #
###################

# 0/1 Dummy Codierung von LK_SK
features_raw = features_raw.join(pd.get_dummies(features_raw["LK_SK"]))

# 0/1 Dummy Codierung von Bundesland 
features_raw = features_raw.join(pd.get_dummies(features_raw["Bundesland"]))

# unnötige Spalten löschen --> wurden als Dummy codiert
features_raw.drop(["LK_SK", "Bundesland"], axis=1, inplace=True)

####################
# Train_Test Split #
####################

# 80% Trainingsdaten und 20% Testdaten
X_train, X_test, y_train, y_test = train_test_split(features_raw, 
                                                    targets_raw, 
                                                    test_size = 0.2, 
                                                    random_state = 0)

####################################################
# Bestes Modell mit sechs Einflussvariablen finden #
####################################################

# die folgenden 21 Feature sind plausibel und eignen sich für Modelle
# die 16 Bundesländer werden nicht berücksichtig, da z. B. die Fallzahlen in
# Bayern sehr hoch sind und die Sterberate dort auch am höchsten ist
# Bayern hat aber 96 Kreise, die sehr unterschiedliche Sterberaten aufweisen
# Bundesländer sind nicht plausibel, aber beeinflussen die Modelle teilweise sehr stark

# finde das beste Modell, das aus 6 dieser 21 Features besteht

X_21 =  ["age_0_34_%",
         "age_35_59_%",
         "age_60+_%",
         "Einw_pro_qm",
         "LK",
         "SK",
         "age_covid_0_34_%",
         "age_covid_35_59_%",
         "age_covid_60+_%",
         "gender_covid_f_%",
         "gender_covid_m_%",
         "Prävalenz",
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

counter = 0

# Modell für jede der 54264 Kombinationen schätzen
for komb in [['age_covid_0_34_%', 'age_covid_35_59_%', 'Diabetes', 'Krebs', 'Lebererkrankungen', 'Immunschwäche']] :#kombinationen_6:
        
    counter  = counter +1
    if counter % 10000 == 0:
        print(counter)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        print("\n")
    
    # Datensatz auf mögliche Variablen begrenzen
    train_df_6_komb = X_train[komb]
    test_df_6_komb  = X_test[komb]
    
    # Modelldefinition
    regr = Lasso(alpha=0.05)

    # Modelltraining
    regr.fit(train_df_6_komb, y_train)
    
    # Score der Trainings- und Testdaten
    ar_train_6_komb = regr.score(train_df_6_komb, y_train)
    ar_test_6_komb  = regr.score(test_df_6_komb,  y_test)
    
    # Regressionskoeffizienten
    linReg_L1_coef_alle = pd.DataFrame(regr.coef_.transpose(), train_df_6_komb.columns, columns=['Koeffizienten'])
    
    # Ergebnisse in Liste einfügen
    ergebnisse.append([komb, [ar_train_6_komb, ar_test_6_komb], [linReg_L1_coef_alle]])

########################
# bestes Modell finden #
########################
    
hoechste_ar = 0
# suche Modell mit höchstem Score auf Testdaten
for x in range(0, len(ergebnisse)):
    if ergebnisse[x][1][1] > hoechste_ar:
        hoechste_ar = ergebnisse[x][1][1]
        position    = x

print('\n-----------------------------')
print('Bestes Modell mit 6 Features')        
print('-----------------------------')
print(ergebnisse[position])
print("\n")


'''
-----------------------------
Bestes Modell mit 6 Features
-----------------------------
[['age_covid_0_34_%', 'age_covid_35_59_%', 'Diabetes', 'Krebs', 'Lebererkrankungen', 'Immunschwäche'], [0.6224500082108149, 0.5048907778824191], [                   Koeffizienten
age_covid_0_34_%       -1.756199
age_covid_35_59_%      -1.656975
Diabetes               -0.235023
Krebs                  -0.189913
Lebererkrankungen       0.087428
Immunschwäche          -0.068011]]
'''

#############################
# finales Modell optimieren #
#############################

print("\n----------------------------")
print("Finales Modell optimieren")
print("----------------------------")

# beste sechs Feature
X_6 = ["age_covid_0_34_%",
       "age_covid_35_59_%",
       "Diabetes",
       "Immunschwäche",
       "Krebs",
       "Lebererkrankungen"]

X_train_6 = X_train[X_6]  
X_test_6  = X_test[X_6]

# definiere Alphas -> Regularisierungsparameter
alphas = np.logspace(-10, 1, 400)

# finde das beste Alpha
regr_6 = LassoCV(cv             = 5,
                 alphas         = alphas,
                 random_state   = 0,
                 n_jobs         = -1)

regr_6.fit(X_train_6, y_train)

print("\nBestes Alpha:")
print(regr_6.alpha_)

# Bestes Alpha:
# 0.005239601353002634

##################
# finales Modell #
##################

print("\n----------------------------")
print("Finales Modell")
print("----------------------------")

regr_6 = Lasso(alpha=0.005239601353002634)
regr_6.fit(X_train_6, y_train)
print("\nScore Trainingsdaten", regr_6.score(X_train_6, y_train))
print("Score Testdaten",        regr_6.score(X_test_6, y_test))

# Regressionskoeffizienten
linReg_L1_coef_alle = pd.DataFrame(regr_6.coef_.transpose(), X_train_6.columns, columns=['Koeffizienten'])
linReg_L1_coef_alle["absolut"] = abs(linReg_L1_coef_alle["Koeffizienten"])
linReg_L1_coef_alle.sort_values(by='absolut', ascending=False, inplace=True)

print("\n")
print(linReg_L1_coef_alle)

###############################################################################
# Modell Auswertung                                                           #
###############################################################################

######################################################################################################
# durchschnittliche Abweichung zwischen tatsächlicher und modellierten durchschnittlicher Sterberate #
######################################################################################################

# Trainingsdaten
X_train_6["Sterberate_modelliert"]  = regr_6.predict(X_train_6)
X_train_6["Sterberate_%"] = y_train
X_train_6["Differenz"] = abs(X_train_6["Sterberate_%"] - X_train_6["Sterberate_modelliert"])
mean_train = X_train_6["Differenz"].mean()

# Testdaten
X_test_6["Sterberate_modelliert"]  = regr_6.predict(X_test_6)
X_test_6["Sterberate_%"] = y_test
X_test_6["Differenz"] = abs(X_test_6["Sterberate_%"] - X_test_6["Sterberate_modelliert"])
mean_test = X_test_6["Differenz"].mean()

# Trainings- und Testdaten
features_raw_6 = features_raw[X_6]
features_raw_6["Sterberate_modelliert"]  = regr_6.predict(features_raw_6)
features_raw_6["Sterberate_%"] = targets_raw
features_raw_6["Differenz"] = abs(features_raw_6["Sterberate_%"] - features_raw_6["Sterberate_modelliert"])
features_raw_6["Kreis"] = df["Landkreis"]
mean_all = features_raw_6["Differenz"].mean()

print("\nDurchschnittliche Abweichung Trainingsdaten in Prozentpunkten:", round(mean_train, 2))
print("Durchschnittliche Abweichung Testdaten in Prozentpunkten:",        round(mean_test, 2))
print("Durchschnittliche Abweichung aller Daten in Prozentpunkten:",      round(mean_all, 2))

# Durchschnitt Abweichung Trainingsdaten in Prozentpunkten: 1.25
# Durchschnitt Abweichung Testdaten in Prozentpunkten: 1.45
# Durchschnitt Abweichung aller Daten in Prozentpunkten: 1.29

#########################################################################
# größte Abweichung zwischen tatsächlicher und modellierter Ausfallrate #
#########################################################################

maximale_differenz_train = max(X_train_6["Differenz"])
maximale_differenz_test  = max(X_test_6["Differenz"])
maximale_differenz_all   = max(features_raw_6["Differenz"])

print("\nGrößte Abweichung Trainingsdaten:", round(maximale_differenz_train, 2))
print("Größte Abweichung Testdaten:",        round(maximale_differenz_test, 2))
print("Größte Abweichung aller Daten:",      round(maximale_differenz_all, 2))

# Größte Abweichung Trainingsdaten: 5.98
# Größte Abweichung Testdaten: 6.69
# Größte Abweichung aller Daten: 6.69

# selektiere die 3 Kreise mit größter Abweichung zwischen tatsächlicher und modellierter Sterberate
abweichung = features_raw_6[["Kreis", "Sterberate_%", "Sterberate_modelliert", "Differenz"]].sort_values(by='Differenz', ascending=False)[0:3]

print("\n")
print(abweichung)

'''             Kreis  Sterberate_%  Sterberate_modelliert  Differenz
45           SK Emden      0.000000               6.686155   6.686155
'''
# größte Differenz tritt bei SK Emden mit 6.69% auf
# -> "In Emden sind insgesamt drei Personen an einer Infektion mit dem Corona-Virus verstorben
#     Sie kamen aus dem Landkreis Aurich und werden auch dort statistisch erfasst."
# -> https://www.nwzonline.de/ostfriesland/in-ostfriesland-statistik-vom-12-mai-zahl-der-infektionen-in-ostfriesland-stagniert_a_50,7,4293638566.html
# -> in der Stadt Emden sind drei Personen an einer COVID-19 Infektion gestorben
# -> in der Statistk wurden diese Todesfälle allerdings dem LK Aurich zugeordnet
# -> somit liegt die statistische Sterberate im SK Emden bei 0%
# -> hohe Abweichung des Modells ist nachvollziehbar und somit plausibel



'''             Kreis  Sterberate_%  Sterberate_modelliert  Differenz
126  LK Odenwaldkreis     14.987715               9.011861   5.975854
'''
# zweitgrößte Differenz tritt bei SK Odenwaldkreis mit 5.98% auf
# -> im Odenwaldkreis ist in einem Pflegeheim  der Coronavirus ausgebrochen
# -> 39 Bewohner des Pflegeheimes sind an COVID-19 verstorben
# -> große Abweichung plausibel
# https://www.echo-online.de/lokales/odenwaldkreis/odenwaldkreis/keine-corona-neuinfizierten-oder-toten-im-odenwaldkreis_21703350

'''             Kreis  Sterberate_%  Sterberate_modelliert  Differenz
164      SK Pirmasens      0.000000               5.242400   5.242400
'''
# drittgrößte Differenz tritt bei SK Pirmasens mit 5.24% auf
# -> in diesem Kreis gab es keine Verstorbenen (überprüft)
# -> Sterberate liegt bei 0%, es wurde aber eine Sterberate von 5,26% prognostiziert
# -> Abweichung plausibel