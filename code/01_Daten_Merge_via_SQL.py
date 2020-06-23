# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 15:24:19 2020

@author: Stefan Klug
"""


import sqlalchemy as db
import pandas as pd

'''
###################################
# Daten von MySQL-Datenbank laden #
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

'''
j = students.join(addresses, students.c.id == addresses.`c.st_id`)
stmt = select([students]).select_from(j)
result = conn.execute(stmt)
result.fetchall()

import pandas as pd

metadata    = db.MetaData()
table       = db.Table('Gesamt123', metadata, autoload=True, autoload_with=engine)
query       = db.select([table])

results     = con.execute("SELECT * FROM Gesamt123").fetchall()
df          = pd.DataFrame(results)
df.columns  = results[0].keys()
df.info()
'''



'''
a =  "`a.ID_LK_SK`, `a.LK_SK`, `a.Landkreis`, `a.Bundesland`, `a.age_covid_0_34_%`, `a.age_covid_35_59_%`, `a.age_covid_60+_%`, `a.age_covid_unknown_%`, `a.gender_covid_f_%`, `a.gender_covid_m_%`, `a.gender_covid_unknown_%`, `a.Sterberate_%`, "                       

b = "`b.age_0_34_%`, `b.age_35_59_%`, `b.age_60+_%`, `b.Einw_pro_qm`, "

c = "`c.Prävalenz`, `c.Prävalenz_plausibles_Intervall_untere_Grenze`, `c.Prävalenz_plausibles_Intervall_obere_Grenze`, `c.Bluthochdruck`, `c.KHK`, `c.Herzinfarkt`, `c.Herzinsuffizienz`, `c.Schlaganfall`, `c.Diabetes`, `c.Asthma`, `c.COPD`, `c.Krebs`, `c.Lebererkrankungen`, `c.Immunschwäche`" 

# Join der 3 Datensätze
statement = "CREATE VIEW `Gesamt123` AS (Select " + a + b + c + " FROM `kreise_sterberate` a, `kreise_altersverteilung` b, `kreise_AOK` c WHERE `a.ID_LK_SK` = `b.ID_LK_SK` AND `a.ID_LK_SK` = `c.ID_LK_SK`)"   

#statement = "SELECT *, a.ID_LK_SK AS ID_LK_Temp FROM kreise_sterberate a, kreise_altersverteilung b, kreise_AOK c WHERE a.ID_LK_SK = b.ID_LK_SK AND a.ID_LK_SK = c.ID_LK_SK"

#statement = "SELECT * FROM kreise_sterberate a, kreise_altersverteilung b, kreise_AOK c WHERE a.ID_LK_SK = b.ID_LK_SK AND a.ID_LK_SK = c.ID_LK_SK"

#con.execute("SELECT *, a.ID_LK_SK, b.ID_LK_SK, c.ID_LK_SK FROM kreise_sterberate a, kreise_altersverteilung b, kreise_AOK c WHERE a.ID_LK_SK = b.ID_LK_SK AND a.ID_LK_SK = c.ID_LK_SK").fetchall()

#statement = "SELECT *, a.ID_LK_SK AS ID_LK_Temp FROM kreise_sterberate a, kreise_altersverteilung b, kreise_AOK c WHERE a.ID_LK_SK = b.ID_LK_SK AND a.ID_LK_SK = c.ID_LK_SK"


con.execute(statement)


j = students.join(addresses, students.c.id == addresses.`c.st_id`)
stmt = select([students]).select_from(j)
result = conn.execute(stmt)
result.fetchall()

import pandas as pd

metadata    = db.MetaData()
table       = db.Table('Gesamt123', metadata, autoload=True, autoload_with=engine)
query       = db.select([table])

results     = con.execute("SELECT * FROM Gesamt123").fetchall()
df          = pd.DataFrame(results)
df.columns  = results[0].keys()
df.info()
'''