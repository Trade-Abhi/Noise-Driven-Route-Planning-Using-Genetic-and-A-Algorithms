#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import folium
from folium.plugins import HeatMap


# In[2]:


df = pd.read_excel('Final Noise Details.xlsx')
df.head()


# In[3]:


#Creating a folium map object centered around the average of the latitude and longitude coordinates
center_lat = df['Latitude'].mean()
center_lon = df['Longitude'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)


# In[4]:


#Adding the data points to the map as heat map using the noise levels as weights:
heatmap_data = [[row['Latitude'], row['Longitude'], row['Noise Level Data(db)']] for index, row in df.iterrows()]
HeatMap(heatmap_data, name='Heatmap', radius=15, max_zoom=13).add_to(m)


# In[5]:


#Finally, add a layer control to the map to allow users to toggle the heat map on and off:
folium.LayerControl().add_to(m)


# In[6]:


#Save the map to an HTML file:
m.save('Final IISERB Heat MAP.html')


# In[ ]:





# In[ ]:




