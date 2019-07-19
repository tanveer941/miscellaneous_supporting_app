# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 11:35:18 2018

@author: uidj1623
"""

# -*- coding: utf-8 -*-

import os, sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import operator, re


class TFIDExtractor(object):
    
    def __init__(self, query):
        
        self.result1 = []
        self.d = {}
        self.dict1 = {}
        self.wordss=[]
        self.query = query
    
        self.stopword = frozenset([
                        'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again',
                        'against', 'all', 'almost', 'alone', 'along', 'already', 'also','although',
                        'always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 'another',
                        'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',
                        'at', 'back','be','became', 'because','become','becomes', 'becoming', 'been',
                        'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
                        'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can',
                        'cannot', 'cant', 'co', 'con','conditions', 'could', 'couldnt', 'cry', 'de', 'describe',
                        'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight',
                        'either', 'eleven','else', 'elsewhere', 'empty', 'enough', 'etc', 'even',
                        'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few',
                        'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former',
                        'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get',
                        'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here',
                        'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him',
                        'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc',
                        'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last',
                        'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me',
                        'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly',
                        'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
                        'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not',
                        'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
                        'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
                        'over', 'own','part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
                        'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she',
                        'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some',
                        'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere',
                        'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their',
                        'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby',
                        'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third',
                        'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus',
                        'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two','types' 
                        'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well',
                        'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
                        'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which',
                        'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will',
                        'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
                        'yourselves', 'the','recording','labels','_'])

    def get_rec_details(self):
        with open(os.path.join(os.getcwd()+'\\summary.txt'),'r') as f:
            words1 = f.read().split('\n\n')
            self.wordss = [re.sub('([.,_!?()])', r' \1 ', w) for w in words1]
            words = [l.split() for l in words1]
            for item in words:
               result = [word for word in item if '.rec' in word or '.rrec' in word] #obtaining rec names
               self.result1.append(result)  # recording names as a list
# encode document
        vectorizer1 = TfidfVectorizer(stop_words = self.stopword, lowercase=True, analyzer='word' )
        doc_vector = vectorizer1.fit_transform(self.wordss) #tf-idf matrix for summary file
        d = {i:x for i,x in enumerate(doc_vector)}    
        d1 = {i:x for i,x in enumerate(self.result1)}
####################Query######################
        print("self.query :: ", self.query)
        if self.query == []: sys.exit()
        self.query = list([self.query])
        vector2 = vectorizer1.transform(self.query)
###################Similarity##################
        cs=[]
        for key, value in d.items():
            cs = cosine_similarity(vector2, value)  # cosine scores between query and the summary file
            self.dict1[key] = cs[0][0]  #dictionary values as scores
    
        sorted_dict = sorted(self.dict1.items(), key=operator.itemgetter(1), reverse=True) #sort in decreasing order of cosine similarities
        recnames_lst = []
        for key, value in sorted_dict:
            if value == 0.0:
                continue
            else:

                recnames_lst.append(d1[key][0])
        return recnames_lst

if __name__ == '__main__':

    tfid_obj = TFIDExtractor(query="austria")
    print("tfid_obj :: ", tfid_obj)
    op_dict = tfid_obj.get_rec_details()
    print("op_dict :: ", op_dict)

         
 