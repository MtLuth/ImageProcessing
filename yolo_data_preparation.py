import cv2
import pandas as pd
from glob import glob
import xml.etree.ElementTree as xet
import os
from shutil import copy

df = pd.read_csv('labels.csv')
df.head()

def parsing(path):
    parser = xet.parse(path).getroot()
    name = parser.find('filename').text
    filename = os.path.join("./images", name)

    parser_size = parser.find('size')
    width = int(parser_size.find('width').text)
    height = int(parser_size.find('height').text)

    return filename, width, height

df[['filename', 'width', 'height']] = df['filepath'].apply(parsing).apply(pd.Series)
df['center_x'] = (df['xmin']+df['xmax'])/(2*df['width'])
df['center_y'] = (df['ymin']+df['ymax'])/(2*df['height'])
df['bb_width'] = (df['xmax']-df['xmin'])/df['width']
df['bb_height'] = (df['ymax']-df['ymin'])/df['height']
df.head()

df_train = df.iloc[:200]
df_test = df.iloc[200:]

train_folder = './data_images/train'

values = df_train[['filename', 'center_x', 'center_y', 'bb_width', 'bb_height']].values
for fname, x, y, w, h in values:
    image_name = os.path.split(fname)[-1]
    txt_name = os.path.splitext(image_name)[0]

    dst_image_path = os.path.join(train_folder, image_name)
    dst_txt_path = os.path.join(train_folder,txt_name+".txt")

    label_txt = f'0 {x} {y} {w} {h}'

    with open(dst_txt_path, mode='w') as f:
        f.write(label_txt)
        f.close

    copy(fname, dst_image_path)

test_folder = "./data_images/test"

values = df_test[['filename', 'center_x', 'center_y', 'bb_width', 'bb_height']].values
for fname, x, y, w, h in values:
    image_name = os.path.split(fname)[-1]
    txt_name = os.path.splitext(image_name)[0]

    dst_image_path = os.path.join(test_folder, image_name)
    dst_txt_path = os.path.join(test_folder,txt_name+".txt")

    label_txt = f'0 {x} {y} {w} {h}'

    with open(dst_txt_path, mode='w') as f:
        f.write(label_txt)
        f.close

    copy(fname, dst_image_path)
print(df)