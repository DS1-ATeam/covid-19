# -*- coding: utf-8 -*-
"""
@author: ATeam
"""

###################################
# Modell Random Forest Classifier #
###################################

############################
# Bibliotheken importieren #
############################

import sqlalchemy as db
from itertools import combinations
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
import pandas as pd
pd.options.mode.chained_assignment = None


'''
###################################
# Daten aus MySQL-Datenbank laden #
###################################

engine  = db.create_engine('mysql://ateam:5araPGQ7TTjHSKo6BHxO4fdDk5C2MDKyQvnVC7Sb@37.221.198.242:3308/data_science')
con     = engine.connect()

metadata    = db.MetaData()
table       = db.Table('Gesamt', metadata, autoload=True, autoload_with=engine)
query       = db.select([table])
results     = con.execute(query).fetchall()
df          = pd.DataFrame(results)
df.columns  = results[0].keys()
df.drop(columns=['index'], inplace=True)
df.info()
'''

##################
# Daten einlesen #
##################

df = pd.read_csv("../data/02_Gesamt.csv")
df.info()

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

target = df[["ID_LK_SK", "Sterberate_%"]]
target["Class"] = target["Sterberate_%"]

# ordne Sterberaten Klassen zu
target.loc[(target.Class < 2.5),  "Class"] = 0
target.loc[(2.5 <= target.Class) & (target.Class < 5.0), "Class"] = 1
target.loc[(5.0 <= target.Class) & (target.Class < 7.5), "Class"] = 2
target.loc[(7.5 <= target.Class) & (target.Class < 10.0), "Class"] = 3
target.loc[(target.Class >= 10.0), "Class"] = 4

targets_raw  = target["Class"]

##########################
# Verteilung der Klassen #
##########################

print("\nAnzahl der Beobachtungen pro Klasse:")
print(targets_raw.value_counts())

'''
Anzahl der Beobachtungen pro Klasse:
1.0    158
0.0    103
2.0     89
3.0     35
4.0     16
'''
# -> Klassen sind sehr ungleich verteilt
# -> großer Unterschied zwischen Anzahl der Beobachtungen pro Klasse

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



# Show the results of the split
print("Training set has {} samples.".format(X_train.shape[0]))
print("Testing set has {} samples.".format(X_test.shape[0]))

######################
# Feature Selecetion #
######################

classi = RandomForestClassifier(max_depth         = None,
                                min_samples_leaf  = 100,
                                n_estimators      = 100,
                                n_jobs            = -1,
                                random_state      = 0)
classi.fit(X_train, y_train)

print("\nScore Trainingsdaten", classi.score(X_train, y_train))
print("Score Testdaten",        classi.score(X_test, y_test))

# Feature Importance
fea_impor_ran_for_alle = pd.DataFrame(classi.feature_importances_.transpose(), X_train.columns, columns=['Feature_Importance'])
fea_impor_ran_for_alle.sort_values(by='Feature_Importance', ascending=False, inplace=True)

print("\n")
print(fea_impor_ran_for_alle)


####################################################
# Bestes Modell mit sechs Einflussvariablen finden #
####################################################

# Feature Selection liefert diese zwölf Features
X_12 = ["age_covid_0_34_%",
        "age_covid_35_59_%",
        "age_covid_60+_%",
        "age_0_34_%",
        "age_35_59_%",
        "age_60+_%",
        "Asthma",
        "Diabetes",
        "Einw_pro_qm",
        "gender_covid_m_%",
        "gender_covid_f_%",
        "Prävalenz_plausibles_Intervall_obere_Grenze"]


# alle Kombinationen mit 6 aus 12 Variablen: 6 aus 12 = 924 Kombinationen
kombinationen = list(combinations(X_12, 6))

# Liste für alle 924 Kombinationen
kombinationen_6 = []

# Kombinationen liegen als Tupel in kombinationen vor 
# füge alle Kombinationen in eine Liste
for k in kombinationen:
    kombinationen_6.append(list(k))

# Liste für alle 924 Ergebnisse
ergebnisse = []

# Modell für jede der 924 Kombinationen schätzen
for komb in kombinationen_6:
    
    # Datensatz auf mögliche Variablen begrenzen
    train_df_6_komb = X_train[komb]  
    test_df_6_komb  = X_test[komb]
    
    # Modelldefinition
    classi = RandomForestClassifier(n_estimators       = 100,
                                    max_depth          = None,
                                    n_jobs             = -1, 
                                    random_state       = 0)

    # Modelltraining
    classi.fit(train_df_6_komb, y_train)
    
    # Accuracy Ratios Trainings- und Testdaten
    ar_train_6_komb = classi.score(train_df_6_komb, y_train)
    ar_test_6_komb  = classi.score(test_df_6_komb,  y_test)
    
    # Feature Importance
    fea_import_ran_for_6_komb = pd.DataFrame(classi.feature_importances_.transpose(), train_df_6_komb.columns, columns=['Feature_Importance'])
    fea_import_ran_for_6_komb.sort_values(by='Feature_Importance', ascending=False, inplace=True)
    
    # Ergebnisse in Liste einfügen
    ergebnisse.append([komb, [ar_train_6_komb, ar_test_6_komb], [fea_import_ran_for_6_komb]])

########################
# bestes Modell finden #
########################
    
hoechste_ar = 0
# suche Modell mit höchster Accuracy Ratio auf Testdaten
for x in range(0, len(ergebnisse)):
    if ergebnisse[x][1][1] > hoechste_ar:
        hoechste_ar = ergebnisse[x][1][1]
        position  = x

print('-------------------------------------')
print('Bestes Modell mit 6 Einflussvariablen')        
print('-------------------------------------')
print(ergebnisse[position])

'''
-------------------------------------
Bestes Modell mit 6 Einflussvariablen
-------------------------------------
[['age_covid_60+_%', 'age_0_34_%', 'age_35_59_%', 'age_60+_%', 'Asthma', 'Diabetes'], [1.0, 0.5925925925925926], [Feature_Importance
age_covid_60+_%            0.332527
age_0_34_%                 0.145294
age_35_59_%                0.135691
Diabetes                   0.131144
age_60+_%                  0.130089
Asthma                     0.125255]]
'''

#############################
# finales Modell optimieren #
#############################

print("\n----------------------------")
print("Finales Modell optimieren")
print("----------------------------")

# beste sechs Feature
X_6 = ["age_0_34_%",
       "age_35_59_%",
       "age_60+_%",
       "age_covid_60+_%",
       "Asthma",
       "Diabetes"]

X_train_6 = X_train[X_6]  
X_test_6  = X_test[X_6]

classi_6 = RandomForestClassifier(n_estimators = 100,
                                  n_jobs       = -1,
                                  random_state = 0)

##################################################
# finde beste Hyperparamter mit Kreuzvalidierung #
##################################################

# Anzahl der Bäume
n_estimators     = [x for x in range(20,150,20)]
# maximale Tiefe der Bäume
max_depth        = [4,5,6,7,8,9,10,11,12,13,14,15,None]
# minimale Anzahl der Beobachtungen pro Blatt
min_samples_leaf = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,None]

random_grid = {'n_estimators':      n_estimators,
               'max_depth':         max_depth,
               'min_samples_leaf':  min_samples_leaf}

rf_random = RandomizedSearchCV(estimator            = classi_6,
                               param_distributions  = random_grid,
                               n_iter               = 100,
                               cv                   = 5,
                               verbose              = 2,
                               random_state         = 0,
                               n_jobs               = -1)

rf_random.fit(X_train_6, y_train)

print("\nBeste Hyperparameter:")
print(rf_random.best_params_)

# Beste Hyperparameter:
# {'n_estimators': 60, 'min_samples_leaf': 11, 'max_depth': 7}

##################
# finales Modell #
##################

print("\n----------------------------")
print("Finales Modell")
print("----------------------------")

classi_6 = RandomForestClassifier(max_depth        = 7,
                                  min_samples_leaf = 11,
                                  n_estimators     = 60,
                                  n_jobs           = -1,
                                  random_state     = 0)
classi_6.fit(X_train_6, y_train)

print("\nScore Trainingsdaten", classi_6.score(X_train_6, y_train))
print("Score Testdaten",        classi_6.score(X_test_6,  y_test))

# Feature Importance
fea_impor_ran_for_6 = pd.DataFrame(classi_6.feature_importances_.transpose(), X_train_6.columns, columns=['Feature_Importance'])
fea_impor_ran_for_6.sort_values(by='Feature_Importance', ascending=False, inplace=True)

print("\n")
print(fea_impor_ran_for_6)

'''
----------------------------
Finales Modell
----------------------------

Score Trainingsdaten 0.665625
Score Testdaten 0.5802469135802469

                 Feature_Importance
age_covid_60+_%            0.566928
age_60+_%                  0.103259
age_35_59_%                0.091459
age_0_34_%                 0.089658
Diabetes                   0.086439
Asthma                     0.062257
'''

# Modell nicht wirklich aussagekräftig:
# 1. age_covid_60+_% hat Feature Importance von über 56%
# -> beeinflusst Modell zu stark
# 2. zuviele Klassen 
# -> Anzahl der Beobachtungen pro Klasse sehr ungleich verteilt
# -> keine Aussagekraft
'''
Anzahl der Beobachtungen pro Klasse:
1.0    158
0.0    103
2.0     89
3.0     35
4.0     16
'''