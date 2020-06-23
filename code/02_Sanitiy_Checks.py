# -*- coding: utf-8 -*-
"""
@author: ATeam
"""

################
# Datenqualiät #
################

############################
# Bibliotheken importieren #
############################

import sqlalchemy as db
import pandas as pd
import random

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

print("\n------------------------------------------------")
print("Beginn: Datenüberprüfung")
print("------------------------------------------------\n")

#################
# Sanity-Checks #
#################

########################################################
# überprüfen, ob relative Häufigkeiten zu 100 addieren #
########################################################

print("\n------------------------------------------------------")
print("überprüfen, ob relative Häufigkeiten zu 100 addieren")
print("------------------------------------------------------\n")

df["Sanity_check_age"]           = (df["age_0_34_%"] + df["age_35_59_%"] + df["age_60+_%"])/100

df["Sanity_check_covid_age"]     = (df["age_covid_0_34_%"] + df["age_covid_35_59_%"] + df["age_covid_60+_%"] + df["age_covid_unknown_%"])/100

df["Sanity_check_covid_gender"]  = (df["gender_covid_f_%"] + df["gender_covid_m_%"] + df["gender_covid_unknown_%"])/100


if sum(df["Sanity_check_age"]) != len(df["Sanity_check_age"]):
    print("\n------------------------------------------------")
    print("Sanity_check_age")
    print("Werte summieren sich nicht zu 100!")
    print("------------------------------------------------")

if sum(df["Sanity_check_covid_age"]) != len(df["Sanity_check_covid_age"]):
    print("\n------------------------------------------------")
    print("Sanity_check_covid_age")
    print("Werte summieren sich nicht zu 100!")
    print("------------------------------------------------")
    
if sum(df["Sanity_check_covid_gender"]) != len(df["Sanity_check_covid_gender"]):
    print("\n------------------------------------------------")
    print("Sanity_check_covid_gender")
    print("Werte summieren sich nicht zu 100!")
    print("------------------------------------------------")
    
df.drop(columns=['Sanity_check_age', 'Sanity_check_covid_age', 'Sanity_check_covid_gender'])
    
############################################################
# überprüfen, ob Wertebereiche der Features plausibel sind #
############################################################

print("\n----------------------------------------------------------")
print("überprüfen, ob Wertebereiche der Features plausibel sind")
print("----------------------------------------------------------\n")

######################################
# Prozentwerte im Intervall [0, 100] #
######################################

prozent = ["age_0_34_%",
           "age_35_59_%",
           "age_60+_%",
           "age_covid_0_34_%",
           "age_covid_35_59_%",
           "age_covid_60+_%",
           "age_covid_unknown_%",
           "gender_covid_f_%",
           "gender_covid_m_%",
           "gender_covid_unknown_%",
           "Sterberate_%",
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

for el in prozent:
    if min(df[el]) < 0:
        print("\n------------------------------------------------")
        print(el)
        print("Wert(e) kleiner 0!")
        print("------------------------------------------------")

    if max(df[el]>100):
        print("\n------------------------------------------------")
        print(el)
        print("Wert(e) größer 100!")
        print("------------------------------------------------")
    
    
#############################################
# alle Werte in Einw_pro_qm größer gleich 0 #
#############################################
        
if min(df["Einw_pro_qm"]) < 0:
    print("\n------------------------------------------------")
    print("Einw_pro_qm")
    print("Wert(e) kleiner 0!")
    print("------------------------------------------------")

###########################
# Bundesländer überprüfen #
###########################

bundeslaender = ["Baden-Württemberg",
                 "Bayern",
                 "Berlin",
                 "Brandenburg",
                 "Bremen",
                 "Hamburg",
                 "Hessen",
                 "Mecklenburg-Vorpommern",
                 "Niedersachsen",
                 "Nordrhein-Westfalen",
                 "Rheinland-Pfalz",
                 "Saarland",
                 "Sachsen",
                 "Sachsen-Anhalt",
                 "Schleswig-Holstein",
                 "Thüringen"]

bundeslaender_in_df = df["Bundesland"].unique()
     
for bundesland in bundeslaender:
    if bundesland not in bundeslaender_in_df:
        print("\n------------------------------------------------")
        print(bundesland)
        print("Nicht im Datensatz enthalten!")
        print("------------------------------------------------")
        
if len(bundeslaender) != len(bundeslaender_in_df):
    print("\n------------------------------------------------")
    print("Bundesland")
    print("Ungültige Werte!")
    print("------------------------------------------------")
         
#########
# LK SK #
#########

LK_SK = ["LK", "SK"]

LK_SK_in_df = df["LK_SK"].unique()

for el in LK_SK:
    if el not in LK_SK_in_df:
        print("\n------------------------------------------------")
        print(el)
        print("Nicht im Datensatz enthalten!")
        print("------------------------------------------------")

if len(LK_SK) != len(LK_SK_in_df):
    print("\n------------------------------------------------")
    print("LK_SK")
    print("Ungültige Werte!")
    print("------------------------------------------------")

#########################
# Missings bei ID_LK_SK #
#########################

if df["ID_LK_SK"].isnull().sum() > 0:
    print("\n------------------------------------------------")
    print("ID_LK_SK")
    print("Missing Values!")
    print("------------------------------------------------") 
 	
######################
# Missings bei Kreis #
######################

if df["Kreis"].isnull().sum() > 0:
    print("\n------------------------------------------------")
    print("Kreis")
    print("Missing Values!")
    print("------------------------------------------------")    


##########################################################
# randomisiert 40 IDs und dazugehörigen Namen überprüfen #
##########################################################

print("\n-------------------------------------------------------")   
print("randomisiert 40 IDs und dazugehörigen Namen überprüfen")
print("-------------------------------------------------------\n") 
    
for x in range(40):
    rand = random.randint(1, len(df["ID_LK_SK"])) - 1
    if df["ID_LK_SK"][rand] < 10000:
        print(str(df["ID_LK_SK"][rand])+':  ', df["Kreis"][rand])
    else:
        print(str(df["ID_LK_SK"][rand])+': ', df["Kreis"][rand])

###################################################################
# Quellen zum überprüfen der Kombinationen aus ID und LK/SK-Namen #
###################################################################

# Landkreise (LK):         https://de.wikipedia.org/wiki/Liste_der_Landkreise_in_Deutschland
    
# kreisfreien Städte (SK): https://de.wikipedia.org/wiki/Liste_der_kreisfreien_St%C3%A4dte_in_Deutschland

'''
-------------------------------------------------------
randomisiert 40 IDs und dazugehörigen Namen überprüfen
-------------------------------------------------------

9475:   LK Hof                          stimmt
9276:   LK Regen                        stimmt
6634:   LK Schwalm-Eder-Kreis           stimmt
7235:   LK Trier-Saarburg               stimmt
8225:   LK Neckar-Odenwald-Kreis        stimmt
15081:  LK Altmarkkreis Salzwedel       stimmt
3405:   SK Wilhelmshaven                stimmt
3255:   LK Holzminden                   stimmt
9763:   SK Kempten                      stimmt
5916:   SK Herne                        stimmt
3354:   LK Lüchow-Dannenberg            stimmt
9175:   LK Ebersberg                    stimmt
5562:   LK Recklinghausen               stimmt
9182:   LK Miesbach                     stimmt
6531:   LK Gießen                       stimmt
5558:   LK Coesfeld                     stimmt
5122:   SK Solingen                     stimmt
3354:   LK Lüchow-Dannenberg            stimmt
9678:   LK Schweinfurt                  stimmt
3460:   LK Vechta                       stimmt
9375:   LK Regensburg                   stimmt
8231:   SK Pforzheim                    stimmt
9677:   LK Main-Spessart                stimmt
5570:   LK Warendorf                    stimmt
8416:   LK Tübingen                     stimmt
8225:   LK Neckar-Odenwald-Kreis        stimmt
6413:   SK Offenbach                    stimmt
14522:  LK Mittelsachsen                stimmt
3356:   LK Osterholz                    stimmt
7336:   LK Kusel                        stimmt
7231:   LK Bernkastel-Wittlich          stimmt
7338:   LK Rhein-Pfalz-Kreis            stimmt
7233:   LK Vulkaneifel                  stimmt
5112:   SK Duisburg                     stimmt
9463:   SK Coburg                       stimmt
3360:   LK Uelzen                       stimmt
9763:   SK Kempten                      stimmt
9761:   SK Augsburg                     stimmt
9778:   LK Unterallgäu                  stimmt
5513:   SK Gelsenkirchen                stimmt
'''

print("\n------------------------------------------------")
print("Ende: Datenüberprüfung")
print("------------------------------------------------\n")