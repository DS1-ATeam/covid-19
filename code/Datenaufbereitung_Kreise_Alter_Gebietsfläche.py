# -*- coding: utf-8 -*-
"""
Created on Tue May 26 21:36:49 2020

@author: Stefan Klug
"""

import pandas as pd

##################
# Daten einlesen #
##################

# Datensatz Geschlecht, Alter
data = pd.read_csv("C:/Users/Stefan Klug/data-science-project/data/Kreise_Alter_Geschlecht.csv", sep=';')

# Datensatz Kreise Gebietsfläche
data_flaeche = pd.read_csv("C:/Users/Stefan Klug/data-science-project/data/Kreise_Gebietsfläche.csv", sep=';', decimal=",")

#data_flaeche.fillna(0, inplace=True)

#####################
# Daten aggregieren #
#####################


# https://www-genesis.destatis.de/genesis/online#astructure

data["age_0_5"] = data["unter_3_m"] + data["3_6_m"] + data["unter_3_w"] + data["3_6_w"]

data["age_6_14"] = data["6_10_m"] + data["10_15_m"] + data["6_10_w"] + data["10_15_w"]

data["age_15_34"] =   data["15_18_m"] + data["18_20_m"] + data["20_25_m"] + data["25_30_m"] + data["30_35_m"] + data["15_18_w"] + data["18_20_w"] + data["20_25_w"] + data["25_30_w"] + data["30_35_w"]

data["age_35_59"] =   data["35_ 40_m"] + data["40_45_m"] + data["45_ 50_m"] + data["50_ 55_m"] + data["55_60_m"] + data["35_40_w"] + data["40_45_w"] + data["45_50_w"] + data["50_55_w"] + data["55_60_w"]

data["age_60_75"] = data["60_65_m"] + data["65_75_m"] + data["60_65_w"] + data["65_75_w"]

data["age_75+"] = data["75_m"] + data["75_w"]


data_new = data[["ID_LK_SK","age_0_5", "age_6_14" , "age_15_34", "age_35_59", "age_60_75", "age_75+" ]]

data_new['age_0_34']    = data_new['age_0_5'] + data_new['age_6_14']  + data_new['age_15_34']   

data_new['age_60+']     = data_new['age_60_75'] + data_new['age_75+']

data_new['sum'] = data_new['age_0_34'] + data_new['age_35_59'] + data_new['age_60+']


##############################
# Gebietsfläche mit einfügen #
##############################

data_new = pd.merge(data_new, data_flaeche, on='ID_LK_SK')

data_new['Einw_pro_qm'] = data_new['sum'] / data_new['Flaeche_in_qm']

#################
# fertigstellen #
#################

data_new['age_0_34_%'] = (data_new['age_0_34'] / data_new['sum']) * 100

data_new['age_35_59_%'] = (data_new['age_35_59'] / data_new['sum']) * 100

data_new['age_60+_%'] = (data_new['age_60+'] / data_new['sum']) * 100

data_new_final = data_new[['ID_LK_SK' ,'age_0_34_%', 'age_35_59_%' , 'age_60+_%', 'Einw_pro_qm']]


#x = [11004, 11002, 11011, 11010, 11001, 11008, 11003, 11012, 11005, 11006, 11007, 11009]

x_sorted = [11001, 11002, 11003, 11004, 11005, 11006, 11007, 11008, 11009, 11010, 11011, 11012]

for x in x_sorted:
    
    new_row = {'ID_LK_SK':x, 'age_0_34_%':40.448, 'age_35_59_%':34.8899, 'age_60+_%':24.6621, 'Einw_pro_qm':891.12}
    data_new_final = data_new_final.append(new_row, ignore_index=True)

data_new_final.fillna(0, inplace=True)

data_new_final.to_csv("C:/Users/Stefan Klug/data-science-project/data/Kreise_Altersverteilung.csv")

