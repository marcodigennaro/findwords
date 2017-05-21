## README

Word_counter.py reads any number of text files and returns the most used key-words in each text file.
A key-word can be a single word, a couple or a triplets of words.
It then check the occourrence of the most repeated words, couples and triplets in all other texts and returns the total occurrence per file.

## CONTENTS
README.txt
Word_counter.py
user_defined_stopwords.txt

## REQUIREMENTS
1. python3
2. nltk 

## RUNNING
Download Word_counter.py to your computer
Make folder containing text files to read (can be in the same folder containing Word_counter.py)
python read_words.py

## CUSTOMIZATION
The user will be asked to specify:
1. The name of the folder containing the files to read (can be ".", or the absolute path, or the relative path)
2. The maximum number N of key-words to print in the main_log.txt file
3. The maximum number M of key-words to print in the log files relative to single words, couples and triplets of words.

All words present in the nltk.stopwords module are neglected
The user can specify any word to be neglected by adding it in a new line to the "user_defined_stopwords.txt" file
All alphanumeric characters are allowed. The user can specify to read only alphabetical character by choosing the 'allowed_char' variable in the word_cluster function.

## OUTPUTS
1. main_log.txt
For each of the text files in the above specified folder the most occourrent key-words are printed before and after removing stopwords and punctuation
