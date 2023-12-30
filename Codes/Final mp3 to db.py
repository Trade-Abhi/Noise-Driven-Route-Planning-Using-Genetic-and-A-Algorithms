#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import librosa
import pandas as pd

# Initialize an empty DataFrame to store results
results = pd.DataFrame(columns=['File Name', 'Decibels'])

# Loop through file numbers
for i in range(5, 18):
    # Load audio file
    audio_file = f"ZOOM00{i:02}.mp3"
    audio_data, sr = librosa.load(audio_file)

    # Calculate root mean square
    rms = np.sqrt(np.mean(np.square(audio_data)))

    # Convert to decibels
    decibels = 20 * np.log10(rms)

    # Append result to DataFrame
    results = results.append({'File Name': audio_file, 'Decibels': decibels}, ignore_index=True)

# Save results to a spreadsheet
results.to_excel('decibels_output.xlsx', index=False)


# In[ ]:




