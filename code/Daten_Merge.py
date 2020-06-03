# -*- coding: utf-8 -*-
"""
Created on Thu May 28 23:35:21 2020

@author: Stefan Klug
"""

import pandas as pd

################
# Daten mergen #
################

kreise_sterberate = pd.read_csv("../data/01_RKI_Kreise_Sterberate.csv")

kreise_altersverteilung = pd.read_csv("../data/01_Kreise_Altersverteilung_Fläche.csv")

kreise_altersverteilung.drop(['Unnamed: 0'], axis=1, inplace=True)

df_merge = pd.merge(kreise_altersverteilung, kreise_sterberate, on='ID_LK_SK')

kreise_AOK = pd.read_csv("../data/01_AOK_aufbereitet.csv")

kreise_AOK.drop(['Unnamed: 0', 'Kreisname'], axis=1, inplace=True)

df_merge = pd.merge(df_merge, kreise_AOK, on='ID_LK_SK')

#df_merge.to_csv("../data/02_Daten_merged.csv")