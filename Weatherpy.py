
# coding: utf-8

# In[3]:


import requests
from citipy import citipy
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import logging 
import seaborn as sns


# In[4]:


api_address = "http://api.openweathermap.org/data/2.5/weather?appid=5c7b46742bf289485bb109e974fc6779&q="
api_key = '5c7b46742bf289485bb109e974fc6779'


# In[5]:


cities = []
coordinates = []

lat = np.random.uniform(low=-90, high=90, size=2500)
lng = np.random.uniform(low=-180, high=180, size=2500)

for x in range(0,len(lat)):
    coordinates.append((lat[x], lng[x]))
    
for coordinate_pair in coordinates:
    lat, lon = coordinate_pair
    cities.append(citipy.nearest_city(lat, lon))


cities_df = pd.DataFrame(cities)
cities_df["City Name"] = ""
cities_df["Country Code"] = ""
cities_df.head()


# In[6]:


print(coordinates[1])
print(cities[1])


# In[7]:


coordinates_df = pd.DataFrame({"Lat": lat,
                              "Lon": lng})
coordinates_df.head()


# In[9]:


coord_df = coordinates_df
coord_df.head()


# In[10]:


coord_df['City Name'] = ""
coord_df['Country'] = ""
coord_df['Temperature (F)'] = ""
coord_df['Humidity (%)'] = ""
coord_df['Cloudiness (%)'] = ""
coord_df['Wind Speed (mph)'] = ""

coord_df.head()


# In[11]:


for index, row in cities_df.iterrows():
    row["City Name"] = cities_df.iloc[index,0].city_name
    row["Country Code"] = cities_df.iloc[index,0].country_code
    #iloc[index,0]
print(cities_df)
# Drop duplicate cities.
cities_df.drop_duplicates(['City Name', 'Country Code'], inplace=True)
cities_df.reset_index(inplace=True)

# # Delete unnecessary columns
del cities_df[0]
del cities_df['index']

cities_df.head()


# In[12]:


cities_df.head()


# In[13]:


cities_df['Latitude'] = ""
cities_df['Longitude'] = ""
cities_df['Temperature (F)'] = ""
cities_df['Humidity (%)'] = ""
cities_df['Cloudiness (%)'] = ""
cities_df['Wind Speed (mph)'] = ""

cities_df.head()


# In[14]:


url = "http://api.openweathermap.org/data/2.5/weather?"
units = "imperial"
query_url = f"{url}appid={api_key}&units={units}"


# In[16]:


for index, row in cities_df.iterrows():

    print(index, row, row['City Name'], row['Country Code']) 
    print("Processing Record " + str(index) + "of Set 1 | " + str(row['City Name']))

    url = "http://api.openweathermap.org/data/2.5/weather?appid=%s&q=%s&units=imperial" % (api_key, row['City Name'])
    print(url)
    weather_data = requests.get(url)
    #.json() above
    print(weather_data.url)
    weather_data = weather_data.json()
    #Append
    
    try:

        lati = weather_data['coord']['lat']
        long = weather_data['coord']['lon']
        temper = weather_data['main']['temp']
        humi = weather_data['main']['humidity']
        cloud = weather_data['clouds']['all']
        wind = weather_data['wind']['speed']
        
        cities_df.set_value(index, "Latitude", lati)
        cities_df.set_value(index, "Longitude", long)
        cities_df.set_value(index, "Temperature (F)", temper)
        cities_df.set_value(index, "Humidity (%)", humi)
        cities_df.set_value(index, "Cloudiness (%)", cloud)
        cities_df.set_value(index, "Wind Speed (mph)", wind)
        

    except:
        print("Error")
        continue
 


# In[18]:


cities_df.head()


# In[21]:


path_d = 'C:\\Users\\user\\Desktop\\weather'
cities_df.to_csv(os.path.join(path_d, 'weatherpy.csv'))


# In[25]:


cities_df = cities_df[pd.notnull(cities_df['Latitude'])]
cities_df


# In[26]:


columns = ['Latitude', 'Temperature (F)', 'Humidity (%)', 'Cloudiness (%)', 'Wind Speed (mph)']
for column in columns:
    cities_df[column] = pd.to_numeric(cities_df[column], errors='coerce')
    
cities_df.dropna(inplace=True)

cities_df.head()


# In[27]:


path_d = 'C:\\Users\\user\\Desktop\\weather'
cities_df.to_csv(os.path.join(path_d, 'weatherpy2.csv'))


# In[29]:


plt.scatter(cities_df["Latitude"],
            cities_df["Temperature (F)"])
plt.title("City Latitude vs. Max Temperature")
plt.ylabel("Temperature (F)")
plt.axvline(0, color = 'black', alpha = .25, label = 'Equator')
plt.text(1,30,'Equator',rotation=90)
plt.ylim(-50,120)
plt.xlabel("Latitude")
plt.xlim(-60,90)
plt.grid(True)
plt.savefig("LatVsTemp.png")
plt.show()


# In[31]:


plt.scatter(cities_df["Latitude"],
            cities_df["Humidity (%)"])
plt.title("Latitude vs. Humidity Plot")
plt.ylabel("Humidity (%)")
plt.axvline(0, color = 'black', alpha = .25, label = 'Equator')
plt.text(1,30,'Equator',rotation=90)
plt.ylim(-50,120)
plt.xlabel("Latitude")
plt.xlim(-60,90)
plt.grid(True)
plt.savefig("LatVsHum.png")
plt.show()


# In[32]:


plt.scatter(cities_df["Latitude"],
            cities_df["Cloudiness (%)"])
plt.title("Latitude vs. Cloudiness Plot")
plt.ylabel("Cloudiness (%)")
plt.ylim(-50,120)
plt.axvline(0, color = 'black', alpha = .25, label = 'Equator')
plt.text(1,30,'Equator',rotation=90)
plt.xlabel("Latitude")
plt.xlim(-60,90)
plt.grid(True)
plt.savefig("LatVsCloud.png")
plt.show()


# In[33]:


plt.scatter(cities_df["Latitude"],
            cities_df["Wind Speed (mph)"])
plt.title("Latitude vs. Windspeed Plot")
plt.ylabel("Wind Speed (mph)")
plt.axvline(0, color = 'black', alpha = .25, label = 'Equator')
plt.text(1,30,'Equator',rotation=90)
plt.ylim(-5,40)
plt.xlabel("Latitude")
plt.xlim(-60,90)
plt.grid(True)
plt.savefig("LatitudeVsWindSpeed.png")
plt.show()

