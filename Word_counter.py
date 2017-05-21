#!/usr/bin/python3

## Word_counter.py 
## by M. Di Gennaro - 21/05/2017

## Requirements:
## python3
## nltk

## Remarks
## coding=UTF-8

## YOU MIGHT WANT TO SPECIFY:
## 1.User defined words to neglect in the './user_defined_stopwords.txt'
## 2.You might want to specify the suffix of the text file to read,
##   Here is set to ".txt"

## PAKCAGES 
import sys
import regex as re
import os
import codecs
import nltk
from   nltk.corpus import stopwords
import time

now      = time.strftime("%d-%m-%Y-%H:%M")
start    = time.time()
main_dir = os.getcwd()

def choose_valid_integer():
  valid = False
  while not valid:
    N = input( '> Please specify integer: ' )
    try:
      val   = int(N)
      valid = True
    except ValueError:
      print('> N must be an integer!! ' )
  return( N )

def print_top_results( sorted_list ):
    log_line     = '' 
    for index in range(1, min(int(words_to_print) + 1, len(sorted_list) )):
        tmp_word =  '"{}"'.format( sorted_list[index][0] )
        log_line += '{}{}. {:25} {:5} times\n'.format( ' '*5, index, tmp_word, sorted_list[index][1]  )
    return( log_line )
          
def words_clusters( text ):
    allowed_char     = '[a-zA-Z0-9]'  # alphanumeric
    #allowed_char     = '[a-zA-Z]'     # alphabetic only
    one_word         = re.compile(r'\b{}+\b'.format(allowed_char))
    one_word_list    = one_word.findall( text ) 
    two_words        = re.compile(r'\b{}+\s+{}+\b'.format(allowed_char, allowed_char))
    two_words_list   = two_words.findall( text , overlapped=True) 
    three_words      = re.compile(r'\b{}+\s+{}+\s+{}+\b'.format(allowed_char, allowed_char, allowed_char))
    three_words_list = three_words.findall( text  , overlapped=True) 
    list_of_w_lists  = [one_word_list, two_words_list, three_words_list]
    list_of_counts   = []
    
    for word_list in list_of_w_lists:
        tmp_list = []
        for word in word_list:
            lower_word = word.lower()
            if lower_word in [ item[0] for item in tmp_list ]:
               for item in tmp_list:
                   if item[0]==lower_word:
                      item[1] += 1
            else:
               tmp_list.append( [lower_word, 1] )
        sorted_list = sorted( tmp_list, key=lambda x: x[1] , reverse=True)
        list_of_counts.append( sorted_list )
    return( list_of_w_lists, list_of_counts )

## STOP WORDS
default_stopwords = set(nltk.corpus.stopwords.words('english'))
stopwords_file    = os.path.join( main_dir, 'user_defined_stopwords.txt' )
try:
  custom_stopwords  = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())
  all_stopwords     = default_stopwords | custom_stopwords
except(FileNotFoundError):
  all_stopwords     = default_stopwords
# introduce here any character/word to neglect
punctuation   = ['``', "''", '""', '(', ')', '.', ',', ':', ';', '-', '–', '\'s', '%']

def main():
  print( '\n{}\n##{}Word_counter.py{}##\n##{}by M. Di Gennaro{}##\n{}\n'.format('#'*40,' '*10,' '*11,' '*10,' '*10, '#'*40) )
  ## Choose here
  ##   1. path of texts to read
  ##   2. default suffix
  ##   3. number of words to return
  suffix     = '.txt'
  valid_path = False
  while not valid_path:
    rel_path = input( '> Please specify folder containing text files: ' )
    abs_path = os.path.join( main_dir, rel_path )
    if os.path.exists( abs_path ):
      list_of_files = ['{}'.format(item) for item in os.listdir( abs_path ) if item.endswith(suffix) ]
      print( '> Reading files in {}\n'.format( abs_path ) )
      print( '> The following files will be read and analyzed:\n> {}'.format( list_of_files ) )
      proceed = input('> Proceed ? (Y/n)')
      if proceed == 'Y':
        valid_path = True
    else: 
      print( '> "{}" does not exists, please specify a valid path'.format(rel_path) ) 
  
  global words_to_print
  print( '> The program will find the N more frequent words in all files.')
  words_to_print = choose_valid_integer()
  ## Create log file
  main_log  = open( os.path.join( main_dir, 'log_main.txt' ), 'w+' )

  ## BEGIN: read file and store most common words
  one_word_dict     = dict()
  two_words_dict    = dict()
  three_words_dict  = dict()
  label_list  = [ 'single word', 'couples of words', 'triplets of words' ]
  dict_list   = [ one_word_dict, two_words_dict, three_words_dict ] 
  log_list    = [ 'log_words.txt', 'log_couples.txt', 'log_triplets.txt' ] 
  for text_name in list_of_files:
      text_file = os.path.join( abs_path, text_name )
      all_lines = open(text_file, 'r').readlines()
      head_line = '\n{}\nreading file: {}\n{}'.format('='*40, text_file, '='*40)
      print( head_line )
      main_log.write( head_line )
      ## Recognizes all 1-words, 2-words and 3-words 
      all_words_lists, all_counts_lists = words_clusters( str(all_lines) )
      
      ## BEGIN: read file and store most common words
      for word_list, label, tmp_dict in zip( all_counts_lists, label_list, dict_list ):
          main_log.write( '\n{}\n{} most common {}:'.format('-'*40, words_to_print, label))
          main_log.write( '\n{} {} total {} have been read'.format( '.'*4, len(word_list), label ))
          main_log.write( '\n{}'.format(print_top_results( word_list )))
          # Remove stopwords and punctuation
          main_log.write( '\n{} Removing all stopwords and punctuation:'.format('.'*4))
          reduced_items = [ item for item in word_list if not bool( set(item[0].split()) & set(  list(all_stopwords) + list(punctuation) )) ] 
          main_log.write( '\n{} {} words after neglecting stopwords and punctuation'.format( '.'*4, len(reduced_items) ))
          main_log.write( '\n{}'.format(print_top_results( reduced_items )))
          ## Initialize dictionary entry
          tmp_dict[text_name]  = reduced_items
      ## END: read file and store most common words
  
  ## BEGING: cross analysis of all top words in all text files
  ## fix one element in "most_common_words" dictionary 
  ## and loop over all the other elements (with no repetition)
  print( '\n> File reading complete.')
  print( '> Results have been written on "main_log.txt"' )
  print( '> The program will now count the occourrence of M results in all text.')
  max_words = choose_valid_integer()
  for dictionary, label, log_name in zip( dict_list, label_list, log_list ): 
      tmp_dict = dict()
      tmp_log  = open( os.path.join( main_dir, log_name ) , 'w+') 
      for text_source, word_list in dictionary.items():
          list_of_words = [ item[0] for item in word_list ]
          list_of_freqs = [ item[1] for item in word_list ]
          for (word, freq) in zip( list_of_words, list_of_freqs ):
              if word in tmp_dict.keys():
                 tmp_dict[ word ].append((text_source, freq))
              else:
                 tmp_dict[ word ] = [(text_source, freq)]
      tmp_log.write( '{}\nMost common {} (in all documets):\n{}\n'.format('='*40, label, '='*40) )
      tmp_list = []
      for (key, elem) in tmp_dict.items():
          tot_occ = sum([ item[1] for item in elem ]) 
          tmp_list.append( [tot_occ, key, elem] )
      tmp_list.sort( key = lambda x: x[0], reverse=True )
      for tmp_index in range(1,int(max_words)):
          tot_occ, word, item = tmp_list[ tmp_index ]
          tmp_log.write( '{}{:3}."{}" appears {} times in total:\n'.format( '.'*3, tmp_index, word, tot_occ ))
          for tmp_item in item:
              tmp_log.write( '{}{} times in {}\n'.format( ' '*10, tmp_item[1], tmp_item[0] ))
      tmp_log.write( '\n' )
      tmp_log.close()
      print( '> Cross analysis for most occourring {} stored in "{}"'.format(label, log_name) )
  ### END: cross analysis of all top words in all text files

  main_log.close()
  print( '\n{}\n## Total running time = {:3.3} sec.     ##'.format( '#'*40, time.time() - start))
  print( '## Thank you for using me.            ##\n{}'.format('#'*40) )


if __name__ == '__main__':
  main()
