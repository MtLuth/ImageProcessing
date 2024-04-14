import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import cv2
import xml.etree.ElementTree as xet

df = pd.read_csv('labels.csv')
df.head()

filename = df['filepath'][0]

def getFilename(filename):  
    filename_img = xet.parse(filename).getroot().find('filename').text
    filepath_img = os.path.join("./images",filename_img)
    return filepath_img

iamge_path = list(df['filepath'].apply(getFilename))