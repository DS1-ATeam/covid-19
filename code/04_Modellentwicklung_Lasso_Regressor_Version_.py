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

from sklearn.linear_model import Lasso, LassoCV

from sklearn.preprocessing import StandardScaler

from sklearn.preprocessing import PolynomialFeatures

import pandas as pd
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

######################
# Feature Selecetion #
######################

# entferne Spalten, die das Ergebnis zu stark beinflussen
X_train_selectio = X_train.drop(["age_covid_60+_%", "Prävalenz_plausibles_Intervall_untere_Grenze", "Prävalenz_plausibles_Intervall_obere_Grenze"], axis=1, inplace=False)
X_test_selection = X_test.drop(["age_covid_60+_%",  "Prävalenz_plausibles_Intervall_untere_Grenze", "Prävalenz_plausibles_Intervall_obere_Grenze"], axis=1, inplace=False)

# Wähle 13 Features aus, die eine Feature Importance > 0 haben
# wird erreicht, indem min_samples_leaf (Mindestanzahl der Beobachtungen pro Blatt auf 27 gesetzt wird)
# das Feature age_covid_60+_% wird hier nicht verwendet, da es das Ergebnis zu stark beeinfluss
# --> erreich Feature Importance von etwa 0,9
# regr = RandomForestRegressor(max_depth=None, min_samples_leaf=20, n_estimators=100, n_jobs=-1, random_state=0)

regr = Lasso(alpha=0.033)
regr.fit(X_train_selectio, y_train)
print("\nScore Trainingsdaten", regr.score(X_train_selectio, y_train))
print("Score Testdaten", regr.score(X_test_selection, y_test))

# Regressionskoeffizienten
linReg_L1_coef_alle = pd.DataFrame(regr.coef_.transpose(), X_train_selectio.columns, columns=['Koeffizienten'])
linReg_L1_coef_alle["absolut"] = abs(linReg_L1_coef_alle["Koeffizienten"])
linReg_L1_coef_alle.sort_values(by='absolut', ascending=False, inplace=True)
print(linReg_L1_coef_alle)

####################################################
# Bestes Modell mit sechs Einflussvariablen finden #
####################################################

# diese Features haben für min_samples_leaf=27 eine Feature Importance > 0
# an dieser Stelle wird das Feature age_covid_60+_% wieder hinzugefügt
# Wenn das beste Modell das Feature age_covid_60+_% enthält, aber eine zu hohe
# Feature Importance aufweist, wird dieses Modell verworfen und  das beste Modell
# ohne das Feature age_covid_60+_% ausgewählt 

# finde das beste Modell, das aus 6 dieser 14 Features besteht 

X_14 =  ["age_0_34_%",
         #"age_35_59_%",
         "age_60+_%",
         "age_covid_0_34_%",
         "age_covid_35_59_%",
         "age_covid_60+_%",
         #"Asthma",
         #"Bluthochdruck",
         "COPD",
         "Diabetes",
         "Einw_pro_qm",
         "gender_covid_f_%",
         #"gender_covid_m_%",
         "gender_covid_unknown_%",
         #"Herzinsuffizienz",
         #"Herz",
         "Hessen",
         "KHK",
         #"Krebs",
         #"Lunge",
         "Lebererkrankungen",
         "Prävalenz"]

X_21 =  ["age_0_34_%",
         "age_35_59_%",
         "age_60+_%",
         "Einw_pro_qm",
         "LK",
         "SK",
         #"Bundesland",
         "age_covid_0_34_%",
         "age_covid_35_59_%",
         "age_covid_60+_%",
         #"age_covid_unknown_%",
         "gender_covid_f_%",
         "gender_covid_m_%",
         #"gender_covid_unknown_%",
         "Prävalenz",
         #"Prävalenz_plausibles_Intervall_untere_Grenze",
         #"Prävalenz_plausibles_Intervall_obere_Grenze",
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

poly = PolynomialFeatures(degree=2)


# alle Kombinationen mit 6 aus 14 Features: 6 aus 14 = 3003 Kombinationen
kombinationen = list(combinations(X_21, 6))

# Liste für alle 3003 Kombinationen
kombinationen_6 = []

# Kombinationen liegen als Tupel in kombinationen vor 
# füge alle Kombinationen in eine Liste
for k in kombinationen:
    kombinationen_6.append(list(k))

# Liste für alle 3003 Ergebnisse
ergebnisse = []

counter = 0

# Modell für jede der 3003 Kombinationen schätzen
for komb in kombinationen_6:
        
    counter  = counter +1
    if counter % 10000 == 0:
        print(counter)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        print("\n")
    
    # Datensatz auf mögliche Variablen begrenzen
    train_df_6_komb = poly.fit_transform(X_train[komb])
    test_df_6_komb  = poly.fit_transform(X_test[komb]) 
    
    # Modelldefinition
    regr = Lasso(alpha=0.05)

    # Modelltraining
    regr.fit(train_df_6_komb, y_train)
    
    # Accuracy Ratios Trainings- und Testdaten
    ar_train_6_komb = regr.score(train_df_6_komb, y_train)
    ar_test_6_komb  = regr.score(test_df_6_komb,  y_test)
    
    # Regressionskoeffizienten
    linReg_L1_coef_alle = regr.coef_ #pd.DataFrame(regr.coef_.transpose(), train_df_6_komb.columns, columns=['Koeffizienten'])
    
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
        position    = x

print('--------------------------------------------------')
print('Bestes Modell mit 6 Features ohne age_covid_60+_%')        
print('--------------------------------------------------')
print(ergebnisse[position])

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

alphas = np.logspace(-10, 1, 400)

regr_6 = LassoCV(cv=5, alphas=alphas, random_state=0, n_jobs=-1)
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
'''
'''
----------------------------
Finales Modell
----------------------------

Score Trainingsdaten 0.6246224924196526
Score Testdaten 0.5103636917231099


                   Koeffizienten   absolut
age_covid_0_34_%       -1.836109  1.836109
age_covid_35_59_%      -1.712645  1.712645
Diabetes               -0.266169  0.266169
Krebs                  -0.224199  0.224199
Lebererkrankungen       0.133093  0.133093
Immunschwäche          -0.107972  0.107972
'''




'''
to do:
- Feature Importance plotten
- Abweichungen abchecken -> wo liegt größte Differenz?
- was ist durchschnittlicher Fehler?
'''
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


--------------------------------------------------
Bestes Modell mit 6 Features ohne age_covid_60+_%
--------------------------------------------------
[['age_covid_0_34_%', 'age_covid_35_59_%', 'Diabetes', 'Krebs', 'Lebererkrankungen', 'Immunschwäche'], [0.6224500082108149, 0.5048907778824191], [                   Koeffizienten
age_covid_0_34_%       -1.756199
age_covid_35_59_%      -1.656975
Diabetes               -0.235023
Krebs                  -0.189913
Lebererkrankungen       0.087428
Immunschwäche          -0.068011]]

-----------------------------
Bestes Modell mit 6 Features
-----------------------------
[['age_covid_0_34_%', 'age_covid_35_59_%', 'Diabetes', 'Krebs', 'Lebererkrankungen', 'Immunschwäche'], [0.6236898095211113, 0.5074407497179356], [                   Koeffizienten
age_covid_0_34_%       -1.786546
age_covid_35_59_%      -1.678112
Diabetes               -0.246865
Krebs                  -0.202931
Lebererkrankungen       0.104775
Immunschwäche          -0.083179]]


--------------------------------------------------
Bestes Modell mit 6 Features ohne age_covid_60+_%
--------------------------------------------------
[['age_covid_0_34_%', 'age_covid_35_59_%', 'Diabetes', 'Krebs', 'Lebererkrankungen', 'Immunschwäche'], [0.6236898095211113, 0.5074407497179356], [                   Koeffizienten
age_covid_0_34_%       -1.786546
age_covid_35_59_%      -1.678112
Diabetes               -0.246865
Krebs                  -0.202931
Lebererkrankungen       0.104775
Immunschwäche          -0.083179]]








##################
# finales Modell #
##################

X_6 = ["age_35_59_%", "age_60+_%", "age_covid_0_34_%", "age_covid_35_59_%", "Einw_pro_qm", "Prävalenz"]

X_6 = ['age_35_59_%', 'age_60+_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'Bluthochdruck', 'Krebs']

X_6 = ["age_35_59_%",
       "age_60+_%",
       "age_covid_0_34_%",
       "age_covid_35_59_%",
       "COPD",
       "Herzinsuffizienz"]

X_train_6 = X_train[X_6]  
X_test_6  = X_test[X_6]

regr_6 = RandomForestRegressor(max_depth=None,
                             #min_samples_leaf=27,
                             n_estimators=100,
                             n_jobs=-1,
                             random_state=0)

regr_6.fit(X_train_6, y_train)
print("\nScore Trainingsdaten", regr_6.score(X_train_6, y_train))
print("Score Testdaten",        regr_6.score(X_test_6, y_test))

# Feature Importance
fea_impor_ran_for_6 = pd.DataFrame(regr_6.feature_importances_.transpose(), X_train_6.columns, columns=['Feature_Importance'])
fea_impor_ran_for_6.sort_values(by='Feature_Importance', ascending=False, inplace=True)

print("\nFeature Importance:")
print(fea_impor_ran_for_6)



from sklearn.model_selection import RandomizedSearchCV# Number of trees in random forest

import numpy as np

n_estimators = [int(x) for x in np.linspace(start = 10, stop = 200, num = 20)]

n_estimators = [x for x in range(20,230,20)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
#max_depth = [int(x) for x in np.linspace(1, 20, num = 11)]

max_depth = [4,5,6,7,8,9,10, None]

#max_depth.append(None)

# Minimum number of samples required to split a node
#min_samples_split = [2, 5, 10]

# Minimum number of samples required at each leaf node
min_samples_leaf = [1,2,3,4,5,6,7,8,9,10]

# Method of selecting samples for training each tree
bootstrap = [True, False]# Create the random grid
random_grid = {'n_estimators':      n_estimators,
               #'max_features':      max_features,
               'max_depth':         max_depth,
               #'min_samples_split': min_samples_split,
               'min_samples_leaf':  min_samples_leaf,
               'bootstrap':         bootstrap}

rf_random = RandomizedSearchCV(estimator = regr_6, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=0, n_jobs = -1)# Fit the random search model
rf_random.fit(X_train_6, y_train)

print(rf_random.best_params_)



regr_6 = RandomForestRegressor(bootstrap=True,
                               max_depth=None,
                               min_samples_leaf=4,
                               max_features = 'auto',
                               n_estimators=160,
                               n_jobs=-1,
                               random_state=0)

regr_6.fit(X_train_6, y_train)
print("\nScore Trainingsdaten", regr_6.score(X_train_6, y_train))
print("Score Testdaten",        regr_6.score(X_test_6, y_test))

# Feature Importance
fea_impor_ran_for_6 = pd.DataFrame(regr_6.feature_importances_.transpose(), X_train_6.columns, columns=['Feature_Importance'])
fea_impor_ran_for_6.sort_values(by='Feature_Importance', ascending=False, inplace=True)

print("\nFeature Importance:")
print(fea_impor_ran_for_6)
'''


'''
-----------------------------
Bestes Modell mit 6 Features
-----------------------------
[['age_35_59_%', 'age_60+_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'Herzinsuffizienz'], [0.933590242615078, 0.5472725185514378], [                   Feature_Importance
age_covid_35_59_%            0.408485
age_covid_0_34_%             0.374407
age_60+_%                    0.092034
age_35_59_%                  0.076501
Herzinsuffizienz             0.048573]]


--------------------------------------------------
Bestes Modell mit 6 Features ohne age_covid_60+_%
--------------------------------------------------
[['age_35_59_%', 'age_60+_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'Herzinsuffizienz'], [0.933590242615078, 0.5472725185514378], [                   Feature_Importance
age_covid_35_59_%            0.408485
age_covid_0_34_%             0.374407
age_60+_%                    0.092034
age_35_59_%                  0.076501
Herzinsuffizienz             0.048573]]



[['age_35_59_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'Prävalenz', 'Schlaganfall', 'COPD'], [0.9318896832272067, 0.5608403508510347], [                   Feature_Importance
age_covid_35_59_%            0.409102
age_covid_0_34_%             0.369917
age_35_59_%                  0.077068
Prävalenz                    0.074334
COPD                         0.049504
Schlaganfall                 0.020074]]
[['age_35_59_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'KHK', 'Schlaganfall', 'Krebs'], [0.9351387020508735, 0.5605672176920466], [                   Feature_Importance
age_covid_35_59_%            0.418243
age_covid_0_34_%             0.374009
age_35_59_%                  0.082443
KHK                          0.074127
Krebs                        0.033475
Schlaganfall                 0.017703]]


-----------------------------
Bestes Modell mit 6 Features
-----------------------------
[['age_35_59_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'Prävalenz', 'Schlaganfall', 'COPD'], [0.9318896832272067, 0.5608403508510347], [                   Feature_Importance
age_covid_35_59_%            0.409102
age_covid_0_34_%             0.369917
age_35_59_%                  0.077068
Prävalenz                    0.074334
COPD                         0.049504
Schlaganfall                 0.020074]]


--------------------------------------------------
Bestes Modell mit 6 Features ohne age_covid_60+_%
--------------------------------------------------
[['age_35_59_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'Prävalenz', 'Schlaganfall', 'COPD'], [0.9318896832272067, 0.5608403508510347], [                   Feature_Importance
age_covid_35_59_%            0.409102
age_covid_0_34_%             0.369917
age_35_59_%                  0.077068
Prävalenz                    0.074334
COPD                         0.049504
Schlaganfall                 0.020074]]

-----------------------------
Bestes Modell mit 6 Features
-----------------------------
[['age_35_59_%', 'age_60+_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'COPD', 'Herzinsuffizienz'], [0.9315315157842833, 0.5474463888564249], [                   Feature_Importance
age_covid_35_59_%            0.399182
age_covid_0_34_%             0.363235
age_60+_%                    0.083485
age_35_59_%                  0.069123
COPD                         0.043376
Herzinsuffizienz             0.041598]]

-----------------------------
Bestes Modell mit 6 Features
-----------------------------
[['age_35_59_%', 'age_60+_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'Bluthochdruck', 'Krebs'], [0.9341076168598734, 0.5557575683550408], [                   Feature_Importance
age_covid_35_59_%            0.402595
age_covid_0_34_%             0.368780
age_35_59_%                  0.075342
Bluthochdruck                0.065017
age_60+_%                    0.063476
Krebs                        0.024790]]

--------------------------------------------------
Bestes Modell mit 6 Features ohne age_covid_60+_%
--------------------------------------------------
[['age_35_59_%', 'age_60+_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'COPD', 'Herzinsuffizienz'], [0.9315315157842833, 0.5474463888564249], [                   Feature_Importance
age_covid_35_59_%            0.399182
age_covid_0_34_%             0.363235
age_60+_%                    0.083485
age_35_59_%                  0.069123
COPD                         0.043376
Herzinsuffizienz             0.041598]]

-----------------------------
Bestes Modell mit 6 Features
-----------------------------
[['age_35_59_%', 'age_60+_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'Einw_pro_qm', 'Prävalenz'], [0.62642105889463, 0.4652831409795684], [                   Feature_Importance
age_covid_35_59_%            0.505983
age_covid_0_34_%             0.449954
age_60+_%                    0.023371
age_35_59_%                  0.009170
Prävalenz                    0.008074
Einw_pro_qm                  0.003448]]


--------------------------------------------------
Bestes Modell mit 6 Features ohne age_covid_60+_%
--------------------------------------------------
[['age_35_59_%', 'age_60+_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'Einw_pro_qm', 'Prävalenz'], [0.62642105889463, 0.4652831409795684], [                   Feature_Importance
age_covid_35_59_%            0.505983
age_covid_0_34_%             0.449954
age_60+_%                    0.023371
age_35_59_%                  0.009170
Prävalenz                    0.008074
Einw_pro_qm                  0.003448]]

-----------------------------
Bestes Modell mit 6 Features
-----------------------------
[['age_35_59_%', 'age_60+_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'Krebs', 'Prävalenz'], [0.6268999824335861, 0.4664563993982839], [                   Feature_Importance
age_covid_35_59_%            0.506419
age_covid_0_34_%             0.449521
age_60+_%                    0.021537
age_35_59_%                  0.009918
Prävalenz                    0.006690
Krebs                        0.005915]]

--------------------------------------------------
Bestes Modell mit 6 Features ohne age_covid_60+_%
--------------------------------------------------
[['age_35_59_%', 'age_60+_%', 'age_covid_0_34_%', 'age_covid_35_59_%', 'Bluthochdruck', 'Krebs'], [0.9343867074868604, 0.5561753587952729], [                   Feature_Importance
age_covid_35_59_%            0.402595
age_covid_0_34_%             0.368780
age_35_59_%                  0.075342
Bluthochdruck                0.065017
age_60+_%                    0.063476
Krebs                        0.024790]]

-----------------------------
Bestes Modell mit 6 Features
-----------------------------
[['age_covid_35_59_%', 'age_covid_60+_%', 'Bluthochdruck', 'COPD', 'Immunschwäche', 'Lebererkrankungen'], [0.9344236684218377, 0.51014412922808], [                   Feature_Importance
age_covid_60+_%              0.654170
age_covid_35_59_%            0.122881
Bluthochdruck                0.098686
Lebererkrankungen            0.048574
COPD                         0.038512
Immunschwäche                0.037177]]


--------------------------------------------------
Bestes Modell mit 6 Features ohne age_covid_60+_%
--------------------------------------------------
[['age_covid_35_59_%', 'Asthma', 'COPD', 'gender_covid_m_%', 'Lebererkrankungen', 'Prävalenz'], [0.8924961704628979, 0.28209564937369447], [                   Feature_Importance
gender_covid_m_%             0.346295
age_covid_35_59_%            0.344340
Lebererkrankungen            0.089163
Prävalenz                    0.087841
COPD                         0.066519
Asthma                       0.065842]]
'''

