# -*- coding: utf-8 -*-
"""
@author: ATeam
"""
########################
# Modell Random Forest #
########################


############################
# Bibliotheken importieren #
############################

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

import pandas as pd
pd.options.mode.chained_assignment = None

from itertools import combinations

import matplotlib.pyplot as plt

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
# das Feature age_covid_60+_% wird hier nicht verwendet, da es das Ergebnis zu stark beeinflusst
# --> covid_60+_% erreicht Feature Importance von etwa 0,9

regr = RandomForestRegressor(max_depth=None,
                             min_samples_leaf=27,
                             n_estimators=100,
                             n_jobs=-1,
                             random_state=0)
regr.fit(X_train_selectio, y_train)

print("\nScore Trainingsdaten", regr.score(X_train_selectio, y_train))
print("Score Testdaten", regr.score(X_test_selection, y_test))

# Feature Importance
fea_impor_ran_for_alle = pd.DataFrame(regr.feature_importances_.transpose(), X_train_selectio.columns, columns=['Feature_Importance'])
fea_impor_ran_for_alle.sort_values(by='Feature_Importance', ascending=False, inplace=True)

print("\n")
print(fea_impor_ran_for_alle)

'''
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
         "age_35_59_%",
         "age_60+_%",
         "age_covid_0_34_%",
         "age_covid_35_59_%",
         "age_covid_60+_%",
         "Bluthochdruck",
         "COPD",
         "Diabetes",
         "Einw_pro_qm",
         "gender_covid_f_%",
         "gender_covid_m_%",
         "Herzinsuffizienz",
         "Prävalenz"]

# alle Kombinationen mit 6 aus 14 Features: 6 aus 14 = 3003 Kombinationen
kombinationen = list(combinations(X_14, 6))

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
    if counter % 500 == 0:
        print(counter)
    
    # Datensatz auf mögliche Variablen begrenzen
    train_df_6_komb = X_train[komb]  
    test_df_6_komb  = X_test[komb]
    
    # Modelldefinition
    regr = RandomForestRegressor(n_estimators       = 100,
                                 max_depth          = None,
                                 #min_samples_leaf   = 15, # leichte Regularisierung der Bäume -> Schutz vor Overfitting
                                 n_jobs             = -1, 
                                 random_state       = 0)

    # Modelltraining
    regr.fit(train_df_6_komb, y_train)
    
    # Score der Trainings- und Testdaten
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
        position    = x

print('\n-----------------------------')
print('Bestes Modell mit 6 Features')        
print('-----------------------------')
print(ergebnisse[position])
print("\n")
'''

'''
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
'''

#############################
# finales Modell optimieren #
#############################

print("\n----------------------------")
print("Finales Modell optimieren")
print("----------------------------")

# beste sechs Feature
X_6 = ["age_35_59_%",
       "age_60+_%",
       "age_covid_0_34_%",
       "age_covid_35_59_%",
       "COPD",
       "Herzinsuffizienz"]

X_train_6 = X_train[X_6]  
X_test_6  = X_test[X_6]

regr_6 = RandomForestRegressor(n_estimators=100,
                               n_jobs=-1,
                               random_state=0)

# Anzahl der Bäume
n_estimators     = [x for x in range(20,150,20)]
# maximale Tiefe der Bäume
max_depth        = [4,5,6,7,8,9,10,11,12,13,14,15,None]
# minimale Anzahl der Beobachtungen pro Blatt
min_samples_leaf = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,None]

random_grid = {'n_estimators':      n_estimators,
               'max_depth':         max_depth,
               'min_samples_leaf':  min_samples_leaf}

rf_random = RandomizedSearchCV(estimator            = regr_6,
                               param_distributions  = random_grid,
                               n_iter               = 100,
                               cv                   = 5,
                               verbose              = 2,
                               random_state         = 0,
                               n_jobs               = -1)

rf_random.fit(X_train_6, y_train)

print("\nBeste Parameter:")
print(rf_random.best_params_)

# Beste Parameter:
# {'n_estimators': 80, 'min_samples_leaf': 6, 'max_depth': 15}

##################
# finales Modell #
##################

print("\n----------------------------")
print("Finales Modell")
print("----------------------------")

regr_6 = RandomForestRegressor(max_depth        = 15,
                               min_samples_leaf = 6,
                               n_estimators     = 80,
                               n_jobs           = -1,
                               random_state     = 0)

regr_6.fit(X_train_6, y_train)

print("\nScore Trainingsdaten", regr_6.score(X_train_6, y_train))
print("Score Testdaten",        regr_6.score(X_test_6, y_test))

# Feature Importance
fea_impor_ran_for_6 = pd.DataFrame(regr_6.feature_importances_.transpose(), X_train_6.columns, columns=['Feature_Importance'])
fea_impor_ran_for_6.sort_values(by='Feature_Importance', ascending=False, inplace=True)

print("\n")
print(fea_impor_ran_for_6)


###############################################################################
# Modell Auswertung                                                           #
###############################################################################

# plotte Features zusammen mit deren Feature Importance

def print_fea_import(data, text, x):

    data.sort_values('Feature_Importance',inplace=True)
    
    #plotte Missing Values
    plt.rc('xtick',labelsize=12)
    plt.rc('ytick',labelsize=12)
    plt.rcParams["figure.figsize"] = [x,4]
    plt.rcParams['font.family'] = 'sans-serif'
    
    plt.xlim([0, max(data['Feature_Importance'])+0.025])
    
    plt.barh(data.index.values.astype(str), data['Feature_Importance'], color='darkorange')
    
    for i,j in zip(data.index.values.astype(str), data['Feature_Importance']):
        
        if j > 0.1:
            minus = 0.06
        else:
            minus = -0.01
        
        label = str(round(j*100, 2)) + ' %'
        
        plt.text(j-minus, i, label, fontsize=12, family = 'sans-serif', verticalalignment='center')
    
    plt.title('Feature Importance Random Forest Regressor', fontsize=12, fontweight="semibold")
    plt.tight_layout()
    plt.savefig('../data_analysis/'+text+'.png')
    plt.show()

print_fea_import(data=fea_impor_ran_for_6, text='Feature_Importance_Random_Forest_Regressor', x=9)

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
print("Durchschnittliche Abweichung Testdaten in Prozentpunkten:", round(mean_test, 2))
print("Durchschnittliche Abweichung aller Daten in Prozentpunkten:", round(mean_all, 2))

# Durchschnitt Abweichung Trainingsdaten in Prozentpunkten: 1.0
# Durchschnitt Abweichung Testdaten in Prozentpunkten: 1.58
# Durchschnitt Abweichung aller Daten in Prozentpunkten: 1.12

#########################################################################
# größte Abweichung zwischen tatsächlicher und modellierter Ausfallrate #
#########################################################################

maximale_differenz_train = max(X_train_6["Differenz"])
maximale_differenz_test  = max(X_test_6["Differenz"])
maximale_differenz_all   = max(features_raw_6["Differenz"])

print("\nGrößte Abweichung Trainingsdaten:", round(maximale_differenz_train, 2))
print("Größte Abweichung Testdaten:", round(maximale_differenz_test, 2))
print("Größte Abweichung aller Daten:", round(maximale_differenz_all, 2))

# Größte Abweichung Trainingsdaten: 5.47
# Größte Abweichung Testdaten: 5.05
# Größte Abweichung aller Daten: 5.47

# selektiere die 3 Kreise mit größter Abweichung zwischen tatsächlicher und modellierter Sterberate
abweichung = features_raw_6[["Kreis", "Sterberate_%", "Sterberate_modelliert", "Differenz"]].sort_values(by='Differenz', ascending=False)[0:3]

print("\n")
print(abweichung)

'''             Kreis  Sterberate_%  Sterberate_modelliert  Differenz
18       SK Wolfsburg     14.825581               9.352153   5.473428
'''
# größte Differenz tritt bei SK Wolfsburg mit 5.47% auf
# -> in Wolfsburg ist in einem Senioren-Einrichtungen der Coronavirus ausgebrochen
# -> 44 Bewohner der Senioren-Einrichtungen sind an COVID-19 verstorben
# -> große Abweichung plausibel
# https://www.wolfsburger-nachrichten.de/wolfsburg/article228716311/corona-wolfsburg-infizierte-geschaefte-bus-bahn-infos-informationen-arzt.html


'''             Kreis  Sterberate_%  Sterberate_modelliert  Differenz
126  LK Odenwaldkreis     14.987715               9.599382   5.388333
'''
# zweitgrößte Differenz tritt bei SK Odenwaldkreis mit 5.39% auf
# -> im Odenwaldkreis ist in einem Pflegeheim  der Coronavirus ausgebrochen
# -> 39 Bewohner des Pflegeheimes sind an COVID-19 verstorben
# -> große Abweichung plausibel
# https://www.echo-online.de/lokales/odenwaldkreis/odenwaldkreis/keine-corona-neuinfizierten-oder-toten-im-odenwaldkreis_21703350

'''             Kreis  Sterberate_%  Sterberate_modelliert  Differenz
164      SK Pirmasens      0.000000               5.054743   5.054743
'''
# drittgrößte Differenz tritt bei SK Pirmasens mit 5.05% auf
# -> in diesem Kreis gab es keine Verstorbenen (überprüft)
# -> Sterberate liegt bei 0%, es wurde aber eine Sterberate von 5,26% prognostiziert
# -> Abweichung plausibel

