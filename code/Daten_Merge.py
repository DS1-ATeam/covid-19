# -*- coding: utf-8 -*-
"""
Created on Thu May 28 23:35:21 2020

@author: Stefan Klug
"""

import pandas as pd

################
# Daten mergen #
################

kreise_sterberate = pd.read_csv("C:/Users/Stefan Klug/data-science-project/data/Kreise_Sterberate.csv")

kreise_altersverteilung = pd.read_csv("C:/Users/Stefan Klug/data-science-project/data/Kreise_Altersverteilung.csv")

kreise_altersverteilung.drop(['Unnamed: 0'], axis=1, inplace=True)

df_merge = pd.merge(kreise_altersverteilung, kreise_sterberate, on='ID_LK_SK')

df_merge.to_csv("C:/Users/Stefan Klug/data-science-project/data/Kreise_Sterberate_merged.csv")