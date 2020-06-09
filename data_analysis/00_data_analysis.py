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

df = pd.read_csv("C:/Users/Stefan Klug/data-science-project/data/02_Daten_merged.csv")

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
plt.savefig('Altersverteilung' + '.png')
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
plt.savefig('Altersverteilung_Covid' + '.png')
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
plt.savefig('Geschlechterverteilung_Covid' + '.png')
plt.show()    

#################
# Prävalenz     #
#################    
    
prävalenz = ["Prävalenz (Anteil mit mindestens einer Vorerkrankung in %)",
             "Prävalenz-Schätzwerte plausibles Intervall Untergrenze",
             "Prävalenz-Schätzwerte plausibles Intervall Obergrenze"]

x_prävalenz  = []
y1_prävalenz = []

for el in prävalenz:
    x_prävalenz.append(el)
    y1_prävalenz.append(df[el].mean())      
    
plt.bar(x_prävalenz, y1_prävalenz, color='darkorange')
plt.title("Prävalenz", fontsize=12, fontweight="semibold") #15
plt.xticks(x_prävalenz, rotation='vertical')
plt.tight_layout()
plt.savefig('Prävalenz' + '.png')
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
            #"Sterberate_%",
            "Prävalenz (Anteil mit mindestens einer Vorerkrankung in %)",
            "Prävalenz-Schätzwerte plausibles Intervall Untergrenze",
            "Prävalenz-Schätzwerte plausibles Intervall Obergrenze"]

for el in metrisch:
    # Einteilung in 5 Bins
    total_bins      = pd.cut(df[el], bins=5, duplicates='drop', precision=0, right=False)
    total_bins      = total_bins.rename("bins")
    temp            = pd.concat([total_bins, df[[el, "Sterberate_%"]]], axis=1, join='inner')
    grafikdaten     = temp.groupby(["bins"])['Sterberate_%'].mean() 
    grafikdaten     = pd.concat([grafikdaten, temp["bins"].value_counts()], axis=1, join='inner')
                 
    print(el)
    plt.bar(grafikdaten.index.values.astype(str), grafikdaten["bins"], color='darkorange')
    plt.title(el, fontsize=12, fontweight="semibold") #15
    plt.xticks(grafikdaten.index.values.astype(str), rotation='vertical')
    #plt.text(0.625, 0.95, string, fontsize=15, transform=plt1.transAxes,
    #          verticalalignment='top', bbox= dict(boxstyle='round', alpha=0.5))

    plt2 = plt.twinx()
    plt2.plot(grafikdaten.index.values.astype(str), grafikdaten['Sterberate_%'], color='dodgerblue', marker='o', label='Sterberate in %')
    plt2.set_ylim([0, max(grafikdaten["Sterberate_%"])+0.5])
    plt2.set_ylabel('Sterberate in %')#,  fontsize=15)
    plt.tight_layout()
    plt.savefig('Sterberate_' + el + '.png')
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
    plt.title(el, fontsize=12, fontweight="semibold") #15
    plt.xticks(grafikdaten.index.values.astype(str), rotation='vertical')
    #plt.text(0.625, 0.95, string, fontsize=15, transform=plt1.transAxes,
    #          verticalalignment='top', bbox= dict(boxstyle='round', alpha=0.5))
    print(el)
    plt2 = plt.twinx()
    plt2.plot(grafikdaten.index.values.astype(str), grafikdaten['Sterberate_%'], color='dodgerblue', marker='o', label='Sterberate in %')
    plt2.set_ylim([0, max(grafikdaten["Sterberate_%"])+0.5])
    plt2.set_ylabel('Sterberate in %')#,  fontsize=15)
    plt.tight_layout()
    plt.savefig('Sterberate_' + el + '.png')
    plt.show()
    
    
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
               "Sterberate_%"]
               #"Prävalenz (Anteil mit mindestens einer Vorerkrankung in %)",
               #"Prävalenz-Schätzwerte plausibles Intervall Untergrenze",
               #"Prävalenz-Schätzwerte plausibles Intervall Obergrenze"]
              
total_metrisch = df[korrelation]

import seaborn as sns

plt.rcParams["figure.figsize"] = [12,12] #12
plt.rc('xtick',labelsize=15)#15
plt.rc('ytick',labelsize=15)#15

fig, ax = plt.subplots()

sns.set(font_scale=1.25)
#fig = plt.figure(figsize=(20,20))
sns.heatmap(total_metrisch.corr(method='pearson'), annot=True, fmt='.3f',
            cmap=plt.get_cmap('Oranges'), cbar=False, ax=ax, square=True) #copper_r

#plt.title('Korrelation', fontsize=15, fontweight="semibold")

#b, t = plt.ylim() # discover the values for bottom and top
#b += 0.5 # Add 0.5 to the bottom
#t -= 0.5 # Subtract 0.5 from the top
#plt.ylim(b, t) # update the ylim(bottom, top) values
ax.set_xticklabels(ax.get_xticklabels(), rotation=53)  #"horizontal")
ax.set_yticklabels(ax.get_yticklabels(), rotation="horizontal")
plt.tight_layout()
plt.savefig('Korrelation' + el + '.png')
plt.show()


