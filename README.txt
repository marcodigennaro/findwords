=====================
Word_counter.py
author: M. Di Gennaro
=====================

## 1.README
1.1 Word_counter.py reads a group of text files and returns the most used key-words in each text file. A key-word can be a single word, a couple or a triplets of words.
1.2 After checking the most occurring key-word in one document, Word_counter.py checks the occurrence of these expressions in all the other files.

## 2.CONTENTS
2.1 README.txt
2.2 Word_counter.py
2.3 user_defined_stopwords.txt
2.4 scripts.zip 

## 3.REQUIREMENTS
3.1 python3  (www.python.org/downloads/)
3.2 nltk     (sudo pip3 install -U nltk)

## 4.RUNNING
4.1 Download Word_counter.py to your computer
4.2 Download scripts.zip and extract files to desired destination
4.3 Run with 
    "$python3 Word_counter.py"
    or 
    "$chmod +x Word_counter.py" 
    "./Word_counter.py" 
4.4 The user will be asked to specify:
4.4.1 The name of the folder containing the files to read (can be "." if it is in the same directory as Word_counter.py, its absolute path, or its relative path)
4.4.2 The number N of key-words per text file to print in the main_log.txt file
4.4.3 The number M of key-words to print relative to key-word type (i.e. single, couple, triplets).

## 5.OUTPUTS
5.1 log_main.txt
For each text file in the above specified folder (4.4.1), the N most occurring key-words (4.4.2) are printed before and after removing stopwords and punctuation.
5.2 log_words.txt, log_couples.txt, log_triplets.txt
These three files report the M most occurring key-words, reporting the total occurrence and the relative occurrence in each of the text files (M specified in 4.4.3). 

## 6.CUSTOMIZATION
The user can specify:
6.1 Words to neglect in the 'user_defined_stopwords.txt'
The user can specify the language in the "default_stopwords" variable (default is 'english').
Please refer to the nltk documentation (http://www.nltk.org/). 
6.2 Punctuation symbols to neglect are listed in "punctuation_list"
6.3 The suffix of the text file to read (default is "suffix" = ".txt")
6.4 Read alphanumeric or alphabetic characters only (default is "allowed_char" = alphanumeric)
