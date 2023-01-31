import nltk
from nltk import word_tokenize, sent_tokenize, pos_tag
import pandas as pd
import os
import re
from xml.dom import minidom
from xml.etree import cElementTree as ET
from Data_Generation import Data_generation

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

path = r'.\data\train_xml\ADREVIEW.xml'

# for child in root:
#     print(child.tag)

example = Data_generation(path)

example.set_text_content_tags()

example.data_preprocess()

count = 0
for key,value in example.BIO_tags.items():
    if len(value) !=0:
        count += len(value)
        print(key,value)
    
