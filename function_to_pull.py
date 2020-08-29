# Dependencies
import numpy as np
import pandas as pd
import requests
from census import Census

# Census API Key
from config2 import api_key
c = Census(api_key, year=2018)

def scrape ():
    
    #Defining Variables to Pull
    countries = pd.read_csv("CodesByCountry.csv")
    baseline = countries[['code ','country ']]
    baseline = baseline.drop_duplicates(subset=['country '],keep='first')
    baseline = baseline.dropna(subset=['country '])
    countries_list = baseline['code '].values.tolist()
    countries_list.append("B05006_001E")
    countries_list_name = baseline['country '].values.tolist()
    countries_list_name.append("TotalMigration")
    population = ["B01003_001E"]

    educational_degree_code = ["B06009_025E","B06009_026E","B06009_027E","B06009_028E","B06009_029E","B06009_030E"]
    educational_degree_name = ["TotalEducation","<HighSchool","HighSchool","College","Bachelor","Graduate"]

    age_code = ["B06001_049E","B06001_050E","B06001_051E","B06001_052E","B06001_053E","B06001_055E",
                "B06001_056E","B06001_057E","B06001_058E","B06001_059E","B06001_060E"]
    age_name = ["TotalAge","<5","<18","<25","<35","<45","<55","<60","<65","<75",">75"]

    income_code = ["B06010_046E","B06010_047E","B06010_048E","B06010_049E","B06010_050E",
                "B06010_051E","B06010_052E","B06010_053E","B06010_054E","B06010_055E"]
    income_name = ["NoIncome","Income","<10,000","<15,000","<25,000","<35000","<50,000","<65,000","<75,000",">75,000"]

    sex_code = ["B06003_013E","B06003_014E","B06003_015E"]
    sex_name = ["TotalSex","Male","Female"]


    civil_status_code = ["B05007_001E","B05007_002E","B05007_003E","B05007_004E","B05007_005E","B05007_006E","B05007_007E",
                        "B05007_008E","B05007_009E","B05007_010E","B05007_011E","B05007_012E","B05007_013E"]
    civil_stats_name = ["TotalCivil",">2010",">2010NotCitizen",">2010Citizen",">2000",">2000NotCitizen",">2000Citizen",
                    ">1990",">1990NotCitizen",">1900Citizen","<1990","<1990NotCitizen","<1900Citizen"]
    #Creating String to Pull
    data = population + educational_degree_code + age_code + income_code + sex_code + civil_status_code
    key=data[0]
    for i in range(1,len(data)):
        key = key+","+data[i]
        
    key2=countries_list[0]
    for i in range(1,49):
        key2 = key2+","+countries_list[i]

    key3=countries_list[49]
    for i in range(50,98):
        key3 = key3+","+countries_list[i]

    key4=countries_list[98]
    for i in range(99,len(countries_list)):
        key4 = key4+","+countries_list[i]

    #Pull Data    
    census_data = c.acs5.get(("NAME", key), {'for': 'state:*'})
    census_data = pd.DataFrame(census_data)
    census_country1=c.acs5.get(("NAME", key2), {'for': 'state:*'})
    census_country1=pd.DataFrame(census_country1)
    census_country1 = census_country1.drop(columns=['NAME'])
    census_country2=c.acs5.get(("NAME", key3), {'for': 'state:*'})
    census_country2=pd.DataFrame(census_country2)
    census_country2 = census_country2.drop(columns=['NAME'])
    census_country3=c.acs5.get(("NAME", key4), {'for': 'state:*'})
    census_country3=pd.DataFrame(census_country3)
    census_country3 = census_country3.drop(columns=['NAME'])

    data_df = census_data.merge(census_country1,left_on="state",right_on="state")
    data_df = data_df.merge(census_country2,left_on="state",right_on="state")
    data_df = data_df.merge(census_country3,left_on="state",right_on="state")

    names_list = ["State_Name","Population"]+educational_degree_name + age_name + income_name + sex_name + civil_stats_name+["State"]
    for x in countries_list_name:
        names_list.append(x)
    
    dic={}
    for i in range(0,len(data_df.columns)):
        dic[data_df.columns[i]]=names_list[i]

    data_df = data_df.rename(columns= dic)
    data_df = data_df.set_index('State')
    data_df = data_df.set_index('State_Name')
    data_dt_T = data_df.transpose()
    final_list=[]
    for x in data_dt_T.keys():
        data_dict={}
        data_dict["state_name"]=x
        data_dict["data"]=data_dt_T[x].to_dict()
        final_list.append(data_dict)

    return final_list
