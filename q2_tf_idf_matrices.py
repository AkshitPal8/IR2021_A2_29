# -*- coding: utf-8 -*-
"""Q2 TF-IDF Matrices.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1niZAkrYIQ-YhBLSHOY4WOhMRZcO3Bf26
"""

import os
import pickle
import codecs
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import math

"""Navigate to working directory"""

cd '/content/drive/MyDrive/College/Semester 8/IR/Assignment 2'

"""Unpickle the positional index and file map"""

index = pickle.load(open("pos_index_final.pkl","rb"))
file_map = pickle.load(open("file_map.pkl","rb"))

#succesfully loaded, this has been tested - these are ok in general

"""Make a vocabulary map first"""

word_ID = 1    #the words will be following one-based indexing as the files have followed the same
vocab_map = {}

wordlist = index.keys()

for word in wordlist:

  vocab_map[word_ID] = word
  word_ID += 1

#vocab_map made successfully - tested

"""Pickle vocabulary map as "word_map""""

opfile = open('word_map.pkl','wb')
pickle.dump(vocab_map,opfile)
opfile.close()

#DON'T RUN THIS CELL AGAIN

"""At the moment, word_ID - 1 = vocabsize, thus we save it as such. This will be useful when **computing TF-IDF scores for a query**"""

vocab_size = word_ID - 1  #this is also correct

"""We also need to make an inverse word map to handle the query"""

inv_vocab_map = {}

for i in vocab_map.keys():

  inv_vocab_map[vocab_map[i]] = i

# also works

"""We should pickle this as well"""

#PICKLE inv_vocab_map
opfile = open('inverse_word_map.pkl','wb')
pickle.dump(inv_vocab_map,opfile)
opfile.close()

#DON'T RUN THIS CELL AGAIN

"""Similarly, making an inverse file map may help us later. Pickle this too"""

#MAKE inv_file_map

#PICKLE the inverse file map also

"""Function to compute idf score given word_ID"""

def IDF(word_ID):

  if word_ID not in vocab_map:
    return 0

  word = vocab_map[word_ID]
  df = len(index[word][1])

  idf = len(file_map.keys())/df   # total number of documents / number of documents containing given word
  idf += 1
  idf = math.log(idf) #if required, change this to math.log(idf, base=10)  

  return idf

#checked, works all right

"""Functions to compute tf score of a given (file_ID, word_ID) pair using 

1.   Binary
2.   Raw count
3.   term frequency
4.   log normalization
5.   double normalization


"""

def tf_binary(file_ID, word_ID):

  if word_ID not in vocab_map:
    return 0

  word = vocab_map[word_ID]

  if file_ID in index[word][1]:

    return 1

  else:

    return 0

#works fine

def tf_raw_count(file_ID, word_ID):

  if word_ID not in vocab_map:
    return 0

  word = vocab_map[word_ID]

  if file_ID in index[word][1]:

    tf = len(index[word][1][file_ID])
    return tf

  else:

    return 0

#works fine

"""In **TF Term Frequency** want to avoid summing over all words everytime so we precompute this for all documents."""

term_freq_helper = [0]*(len(file_map.keys()) + 1)
# precompute Sum(frquency(word', fileno)) for all documents

for file_ID in file_map.keys():

  for word in inv_vocab_map.keys():

    if file_ID in index[word][1]:

      term_freq_helper[file_ID] += len(index[word][1][file_ID])

#the sums have been precomputed
#works fine

def tf_term_frequency(file_ID, word_ID):

  if word_ID not in vocab_map:
    return 0

  word = vocab_map[word_ID]

  if file_ID in index[word][1]:

    tf = len(index[word][1][file_ID])

    #Sum of term frequencies of all words in document
    tfsum = term_freq_helper[file_ID]

    tf = tf / tfsum
    return tf

  else:

    return 0

#also works fine

def tf_log_normalization(file_ID, word_ID):

  if word_ID not in vocab_map:
    return 0

  word = vocab_map[word_ID]

  if file_ID in index[word][1]:

    tf = len(index[word][1][file_ID]) + 1
    tf = math.log(tf)   #if required, change this to math.log(tf, base = 10)
    return tf

  else:

    return 0

# works fine

"""For **Double Normalization TF** we need a similar helper list to avoid excess computation"""

double_normalization_helper = [0]*(len(file_map.keys()) + 1)
# precompute max(frquency(word', fileno)) for all documents

for file_ID in file_map.keys():

  cur = -1

  for word in inv_vocab_map.keys():

    if file_ID in index[word][1]:
      
      cur = max(cur, len(index[word][1][file_ID]))
    
  double_normalization_helper[file_ID] = cur

#the maximums have been precomputed
#works fine

def tf_double_normalization(file_ID, word_ID):

  if word_ID not in vocab_map:
    return 0.5

  word = vocab_map[word_ID]

  if file_ID in index[word][1]:

    tf = len(index[word][1][file_ID])

    #to compute maximum of term frequencies of all words in document
    maximum = double_normalization_helper[file_ID]

    tf = 0.5*(tf/maximum)
    tf += 0.5

    return tf

  else:

    return 0.5

#works fine again

"""Now that the functions are made, we need to make and pickle the tf idf tables using all of the given tf metrics.

We choose to make each table as a **2D List** as this will help us easily get tf-idf vectors for individual documents when we need them for cosine similarity computations
"""

num_files = len(file_map.keys())
num_words = vocab_size

print(index[vocab_map[6]][1])
print(index['negatory'][1])

#Precalculate IDF scores for all words

IDF_score = {}

for word_ID in vocab_map.keys():

  IDF_score[word_ID] = IDF(word_ID)

# works fine

"""TF-IDF Matrix using Binary TF - **DONE**"""

print(tf_binary(433, 6)*IDF_score[6])
print(tf_binary(432, 6)*IDF(6))

i1, i2, j1, j2 = 433, 432, 6, 6

print(tf_binary(i1, j1)*IDF(j1))
print(tf_binary(i2, j1)*IDF(j1))

Mat_Binary = [[0]*(len(vocab_map.keys())+1)]

for i in file_map.keys():

  m = [0]

  for j in vocab_map.keys():

    tfscore = tf_binary(i, j)
    tfidf = tfscore*IDF_score[j]
    m.append(tfidf)

  Mat_Binary.append(m)

#THIS was where the issue was, it is working now

print(Mat_Binary[433][6])
print(Mat_Binary[433])
print(Mat_Binary[0])
print(len(Mat_Binary[433]))
print(len(Mat_Binary[0]))

#Pickle the above matrix

opfile = open('Binary_TF-IDF_Matrix.pkl','wb')
pickle.dump(Mat_Binary,opfile)
opfile.close()

print(len(word_map.keys()))

print(len(Mat_Binary[467]))

"""TF-IDF Matrix using Raw Count TF - **DONE**"""

Mat_raw_count = [[0]*(len(vocab_map.keys())+1)]

for i in file_map.keys():

  m = [0]

  for j in vocab_map.keys():

    tfscore = tf_raw_count(i, j)
    tfidf = tfscore*IDF_score[j]
    m.append(tfidf)

  Mat_raw_count.append(m)

#THIS was where the issue was, it is working now

print(Mat_raw_count[24])
print(Mat_raw_count[433])

#Pickle the above matrix

opfile = open('Raw_Count_TF-IDF_Matrix.pkl','wb')
pickle.dump(Mat_raw_count,opfile)
opfile.close()

"""TF-IDF Matrix using Term Frequency TF - **DONE**"""

Mat_term_frequency = [[0]*(len(vocab_map.keys())+1)]

for i in file_map.keys():

  m = [0]

  for j in vocab_map.keys():

    tfscore = tf_term_frequency(i, j)
    tfidf = tfscore*IDF_score[j]
    m.append(tfidf)

  Mat_term_frequency.append(m)

#THIS was where the issue was, it is working now

print(Mat_term_frequency[130])
print(Mat_term_frequency[433])

#Pickle the above matrix

opfile = open('Term_Frequency_TF-IDF_Matrix.pkl','wb')
pickle.dump(Mat_term_frequency,opfile)
opfile.close()

"""TF-IDF Matrix using Log normalization TF - **DONE**"""

Mat_log_normalization = [[0]*(len(vocab_map.keys())+1)]

for i in file_map.keys():

  m = [0]

  for j in vocab_map.keys():

    tfscore = tf_log_normalization(i, j)
    tfidf = tfscore*IDF_score[j]
    m.append(tfidf)

  Mat_log_normalization.append(m)

#THIS was where the issue was, it is working now

print(Mat_log_normalization[130])
print(Mat_log_normalization[433])

#Pickle the above matrix

opfile = open('Log_Normalization_TF-IDF_Matrix.pkl','wb')
pickle.dump(Mat_log_normalization,opfile)
opfile.close()

"""TF-IDF Matrix using Double Normalization TF - **DONE**"""

Mat_double_normalization = [[0]*(len(vocab_map.keys())+1)]

for i in file_map.keys():

  m = [0]

  for j in vocab_map.keys():

    tfscore = tf_double_normalization(i, j)
    tfidf = tfscore*IDF_score[j]
    m.append(tfidf)

  Mat_double_normalization.append(m)

#THIS was where the issue was, it is working now

print(Mat_double_normalization[130])
print(Mat_double_normalization[433])

#Pickle the above matrix

opfile = open('Double_Normalization_TF-IDF_Matrix.pkl','wb')
pickle.dump(Mat_double_normalization,opfile)
opfile.close()