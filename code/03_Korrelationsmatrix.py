# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 09:30:55 2020

@author: Stefan Klug
"""

#################
# Datenanalysen #
#################

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/02_Daten_merged.csv")

   
######################
# Korrelationsmatrix #
######################
    
korrelation = ["age_0_34_%",
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
               "Immunschwäche",
               "Sterberate_%"]
              
total_metrisch = df[korrelation]

import seaborn as sns

plt.rcParams["figure.figsize"] = [20,20] #12
plt.rc('xtick',labelsize=15)#15
plt.rc('ytick',labelsize=15)#15

fig, ax = plt.subplots()

sns.set(font_scale=1.25)
#fig = plt.figure(figsize=(20,20))
sns.heatmap(total_metrisch.corr(method='pearson'), annot=True, fmt='.2f',
            cmap=plt.get_cmap('Oranges'), cbar=False, ax=ax, square=True) #copper_r

#plt.title('Korrelation', fontsize=15, fontweight="semibold")

#b, t = plt.ylim() # discover the values for bottom and top
#b += 0.5 # Add 0.5 to the bottom
#t -= 0.5 # Subtract 0.5 from the top
#plt.ylim(b, t) # update the ylim(bottom, top) values
#ax.set_xticklabels(ax.get_xticklabels(), rotation=53)  #"horizontal")
ax.set_xticklabels(ax.get_xticklabels(), rotation=80)  #"horizontal")
ax.set_yticklabels(ax.get_yticklabels(), rotation="horizontal")
plt.tight_layout()
plt.savefig('../Datenanalysen/Korrelationsmatrix.png')
plt.show()