import os
import pickle
import codecs
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

root = "processed/"

file_list = []
for path, subdirs, files in os.walk(root):
    for name in files:
        file_list.append(os.path.join(path, name))

file_map = pickle.load(open("file_map.pkl","rb"))


def preprocess(filetext):
        filetext = filetext.lower()

        #Punctuation removal
        filetext = re.split("[" + string.punctuation + "]+", filetext)
        filetext = " ".join(filetext)

        #Tokenization
        words = word_tokenize(filetext)

        #Stopword removal
        stop_words = set(stopwords.words('english'))
        filtered = [word for word in words if not word in stop_words]
        for i in range(len(filtered)):
            filtered[i] = filtered[i].strip()
        #print(filtered)
        
        return filtered

print('Input Query')
query = input()
query = preprocess(query)
print(query)

jaccard_coef = {}

for file in file_list:
	filename = file.split('/')[-1]
	text = codecs.open(file,'r','unicode_escape')
	filetext = text.read()
	words = filetext.split(' ')
	#print(words)
	#break

	intersection = len(list(set(words)&set(query)))
	union = len(list(set(words)|set(query)))
	jac = intersection/union



	jaccard_coef[filename] = jac

final_ans = []
def by_value(item):
	return item[1]
for k, v in sorted(jaccard_coef.items(), key=by_value):
	final_ans.append(k+"->"+str(v))

print(final_ans[:-5:-1])