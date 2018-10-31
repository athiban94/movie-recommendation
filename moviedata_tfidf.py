
# coding: utf-8

# In[16]:


import nltk
import re
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
from nltk.corpus import stopwords

import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from scipy.spatial import distance


# In[17]:


def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


# In[18]:


stop_words = stopwords.words('english')

#adding new stopwords based upon domain knowledge
stop_words.append('nan')

wordnet_lemmatizer = WordNetLemmatizer()

def tokenize(keywords):
    token_count={}
    tokens=[x.strip() for x in keywords.split(",")]
    #print(tokens)
    tag_token=nltk.pos_tag(tokens)
    #print(tag_token)
    lem_tok=[]
    for (w,tag) in tag_token:
        if w not in stop_words:
            lem_tok.append(wordnet_lemmatizer.lemmatize(w, get_wordnet_pos(tag)))
    #print(lem_tok)
    
    token_count=nltk.FreqDist(lem_tok)
        
    return token_count


# In[19]:


def get_top_words(mvdata,n):
    
    topwrds_dict={}
    labels=list(mvdata.keys())
    
    doc_dict={}
    for lb in mvdata.keys():
        doc_dict[lb]=tokenize(mvdata[lb])
    
    #calculate tfidf matrix
    
    #create matrix from dictionary
    dtm=pd.DataFrame.from_dict(doc_dict,orient="index")
    dtm=dtm.fillna(0)
    
    #get normalized term frequency (tf) matrix        
    tf=dtm.values
    doc_len=tf.sum(axis=1)
    tf=np.divide(tf.T, doc_len).T
    
    #get idf
    df=np.where(tf>0,1,0)
    idf=np.log(np.divide(len(mvdata.values()),np.sum(df, axis=0)))+1
    
    #tfidf
    tfidf=normalize(tf*idf)
    #print(tfidf)
    
    smoothed_idf=np.log(np.divide(len(mvdata.values())+1, np.sum(df, axis=0)+1))+1
    #print(smoothed_idf)
    smoothed_tf_idf=normalize(tf*smoothed_idf)
    #print(smoothed_tf_idf)
    
    top=smoothed_tf_idf.argsort()[:,::-1][:,0:n]
    #print(top)
    for idd,row in enumerate(top):
        topwrds_dict[labels[idd]]=[dtm.columns[x] for x in row]
        
    return topwrds_dict


# In[20]:


#fieldname=["category","movie","title","rating","genre","subgenre","theme","keyword","releasedate","country","review"]
#with open('movie10k.csv') as csv_file:
mvdf = pd.read_csv("movie10k.csv", header =0,encoding="ISO-8859-1")
mvkeydict={}
mvthemedict={}
for index, row in mvdf.iterrows():
    label=row["category"]
    if label in mvkeydict.keys():
        mvkeydict[label]=mvkeydict[label]+","+str(row["keyword"])
    else:
        mvkeydict[label]=str(row["keyword"])
    if label in mvthemedict.keys():
        mvthemedict[label]=mvthemedict[label]+","+str(row["theme"])
    else:
        mvthemedict[label]=str(row["theme"])   
    
#print top n keywords by category
print("print top keywords by category:")
print(get_top_words(mvkeydict,3))

#print top n themes by category
print("print top themes by category:")
print(get_top_words(mvthemedict,3))

