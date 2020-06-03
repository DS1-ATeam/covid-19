# -*- coding: utf-8 -*-
"""
Created on Thu May 28 09:45:21 2020

@author: Luis Hohmann
"""

import pandas as pd
import numpy as np


df = pd.read_csv(filepath_or_buffer="../data/00_AOK_wido_c_12.csv", sep=';')

# convert "Anzahl Patienten mit mindestens einer Vorerkrankung" to int
df["Anz_Pati_mind_einer_Vorerkrankung"] = df["Anzahl Patienten mit mindestens einer Vorerkrankung"].str.replace(',','').astype(int)


#####################################
# Bezeichnungen kongruent gestalten #
#####################################


df.loc[df.Kreisname == 'Altenkirchen (Westerwald)',             'Kreisname'] = "Altenkirchen"
df.loc[df.Kreisname == 'Brandenburg an der Havel',              'Kreisname'] = "Brandenburg a.d"
df.loc[df.Kreisname == 'Dillingen an der Donau',                'Kreisname'] = "Dillingen a.d.D"
df.loc[df.Kreisname == 'Eifelkreis Bitburg-Prüm',               'Kreisname'] = "Bitburg-Prüm"
df.loc[df.Kreisname == 'Frankenthal (Pfalz)',                   'Kreisname'] = "Frankenthal"
df.loc[df.Kreisname == 'Freiburg im Breisgau',                  'Kreisname'] = "Freiburg i.Brei"
df.loc[df.Kreisname == 'Halle (Saale)',                         'Kreisname'] = "Halle"
df.loc[df.Kreisname == 'Kempten (Allgäu)',                      'Kreisname'] = "Kempten"
df.loc[df.Kreisname == 'Landau in der Pfalz',                   'Kreisname'] = "Landau i.d.Pfalz"
df.loc[df.Kreisname == 'Landsberg am Lech',                     'Kreisname'] = "Landsberg a.Lec"
df.loc[df.Kreisname == 'Lindau (Bodensee)',                     'Kreisname'] = "Lindau"
df.loc[df.Kreisname == 'Ludwigshafen am Rhein',                 'Kreisname'] = "Ludwigshafen"
df.loc[df.Kreisname == 'Mühldorf am Inn',                       'Kreisname'] = "Mühldorf a.Inn"
df.loc[df.Kreisname == 'Mülheim an der Ruhr',                   'Kreisname'] = "Mülheim a.d.Ruh"
df.loc[df.Kreisname == 'Neumarkt in der Oberpfalz',             'Kreisname'] = "Neumarkt i.d.OP"
df.loc[df.Kreisname == 'Neustadt an der Aisch - Bad Windsheim', 'Kreisname'] = "Neustadt a.d.Ai"
df.loc[df.Kreisname == 'Neustadt an der Waldnaab',              'Kreisname'] = "Neustadt a.d.Wa"
df.loc[df.Kreisname == 'Neustadt an der Weinstraße',            'Kreisname'] = "Neustadt a.d.We"
df.loc[df.Kreisname == 'Offenbach am Main',                     'Kreisname'] = "Offenbach"
df.loc[df.Kreisname == 'Pfaffenhofen an der Ilm',               'Kreisname'] = "Pfaffenhofen a."
df.loc[df.Kreisname == 'Regionalverband Saarbrücken',           'Kreisname'] = "Stadtverband Saarbrückenau"
df.loc[df.Kreisname == 'Region Hannover',                       'Kreisname'] = "Hannover"
df.loc[df.Kreisname == 'Saarpfalz-Kreis',                       'Kreisname'] = "Saar-Pfalz-Kreis"
df.loc[df.Kreisname == 'Städteregion Aachen',                   'Kreisname'] = "Aachen"
df.loc[df.Kreisname == 'St, Wendel',                            'Kreisname'] = "Sankt Wendel"
df.loc[df.Kreisname == 'Weiden in der Oberpfalz',               'Kreisname'] = "Weiden i.d.OPf."
df.loc[df.Kreisname == 'Wunsiedel im Fichtelgebirge',           'Kreisname'] = "Wunsiedel i.Fic"


################
# Daten mergen #
################

landkreise_ID = pd.read_csv("C:/Users/Stefan Klug/data-science-project/data/01_RKI_Kreise_Sterberate.csv")[["Landkreis","ID_LK_SK"]]

landkreise_ID["sub_L"] = landkreise_ID.Landkreis.str.slice(3, 18)

df["Kreisname_2"] = np.where(df.Kreisname.str.contains("Landkreis"), 'LK ' + df.Kreisname, df.Kreisname)

df["sub_L"] = df.Kreisname_2.str.slice(0, 15)

merged = landkreise_ID

merged = merged.merge(df[['Kreisname', 'sub_L']], on='sub_L', how='left')


merged["sub_L_2"] = np.where(merged.Landkreis.str.contains("LK"), 'LK ' + landkreise_ID.sub_L, landkreise_ID.sub_L)

merged["sub_L_2"] = merged.sub_L_2.str.slice(0, 9)

df["sub_L_2"] = np.where(df.Kreisname.str.contains("Landkreis"), 'LK ' + df.Kreisname, '')

df["sub_L_2"] = df.sub_L_2.str.slice(0, 9).str.replace(',','')

df.loc[df.sub_L_2 == 'LK Hof L',           'sub_L_2'] = "LK Hof"


merged = merged.merge(df[['Kreisname', 'sub_L_2']], on='sub_L_2', how='left')

merged['Kreisname_aktuell'] = np.where(merged.Kreisname_y.isnull() , merged.Kreisname_x, merged.Kreisname_y)

#####
#   #
#####

keys = merged[["Kreisname_aktuell", "ID_LK_SK"]]

keys.rename(columns={"Kreisname_aktuell": "Kreisname"}, inplace=True)

new = df.merge(keys, on='Kreisname', how='left')

columns = ["ID_LK_SK",
           "Kreisname",
           #"Anz_Pati_mind_einer_Vorerkrankung",
           "Prävalenz (Anteil mit mindestens einer Vorerkrankung in %)",
           "Prävalenz-Schätzwerte plausibles Intervall Untergrenze",
           "Prävalenz-Schätzwerte plausibles Intervall Obergrenze"]

new = new[columns]

new.to_csv("../data/01_AOK_aufbereitet.csv")