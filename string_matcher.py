# -*- coding: utf-8 -*-
"""
CS481 Fall 2019 Homework 1
Exact String Matching source code file
Created on Mon Oct  7 20:45:39 2019
Revised on Tue Nov 5 19:30:05 2019
@author: İlayda Beyreli 201801130
"""
import sys
from itertools import chain
import time

def readfa(file_name):
    # Reading .FA files into lists
    with open(file_name, "r") as fin:
        data =fin.read().splitlines()
    data = list(chain.from_iterable(data[1:])) 
    return data

def bruteforce(text,pattern,alphabet):
    # The brute force approach for exact string matching
    init_time = time.time()
    comparisons = 0
    occurs = False
    location = None
    n = len(text)
    m = len(pattern)
    i = 1
    while i < n:
        for j in range(i,i+m):
            comparisons+=1
            if pattern[j-i] != text[j]:
                break
            if j == i+m-1:
                occurs = True
                location = i
        if occurs == True:
            break
        else:
            i+=1
    t = (time.time()-init_time) * 10**6
    print("Total number of comparisons:", comparisons)
    print("Matching done in %f microseconds." % t )
    return occurs, location, comparisons, t

"""Knuth-Morris-Pratt"""
def failurefunction(pattern):
    comparisons = 0
    j = 0
    m = len(pattern)
    F =[0] * m
    for i in range(1,m):
        comparisons+=1
        if pattern[i] == pattern[j]:
            # Matched j+1  chars
            F[i] = j+1
            j+=1
        elif j > 0:
            # Use F to shift pattern
            j = F[j-1]
        else:
            F[i] = 0
    return F, comparisons

def kmp(text,pattern, alphabet, info_print=True):
    init_time = time.time()
    n = len(text)
    m = len(pattern)
    comparisons = 0
    occurs = False
    location = None
    F, comparisons = failurefunction(pattern)
    j=0
    i = 0
    # print(F)  #For Debugging Purposes
    while i < n:
        comparisons+=1
        if text[i] == pattern[j]:
            if j == m-1:
                occurs = True
                location = i-j
                break
            else:
                i+=1
                j+=1
        else:
            if j > 0:
                j = F[j-1]
            else:
                i+=1
                j = 0
    t = (time.time()-init_time)* 10**6
    if info_print:
        print("Total number of comparisons:", comparisons)
        print("Matching done in %.2f microseconds." % t )
    return occurs, location, comparisons, t

"""Boyer-Moore"""
def badcharrule(pattern,alphabet=['A','T','C','G']):
    comparisons = 0
    m = len(pattern)
    table = [[0]*len(alphabet) for i in range(0,m)]
    for i in range(1,m):
        comparisons+=1
        target = pattern[i]
        ind = alphabet.index(target)
        table[i] = table[i-1].copy()
        table[i][ind] = i
    return table, comparisons

def goodsuffixrule(pattern):
    comparisons = 0
    m=len(pattern)
    table = [0]*m
    for i in range(m-1,-1,-1):
        suffix = pattern[i:]
        o, l, c, _ = kmp(pattern, suffix, alphabet, info_print=False)
        comparisons+=c
        if o and l < i:
            table[i] = l+1
        else:
            if i is not m-1:
                table[i] = table[i+1]
    return table, comparisons

def boyer_moore(text,pattern,alphabet=['A','T','C','G']):
    init_time = time.time()
    n = len(text)
    m = len(pattern)
    comparisons = 0
    occurs = False
    location = None
    # Create tables for rules
    badchartable, c = badcharrule(pattern, alphabet)
    comparisons += c
    # print(badchartable) # For Debugging Purposes
    goodsuffixtable, c =goodsuffixrule(pattern)
    comparisons += c
    # print(goodsuffixtable) # For Debugging Purposes
    j = m-1
    i = m-1
    for s in range(0,n):
        if j == -1:
            occurs = True
            location = i+1
            break
        elif i >= n:
            break
        else:
            if text[i] != pattern[j]:
                #print("i:",i,"j:",j)  # For Debugging Purposes
                #print("text_i:", text[i], "pattern_i:", pattern[j] )  #For Debugging Purposes
                comparisons+=1
                ind = alphabet.index(text[i])
                bad = badchartable[j][ind]
                bad = j-bad
                #print("Bad: ",bad)  #For Debugging Purposes
                good = goodsuffixtable[j]
                good = j-good
                #print("Good: ",good)  #For Debugging Purposes
                 # Get the min of shifts suggested by rules to not skip anything
                shift = max(min(bad,good),1)
                #print("Shift: ",shift) #For Debugging Purposes
                i = i + shift + (m-1-j)
                j = m-1
            else:
                j-=1
                i-=1
            # print("i\':",i,"j\':",j)  #For Debugging Purposes
    t = (time.time()-init_time)* 10**6
    print("Total number of comparisons:", comparisons)
    print("Matching done in %.2f microseconds." % t )
    return occurs, location, comparisons, t

"""Rabin-Karb"""
def radix_map(alphabet):
    radixmap = dict()
    i = 0
    for item in alphabet:
        radixmap[item] = i
        i+=1
    return radixmap

def rabin_karb(text,pattern,alphabet):
    init_time = time.time()
    n = len(text)
    m = len(pattern)
    d = len(alphabet)
    comparisons = 0
    occurs = False
    location = None
    q = max(m,d)+1
    c = d**(m-1) % q
    radixmap = radix_map(alphabet)
    # Preprocessing
    fp = 0
    ft = 0
    for i in range(m):
        fp = (d*fp + radixmap.get(pattern[i])) % q
        ft = (d*ft + radixmap.get(text[i])) % q
    # Matching
    for s in range(n-m):
        comparisons+=1
        if ft == fp:
            for i in range(s,s+m):
                comparisons+=1
                if pattern[i-s] != text[i]:
                    break
                if i == s+m-1:
                    occurs = True
                    location = s
                    break
        if occurs == True:
            break
        ft = ((ft - radixmap[text[s]]*c)*d + radixmap[text[s+m]]) % q
    t = (time.time()-init_time)* 10**6
    print("Total number of comparisons:", comparisons)
    print("Matching done in %.2f microseconds." % t )
    return occurs, location, comparisons, t

def string_matcher(algo,text,pattern, alphabet):
    switcher = {
        "brute-force": bruteforce,
        "kmp": kmp,
        "boyer-moore": boyer_moore,
        "rabin-karb": rabin_karb,
    }
    func = switcher.get(algo, lambda: " ")
    return func(text,pattern,alphabet=alphabet)
    

## Main Function

text_file =  sys.argv[1]
pattern_file = sys.argv[2] 
algo = sys.argv[3]

#text_file = "hw1example.fa" # Sample File For Debugging Purposes
#pattern_file = "hw1patternT.fa" #  Sample File For Debugging Purposes

text = readfa(text_file)
pattern = readfa(pattern_file)
alphabet=list(set(text+pattern))
print("Using ", algo, "algorithm ...")
occurs, location,  comparisons, t = string_matcher(algo, text,pattern,alphabet=alphabet)
if occurs:
    print("The pattern is matched at position starting from ", location, ".")
else:
    print("Match Not Found.")