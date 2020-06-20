# -*- coding: utf-8 -*-
"""
@author: ATeam
"""

#################
# Datenanalysen #
#################

############################
# Bibliotheken importieren #
############################

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/02_Daten_merged.csv")

#################
# age           #
#################

age = ["age_0_34_%",
       "age_35_59_%",
       "age_60+_%"]

x_age  = []
y1_age = []
y2_age = []

for el in age:
    x_age.append(el)
    y1_age.append(df[el].mean())
    
plt.bar(x_age, y1_age, color='darkorange')
plt.title("durchschnittliche Altersverteilung der LKs/ SKs", fontsize=12, fontweight="semibold") #15
plt.xticks(x_age, rotation='vertical')
plt.tight_layout()
plt.savefig('../Datenanalysen/Altersverteilung' + '.png')
plt.show()    
    
#################
# covid         #
#################    
    
covid = ["age_covid_0_34_%",
         "age_covid_35_59_%",
         "age_covid_60+_%",
         "age_covid_unknown_%"]

x_covid  = []
y1_covid = []

for el in covid:
    x_covid.append(el)
    y1_covid.append(df[el].mean())   
    
plt.bar(x_covid, y1_covid, color='darkorange')
plt.title("durchschnittliche Altersverteilung der Covid Patienten", fontsize=12, fontweight="semibold") #15
plt.xticks(x_covid, rotation='vertical')
plt.tight_layout()
plt.savefig('../Datenanalysen/Altersverteilung_Covid' + '.png')
plt.show()

#################
# gender        #
#################    
    
gender = ["gender_covid_f_%",
          "gender_covid_m_%",
          "gender_covid_unknown_%"]

x_gender  = []
y1_gender = []

for el in gender:
    x_gender.append(el)
    y1_gender.append(df[el].mean())    
    
plt.bar(x_gender, y1_gender, color='darkorange')
plt.title("durschnittliche Geschlechterverteilung der Covid Patienten", fontsize=12, fontweight="semibold") #15
plt.xticks(x_gender, rotation='vertical')
plt.tight_layout()
plt.savefig('../Datenanalysen/Geschlechterverteilung_Covid' + '.png')
plt.show()    

#################
# Prävalenz     #
#################    
    
prävalenz = ["Prävalenz",
             "Prävalenz_plausibles_Intervall_untere_Grenze",
             "Prävalenz_plausibles_Intervall_obere_Grenze"]

x_prävalenz  = []
y1_prävalenz = []

for el in prävalenz:
    x_prävalenz.append(el)
    y1_prävalenz.append(df[el].mean())      
    
plt.bar(x_prävalenz, y1_prävalenz, color='darkorange')
plt.title("Prävalenz", fontsize=12, fontweight="semibold") #15
plt.xticks(x_prävalenz, rotation='vertical')
plt.tight_layout()
plt.savefig('../Datenanalysen/Prävalenz' + '.png')
plt.show()
       
#######################
# metrische Variablen #
#######################
    
metrisch = ["age_0_34_%",
            "age_35_59_%",
            "age_60+_%",
            "Einw_pro_qm",
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

for el in metrisch:
    # Einteilung in 5 Bins
    total_bins      = pd.cut(df[el], bins=5, duplicates='drop', precision=0, right=False)
    total_bins      = total_bins.rename("bins")
    temp            = pd.concat([total_bins, df[[el, "Sterberate_%"]]], axis=1, join='inner')
    grafikdaten     = temp.groupby(["bins"])['Sterberate_%'].mean() 
    grafikdaten     = pd.concat([grafikdaten, temp["bins"].value_counts()], axis=1, join='inner')
                 
    plt.bar(grafikdaten.index.values.astype(str), grafikdaten["bins"], color='darkorange')
    plt.title(el, fontsize=12, fontweight="semibold")
    plt.xticks(grafikdaten.index.values.astype(str), rotation='vertical')

    plt2 = plt.twinx()
    plt2.plot(grafikdaten.index.values.astype(str), grafikdaten['Sterberate_%'], color='dodgerblue', marker='o', label='Sterberate in %')
    plt2.set_ylim([0, max(grafikdaten["Sterberate_%"])+0.5])
    plt2.set_ylabel('Sterberate in %')
    plt.tight_layout()
    plt.savefig('../Datenanalysen/Sterberate_' + el + '.png')
    plt.show()

#########################
# kategoriale Variablen #
#########################

kategorial = ["LK_SK",
              "Bundesland"]

for el in kategorial:    
    grafikdaten = df.groupby([el])['Sterberate_%'].mean()
    grafikdaten = pd.concat([grafikdaten, df[el].value_counts()], axis=1, join='inner')
    grafikdaten.sort_values(by=['Sterberate_%'], inplace=True)
          
    plt.bar(grafikdaten.index.values.astype(str), grafikdaten[el], color='darkorange')
    plt.title(el, fontsize=12, fontweight="semibold")
    plt.xticks(grafikdaten.index.values.astype(str), rotation='vertical')
    plt2 = plt.twinx()
    plt2.plot(grafikdaten.index.values.astype(str), grafikdaten['Sterberate_%'], color='dodgerblue', marker='o', label='Sterberate in %')
    plt2.set_ylim([0, max(grafikdaten["Sterberate_%"])+0.5])
    plt2.set_ylabel('Sterberate in %')
    plt.tight_layout()
    plt.savefig('../Datenanalysen/Sterberate_' + el + '.png')
    plt.show()
    
