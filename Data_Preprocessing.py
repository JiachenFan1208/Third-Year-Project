import nltk
from nltk import word_tokenize, sent_tokenize, pos_tag
import pandas as pd
import os
import re
from xml.dom import minidom
from xml.etree import cElementTree as ET

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def spans(txt):
    tokens=nltk.word_tokenize(txt)
    offset = 0
    for token in tokens:
        offset = txt.find(token, offset)
        yield token, offset, offset+len(token)
        offset += len(token)



def BIO_tagging(tags, text):
    """
    This function tags the text with BIO tags
    
    Input: An element of a list of tags, extracted text content
    Output: A set of tuples which consist of words and BIO tag
    """
    
    
    tagged_words = []
    tagged_position = []
    
    tokens = spans(text)
    
    for token in tokens:

        tagged = False
    
        for i in range(len(tags)):

            pos = tags[i].attrib['start'].split(',')
            length = tags[i].attrib['len'].split(',')

            if len(pos) == 1:
                
                d_pos = int(pos[0])
                d_length = int(length[0])

                if token[1] != d_pos and (d_pos >= token[1] or (d_pos+d_length) <= token[1]):
                    continue      
                else:                  
                    if token[1] == d_pos :
                        B_tag = (token[0],'B-'+ str(tags[i].attrib['type']))
                        tagged_words.append(B_tag)
                        tagged = True
                       
                        
                    elif d_pos < token[1] < d_pos+d_length:
                        I_tag = (token[0],'I-'+ str(tags[i].attrib['type']))
                        tagged_words.append(I_tag)
                        tagged = True
                        
            else:

                for m in range(len(pos)):

                    c_pos = int(pos[m])
                    c_length = int(length[m])

                    if token[1] != c_pos and (c_pos >= token[1] or (c_pos+c_length) <= token[1]):
                        continue            
                    else:
                        
                        if token[1] == c_pos and m == 0:
                            B_tag = (token[0],'B-'+ str(tags[i].attrib['type']))
                            tagged_words.append(B_tag)
                            tagged = True
                            break
                        
                        elif token[1] == c_pos and m != 0:
                            I_tag = (token[0],'I-'+ str(tags[i].attrib['type']))
                            tagged_words.append(I_tag)
                            tagged = True
                            break
                            
                        elif c_pos < token[1] < c_pos+c_length:
                            I_tag = (token[0],'I-'+ str(tags[i].attrib['type']))
                            tagged_words.append(I_tag)
                            tagged = True
                            break
                        
            if tagged == True:
                break
    
        if tagged == False:
            O_tag = (token[0],'O')
            tagged_words.append(O_tag)

    return tagged_words


def  preprocess(string):
    """
    Preprocessing for all datasets
    
    Input: A sentence from original text
    Output: Preprocessed sentence
    """
    
    string = re.sub(r"[^\w(),|!?\'\`\:\-\.;\$%#]", " ", string)
    string = re.sub(r"\'s", " is", string)
    string = re.sub(r"\'ve", " have", string)
    string = re.sub(r"n\'t", " not", string)
    string = re.sub(r"\'re", " are", string)
    string = re.sub(r"\'d", " would", string)
    string = re.sub(r"\'ll", " will", string)
    string = re.sub(r"(?<=\w)\.\.\.", " ... ", string)
    string = re.sub(r"(?<=\w)\.", " . ", string)
    string = re.sub(r"(?<=\w),", " , ", string)
    string = re.sub(r"(?<=\w);", " ; ", string)
    string = re.sub(r"(?<=\w)!", " ! ", string)
    string = re.sub(r"\((?=\w)", " ( ", string)
    string = re.sub(r"(?<=\w)\)", " ) ", string)
    string = re.sub(r"(?<=\w)\?", " ? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    
    
    #Tokenization
    tokens = word_tokenize(string)

    # Part-of-speech Tagging
    pos_tagged = pos_tag(tokens)
       
    
    return pos_tagged