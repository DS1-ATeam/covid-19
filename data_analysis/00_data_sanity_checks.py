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

df = pd.read_csv("C:/Users/Stefan Klug/data-science-project/data/02_Daten_merged.csv")


#################
# Sanity-Checks #
#################

###########################################################
# überprüfen. ob sich relative Häufigkeiten zu 1 addieren #
###########################################################

df["Sanity_check_age"]           = (df["age_0_34_%"] + df["age_35_59_%"] + df["age_60+_%"])/100

df["Sanity_check_covid"]         = (df["age_covid_0_34_%"] + df["age_covid_35_59_%"] + df["age_covid_60+_%"] + df["age_covid_unknown_%"])/100

df["Sanity_check_covid_gender"]  = (df["gender_covid_f_%"] + df["gender_covid_m_%"] + df["gender_covid_unknown_%"])/100


#for el in df["Sanity_check_age"]:
#    print(el)
#    if el != 1:
#        print("Summe ungleich 1")

if sum(df["Sanity_check_age"]) == len(df["Sanity_check_age"]):
    print("Sanity_check_age ergibt 1")

if sum(df["Sanity_check_covid"]) == len(df["Sanity_check_covid"]):
    print("Sanity_check_covid ergibt 1")
    
if sum(df["Sanity_check_covid_gender"]) == len(df["Sanity_check_covid_gender"]):
    print("Sanity_check_covid_gender ergibt 1")
    

##############################################################
# randomisiert 40 IDs und dazugehörigen Landkreis überprüfen #
##############################################################
    
for x in range(40):
    rand = random.randint(1, len(df["ID_LK_SK"])) - 1
    print(df["ID_LK_SK"][rand], ': ', df["Landkreis"][rand])

# Quelle zum überprüfen der IDs und LK/SK-Namen
    # 

'''
6438 :  LK Offenbach                stimmt
12066 :  LK Oberspreewald-Lausitz   stimmt
5512 :  SK Bottrop                  stimmt
8316 :  LK Emmendingen              stimmt
9176 :  LK Eichstätt                stimmt
16064 :  LK Unstrut-Hainich-Kreis   stimmt
5122 :  SK Solingen                 stimmt
9762 :  SK Kaufbeuren               stimmt
6433 :  LK Groß-Gerau               stimmt
9471 :  LK Bamberg                  stimmt
9677 :  LK Main-Spessart            stimmt
6631 :  LK Fulda                    stimmt
14625 :  LK Bautzen                 stimmt
9163 :  SK Rosenheim                stimmt
9779 :  LK Donau-Ries               stimmt
9474 :  LK Forchheim                stimmt
3355 :  LK Lüneburg                 stimmt
3359 :  LK Stade                    stimmt
9375 :  LK Regensburg               stimmt
5570 :  LK Warendorf                stimmt
'''