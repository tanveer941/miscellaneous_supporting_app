import os, sys, string, re

class KeyWordMatching(object):
    
    def __init__(self, qry):
    
        self.qry = qry
        self.stopwords = frozenset([
                'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again',
                'against', 'all', 'almost', 'alone', 'along', 'already', 'also','although',
                'always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 'another',
                'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',
                'at', 'back','be','became', 'because','become','becomes', 'becoming', 'been',
                'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
                'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can',
                'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe',
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
                'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two',
                'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well',
                'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
                'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which',
                'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will',
                'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
                'yourselves', 'the','recording','labels'])
        self.dict1 = {}
        self.result2 = []

    def match_all(self):
        with open(os.path.join(os.getcwd()+'\\summary.txt'),'r') as f:
            contents = f.read().split('\n\n')
            for each in contents:
             words = [word for word in each.split()] 
             result1 = [word for word in words if ('.rrec' in word or '.rec' in word)] #getting recording names
             result=result1
             words = [x.lower() for x in words ]
             words = [w for w in words if w not in self.stopwords]
             words = [re.sub('([.,!?()_])', r' \1 ', w) for w in words]
             words = [x.strip(string.punctuation) for x in words]
             result=result+words
             self.result2.append(result)

        print("self.result2 :: ", self.result2)
###Creating a dictionary###
        for each in self.result2[:-1]:
            keys = each[0]
            values = each[1:]
            self.dict1.update({keys:values})
 
###User input , extracting the keywords by removing stopwords###
        if self.qry == []:
            sys.exit()
        query_kw =[w for w in self.qry.lower().split() if w not in self.stopwords]

        output = set()
        for k, each in self.dict1.items():
          if set(query_kw) < set(each):
              output.add(k)              
        return output

if __name__ == '__main__':        
    qry_match = KeyWordMatching(qry ="rain dev")
    op_dict = list(qry_match.match_all())
    print("op_dict :: ", op_dict)
    
    
    
    