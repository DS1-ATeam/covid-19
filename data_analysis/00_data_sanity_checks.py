# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 12:25:45 2020

@author: Stefan Klug
"""

################
# Datenqualiät #
################

import pandas as pd
import random

df = pd.read_csv("../data/02_Daten_merged.csv")


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
 	
##########################
# Missings bei Landkreis #
##########################

if df["Landkreis"].isnull().sum() > 0:
    print("\n------------------------------------------------")
    print("Landkreis")
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
        print(str(df["ID_LK_SK"][rand])+':  ', df["Landkreis"][rand])
    else:
        print(str(df["ID_LK_SK"][rand])+': ', df["Landkreis"][rand])

###################################################################
# Quellen zum überprüfen der Kombinationen aus ID und LK/SK-Namen #
###################################################################

# Landkreise (LK):         https://de.wikipedia.org/wiki/Liste_der_Landkreise_in_Deutschland
    
# kreisfreien Städte (SK): https://de.wikipedia.org/wiki/Liste_der_kreisfreien_St%C3%A4dte_in_Deutschland

'''
5334:   LK Aachen
15083:  LK Börde
5916:   SK Herne
15085:  LK Harz
5512:   SK Bottrop
9376:   LK Schwandorf
5962:   LK Märkischer Kreis
12069:  LK Potsdam-Mittelmark
7320:   SK Zweibrücken
9478:   LK Lichtenfels
15090:  LK Stendal
9576:   LK Roth
9362:   SK Regensburg
5570:   LK Warendorf
14626:  LK Görlitz
5966:   LK Olpe
7320:   SK Zweibrücken
3404:   SK Osnabrück
5954:   LK Ennepe-Ruhr-Kreis
16063:  LK Wartburgkreis
5382:   LK Rhein-Sieg-Kreis
5915:   SK Hamm
12062:  LK Elbe-Elster
6438:   LK Offenbach                stimmt
8121:   SK Heilbronn                stimmt
16064:  LK Unstrut-Hainich-Kreis    stimmt
5112:   SK Duisburg                 stimmt
13074:  LK Nordwestmecklenburg      stimmt
6635:   LK Waldeck-Frankenberg      stimmt
3256:   LK Nienburg (Weser)         stimmt
5334:   LK Aachen
7143:   LK Westerwaldkreis
9376:   LK Schwandorf
3155:   LK Northeim
9276:   LK Regen
7312:   SK Kaiserslautern
8417:   LK Zollernalbkreis
6531:   LK Gießen
9462:   SK Bayreuth                 stimmt
15081:  LK Altmarkkreis Salzwedel   stimmt
'''

print("\n------------------------------------------------")
print("Ende: Datenüberprüfung")
print("------------------------------------------------\n")