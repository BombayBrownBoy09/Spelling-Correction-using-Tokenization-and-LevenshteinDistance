#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
import numpy as np
from collections import defaultdict, deque
import string

with open("word_list.txt") as f:
    d = f.readlines()
dictionary = {}
for i in range(len(d)):
    phrase = d[i].strip()
    if phrase == "te" or phrase == "f":
        continue
    dictionary[phrase] = i

def compute_lev(w1, w2):
    """
    w1 and w2 are both strings
    
    returns an integer for distance
    """
    N = len(w1)
    M = len(w2)
    matrix = np.array([[0 for j in range(M+1)] for i in range(N+1)])    
    for i in range(N+1):
        matrix[i][0] = i
    for j in range(M+1):
        matrix[0][j] = j
    for i in range(1, N+1):
        for j in range(1, M+1):
            case_1 = matrix[i][j-1] + 1
            case_2 = matrix[i-1][j] + 1
            case_3 = matrix[i-1][j-1] 
            if w1[i-1] != w2[j-1]:
                case_3 += 1
            matrix[i][j] = min(case_1, case_2, case_3)
    return matrix[-1][-1]

def find_replacement(word, dictionary, k):
    """
    word is a string
    dictionary maps a phrase to frequency index
    k is a number up to which to replace
    
    returns a word to replace
    """
    
    if word in dictionary:
        return word
    data = defaultdict(list)
    global_replacement = word
    global_frequency = 2**32
    for phrase, frequency in dictionary.items():
        distance = compute_lev(word, phrase)
        data[distance].append((phrase, frequency))
    for i in range(1, k+1):
        current_set = data[i]
        for phrase, frequency in current_set:
            if frequency < global_frequency:
                global_replacement = phrase
                global_frequency = frequency
        if global_replacement != word:
            break
    return global_replacement

def tokenize(text):
    """
    text is a string
    
    returns:
        tokens : array of words to be spellchecked
        punctuation : array of letters to be appended to the corresponding word in tokens
        capitalization : array of indices of char to be capitalized
        isalpha : array of true or false indicating if the word should be spellchecked
    """
    
    #tokenize
    words = text.split(" ")
    tokens = []
    lpunctuation = [] #check if followed by punctuation on the left
    rpunctuation = [] #check if followed by punctuation on the right
    capitalization = [] #check if prefixed by capitalization
    isalpha = [] #if not alphanumeric, we don't check
    
    process_queue = deque([])
    process_queue.append(words.pop(0))
    
    
    while len(process_queue) >= 1 and len(words) >= 1:
        word = process_queue.popleft()
        #Check for empty word
        if len(word) < 1:
            if len(process_queue) < 1 and len(words) >= 1:
                process_queue.append(words.pop(0))
            continue
        #Check if newline is in the word and process it seperately
        if "\n" in word and len(word) > 1:
            split_word = word.split("\n")
            for index, split in enumerate(split_word):
                process_queue.append(split)
                if index != len(split_word) - 1:
                    process_queue.append("\n")
            continue
            
        #Check for punctuation
        lpunc = ""
        rpunc = ""
        while len(word) > 1 and word[0] in string.punctuation:
            lpunc += word[0]
            word = word[1:]
        while len(word) > 1 and word[-1] in string.punctuation:
            rpunc = word[-1] + rpunc
            word = word[:-1]
        lpunctuation.append(lpunc)
        rpunctuation.append(rpunc)
        
        #Check for alphanumeric
        if not word.isalpha():
            tokens.append(word)
            isalpha.append(False)
            capitalization.append([])
            if len(process_queue) < 1 and len(words) >= 1:
                process_queue.append(words.pop(0))
            continue
        else:
            isalpha.append(True)
            
        #Check for capitalization
        capitalization_indices = []
        lowercase = word.lower()
        if word == lowercase:
            capitalization.append([])
        else:
            n = len(word)
            for i in range(n):
                if word[i] != lowercase[i]:
                    capitalization_indices.append(i)
            capitalization.append(capitalization_indices)
        #Add words to array
        tokens.append(lowercase)
        if len(process_queue) < 1 and len(words) > 1:
                process_queue.append(words.pop(0))
    return tokens, lpunctuation, rpunctuation, capitalization, isalpha

def spellcheck(data):
    """
    data is a tuple containing the following:
        dictionary is a mapping of correct words to valid 
        token is a string of a word
        lpunc is the punctuation at the beginning of a phrase
        rpunc is the punctuation at the end of a phrase
        cap is the indices of capitalization
        isalpha is a bool for whether or not we ought to check.
    
    returns a corrected string with proper punctuation and capitalization
    """
    token, lpunc, rpunc, cap, isalpha, k = data
    if not isalpha:
        return lpunc + token + rpunc
    
    replacement = find_replacement(token, dictionary, k)
    for index in cap:
        if index > len(replacement) - 1:
            continue
        replacement = replacement[:index] + replacement[index].upper() + replacement[index+1:]
    return lpunc + replacement + rpunc


def check(text):
    """spellcheck without parallelism
    text is a string
    returns the corrected string
    """
    
    print("Beginning Tokenization\n")
    tokens, lpunctuation, rpunctuation, capitalization, isalpha = tokenize(text)
    ks = []
    for i in range(len(tokens)):
        ks.append(max(1, len(tokens[i])//3))
    print("Beginning Spell Check\n")
    data = list(zip(tokens, lpunctuation, rpunctuation, capitalization, isalpha, ks))
    checked_data = []
    for tup in data:
        checked = spellcheck(tup)
        checked_data.append(checked)
    print("Beginning Reconstruction\n")
    return " ".join(checked_data)

            
if __name__ == "__main__":
    

    f = open("austen-sense-corrupted.txt")
    error_text = f.read()
    
    #Single Threaded, Very Slow ~8 hour runtime
    """
    checked = check(error_text)
    with open("error_checked.txt", "wt") as f:
        f.write(checked)
    f.close()
    """
    
    #Multi Threaded, ~3 hours
    splits = error_text.split(" ")
    subset_1 = " ".join(splits[:27180])
    subset_2 = " ".join(splits[27180:54360])
    subset_3 = " ".join(splits[54360:81540])
    subset_4 = " ".join(splits[81540:])
    split_text = [subset_1,subset_2,subset_3,subset_4]
    
    with multiprocessing.Pool(4) as p:
        corrected_text = p.map(check, split_text)
    checked = " ".join(corrected_text)
    
    with open("error_checked_parallel.txt", "wt") as f:
        f.write(checked)
    f.close()
    
    
    
    
