import sys, re, time, string
import numpy as np

import read_wikirandom
import parse_document
import read_pubmed

def gettopwords(lam_path, M, K, V):
    f = open(lam_path).readlines()
    topwords = np.zeros((K, M), dtype = np.int)
    lam = np.zeros((K,V))
    for i in range(len(f)):
        l = f[i].split()
        for j in range(len(l)):
            lam[i,j] = l[j]
    for k in range(0, K):
        topic = lam[k]
        topwords_k = np.flipud(np.argsort(topic))[0:M]
        topwords[k] = topwords_k
        
    return topwords
    


class TopicCoherence():
    def __init__(self, K, M, D, topwords):
        self._K = K
        self._M =M
        self._D =D
        self._topwords = topwords
        self._df = np.zeros((self._K, self._M))
        self._cdf = np.zeros((self._K, self._M, self._M))
        self._TopicCoherence = np.zeros(self._K)
        
    def count_df(self, ids):
        for k in range(0, self._K):
            for m in range(0, self._M):
                w = self._topwords[k][m]
                if w in ids:
                    self._topwords[k][m] = self._topwords[k][m] + 1
    
    def count_cdf(self, ids):
        for k in range(0, self._K):
            for m in range(1, self._M):
                for l in range (0, m):
                    w1 = self._topwords[k][m]
                    w2 = self._topwords[k][l]
                    if (w1 in ids and w2 in ids):
                        self._cdf[k][m][l] = self._cdf[k][m][l] + 1
    
    def count_df_cdf(self, ids):
        
        for k in range(0, self._K):
            
            w = self._topwords[k][0]
            if w in ids:
                self._df[k][0] = self._df[k][0] + 1
            
            for m in range(1, self._M):
                w1 = self._topwords[k][m]
                if w1 in ids:
                    self._df[k][m] = self._df[k][m] + 1
                    for l in range (0, m):
                        w2 = self._topwords[k][l]
                        if (w2 in ids):
                            self._cdf[k][m][l] = self._cdf[k][m][l] + 1
    
    
    def count_df_cdf_1(self, ids):
        for k in range(0, self._K):
            #ids_k = ids
            topwords_ids_k = list()
           
            
            for m in range(0, self._M):
                w = self._topwords[k][m]
                if w in ids:
                    self._df[k][m] = self._df[k][m] + 1
                    #ids_k.remove(w)
                    topwords_ids_k.append(w)
            
            if (len(topwords_ids_k) < 2):
                continue
                    
            for i in range (1, len(topwords_ids_k)):
                for j in range(0, i):
                    ii = np.where (self._topwords[k] == topwords_ids_k[i] ) [0][0]
                    jj =  np.where (self._topwords[k] == topwords_ids_k[j] ) [0][0]
                    
                    m=-1
                    l=-1
                    if (ii > jj):
                        m = ii
                        l = jj
                    if (ii < jj):
                        m = jj
                        l = ii
                    self._cdf[k][m][l] = self._cdf[k][m][l] + 1
    
    def calculate_tc(self):
      #  self._df = self._df / self._D
       # self._cdf = self._cdf / self._D
        
        for k in range (0, self._K):
            tc_k = 0.0
            cdf_k = self._cdf[k]
            df_k = self._df[k]
            for m in range(1, self._M):
                for l in range (0, m):
                    temp = float((cdf_k[m][l] + 1) / (df_k[l] + 1))
                    tc_k = tc_k + np.log(temp)
            
            self._TopicCoherence[k] = tc_k
    
    def outputresults(self):
        f = open("./topic_coherence.txt", "w")
        for tc in self._TopicCoherence:
            f.write(str(tc))
            f.write("\n")
        f.close()
        
if __name__ == '__main__':
    
    lam_path = ""
    vocab = file("").readlines()
    V = len(vocab)
    M = 20
    K = 100
    D = 1e6
    batchsize = 5000
    document_num=0
    txt_num=0
    iterations = int (D / batchsize)
    topwords = gettopwords(lam_path, M, K, V)
    topiccoherence = TopicCoherence(K, M, D, topwords)
    
    for i in range(0, iterations):
        print i
        #(docset,document_num,txt_num) = \
        #read_wikirandom.get_random_wiki_articles(batchsize,document_num,txt_num)

        (docset,document_num,txt_num) = \
                                      read_pubmed.get_random_wiki_articles(batchsize,document_num,txt_num)
        (wordids,wordcts) = parse_document.parse_doc_list(docset, vocab)
        for j in range (0, len(wordids)):
            #topiccoherence.count_df_cdf(wordids[j])
            topiccoherence.count_df_cdf_1(wordids[j])
            #topiccoherence.count_df(wordids[j])
            #topiccoherence.count_cdf(wordids[j])
    
    topiccoherence.calculate_tc()
    topiccoherence.outputresults()
    print "end"
    
        
        
        
        
