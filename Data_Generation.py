import nltk
from nltk import word_tokenize, sent_tokenize, pos_tag
import pandas as pd
import os
import re
from xml.dom import minidom
from xml.etree import cElementTree as ET
from Data_Preprocessing import spans, BIO_tagging

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

class Data_generation():

    def __init__(self, path):
        self.path = path
        self.text_content_tags = {}
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.BIO_tags = {}
        self.template = {}


    def set_text_content_tags(self):
        for section in self.root[0].findall('Section'):
            tags = []
            for mention in self.root[1].findall('Mention'):
                if mention.attrib['section'] == section.attrib['id']:
                    tags.append(mention)
                self.text_content_tags[section.text] = tags

    

    def sentence_divide(self,text):
        """
        This function divides the text into sentences
        Input: Text
        Output: A list of sentences
        """
        tokens = nltk.sent_tokenize(text)

        sentences = []

        offset = 0
        for token in tokens:
            offset = text.find(token, offset)
            yield token, offset, offset+len(token)
            sentences.append((token, offset, offset+len(token)))
            offset += len(token)

        return sentences

    

    def data_preprocess(self):
        for key, value in self.text_content_tags.items():
            text = key
            tags = value
            # print(len(tags))

            sentences = self.sentence_divide(text)
            # print(sentences)
            BIO_tags = BIO_tagging(tags, text)

            word_count = 0

            for sentence in list(sentences):
                words = nltk.word_tokenize(sentence[0])
                self.BIO_tags[sentence] = BIO_tags[word_count:word_count+len(words)]

                sen_start = sentence[1]
                sen_end = sentence[2]
                templates = []

                for tag in tags:
                    pos = tag.attrib['start'].split(',')
                    length = tag.attrib['len'].split(',')

                    if len(pos) == 1:
                            
                            c_pos = int(pos[0])
                            c_length = int(length[0])
    
                            if sen_start <= c_pos and sen_end >= c_pos+c_length:
                                # print("sentence start: ", sen_start)
                                # print("sentence end: ", sen_end)
                                # print("tag start: ", c_pos)
                                # print("tag end: ", c_pos+c_length)
                                templates.append(tag.attrib['str'] + " is a " + tag.attrib['type'] + " entity")
                    else:
                        b_pos = int(pos[0])
                        b_length = int(length[0])

                        e_pos = int(pos[-1])
                        e_length = int(length[-1])

                        if sen_start <= b_pos and sen_end >= e_pos+e_length:
                            # print("sentence start: ", sen_start)
                            # print("sentence end: ", sen_end)
                            # print("tag start: ", c_pos)
                            # print("tag end: ", c_pos+c_length)
                            templates.append(tag.attrib['str'] + " is a " + tag.attrib['type'] + " entity")

                self.template[sentence] = templates

                word_count += len(words)





