## 1.README

1.1 Word_counter.py reads any number of text files and returns the most used key-words in each text file.
1.2 A key-word can be a single word, a couple or a triplets of words.
1.3 It then check the occourrence of the most repeated words, couples and triplets in all other texts and returns the total occurrence per file.

## 2.CONTENTS
2.1 README.txt
2.2 Word_counter.py
2.3 user_defined_stopwords.txt

## 3.REQUIREMENTS
3.1 python3
3.2 nltk 

## 4.RUNNING
Download Word_counter.py to your computer
Make folder containing text files to read (can be in the same folder containing Word_counter.py)
Run with 
"$python3 Word_counter.py"
or 
"$chmod +x Word_counter.py" 
"./Word_counter.py" 
The user will be asked to specify:
4.1 The name of the folder containing the files to read (can be ".", or the absolute path, or the relative path)
4.2 The maximum number N of key-words to print in the main_log.txt file
4.3 The maximum number M of key-words to print in the log files relative to single words, couples and triplets of words.

## 5.OUTPUTS
5.1 log_main.txt
For each of the text files in the above specified folder (4.1), the N most occourrent key-words are printed before and after removing stopwords and punctuation (N specified in 4.2).
5.2 log_words.txt, log_couples.txt, log_triplets
These three files report the M most occurring key-words, reporting the total occurrency and the relative occurrency in each of the text files (M specified in 4.3). 

## 6.CUSTOMIZATION
6.1 Only files ending in '.txt' will be read. The user can modify this value in the 'suffix' variable (line 92).
6.2 All words present in the nltk.stopwords module are neglected.
    The user can specify the language in the "default_stopwords" variable (default is 'english', line 76).
    Please refer to the nltk documentation (http://www.nltk.org/). 
6.3 The user can specify any word to be neglected by adding it in a new line to the "user_defined_stopwords.txt" file
6.4 All alphanumeric characters are allowed. The user can specify to read only alphabetical character by choosing the 'allowed_char' variable in the word_cluster function.
