#!/usr/bin/python3

"""
Word_counter.py - by M. Di Gennaro - 21/05/2017

Requirements:
python3
nltk

Remarks: coding is set to UTF-8

YOU CAN SPECIFY:
1.Words to neglect in the 'user_defined_stopwords.txt'
2.Punctuation symbols to neglect are listed in "punctuation_list"
3.The suffix of the text file to read (default is "suffix" = ".txt")
4.Read alphanumeric or alphabetic characthers only (default is "allowed_char" = alphanumeric)
"""

## PAKCAGES 
import sys
import regex as re
import os
import codecs
import nltk
from   nltk.corpus import stopwords
import time

main_dir = os.getcwd()

## STOP WORDS
default_stopwords   = set(nltk.corpus.stopwords.words('english'))
stopwords_file      = os.path.join( main_dir, 'user_defined_stopwords.txt' )
try:
  custom_stopwords  = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())
  all_stopwords     = default_stopwords | custom_stopwords
except(FileNotFoundError):
  all_stopwords     = default_stopwords
## PUNCTUATION
punctuation_list    = ['``', "''", '""', '(', ')', '.', ',', ':', ';', '-', '–', '\'s', '%']

def print_list_of_files( path, suffix ):
    """prints all files in 'path' ending in 'suffix'"""
    return ['{}'.format(item) for item in os.listdir( path ) if item.endswith(suffix) ]

def choose_valid_integer( var_name ):
    """check that the input from keyboar is an integer"""
    valid = False
    while not valid:
      N = input( '> Please specify {}: '.format(var_name) )
      try:
        val   = int(N)
        valid = True
      except ValueError:
        print('> {} must be an integer!! '.format(var_name) )
    return( N )

def print_top_results( sorted_list ):
    """print out most occourring key-word"""
    log_line     = '' 
    for index in range(1, min(int(words_to_print) + 1, len(sorted_list) )):
        tmp_word =  '"{}"'.format( sorted_list[index][0] )
        log_line += '{}{}. {:25} {:5} times\n'.format( ' '*5, index, tmp_word, sorted_list[index][1]  )
    return( log_line )
          
def words_clusters( text ):
    """find all occurrences of one word, couples and triplets of words in "text" """
    allowed_char     = '[a-zA-Z0-9]'  # alphanumeric
    #allowed_char     = '[a-zA-Z]'     # alphabetic only
    single_word      = re.compile(r'\b{}+\b'.format(allowed_char))
    single_word_list = single_word.findall( text ) 
    couples          = re.compile(r'\b{}+\s+{}+\b'.format(allowed_char, allowed_char))
    couples_list     = couples.findall( text , overlapped=True) 
    triplets         = re.compile(r'\b{}+\s+{}+\s+{}+\b'.format(allowed_char, allowed_char, allowed_char))
    triplets_list    = triplets.findall( text  , overlapped=True) 
    lists_of_words   = [single_word_list, couples_list, triplets_list]
    list_of_counts   = []
    
    for word_list in lists_of_words:
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
    return( lists_of_words, list_of_counts )

def main():
  ##
  print( '\n{}\n##{}Word_counter.py{}##\n##{}by M. Di Gennaro{}##\n{}\n'.format('#'*40,' '*10,' '*11,' '*10,' '*10, '#'*40) )
  ## Choose path to texts
  valid_path = False
  while not valid_path:
    rel_path   = input( '> Please specify folder containing text files:\n' )
    abs_path   = os.path.abspath( os.path.join( main_dir, rel_path ) )
    valid_path = True if os.path.exists( abs_path ) else print( '> "{}" does not exists, please specify a valid path\n'.format(rel_path) ) 
  ## Choose suffix
  change_suffix = 'y'
  suffix        = '.txt'
  print( '\n> Default suffix = ".txt"' )
  while change_suffix.lower() == 'y':
    print( '> The following files will be read and analyzed:\n' )
    list_of_files = print_list_of_files( abs_path, suffix )
    print( '  {}\n'.format( list_of_files ))
    change_suffix = input( '> Do you want to use anoter suffix ? (Y/n)\n' )
    if change_suffix.lower() == 'y':
           suffix = input( '> Please specify new suffix to use:\n ' )
  ## Choose number of words N to print in log_main.txt
  global words_to_print
  print( '> The program will find the N more frequent words in all files.')
  words_to_print = choose_valid_integer('N')
  ##
  now   = time.strftime("%d-%m-%Y-%H:%M")
  start = time.time()
  ## Create log file
  main_log = open( os.path.join( main_dir, 'log_main.txt' ), 'w+' )
  ##
  ## BEGIN: read file and store most common words
  single_word_dict = dict()
  couples_dict     = dict()
  triplets_dict    = dict()
  label_list       = [ 'single word'    , 'couples of words', 'triplets of words' ]
  dict_list        = [  single_word_dict,  couples_dict     ,  triplets_dict      ] 
  log_list         = [ 'log_words.txt'  , 'log_couples.txt' , 'log_triplets.txt'  ] 
  for text_name in list_of_files:
      text_file    = os.path.join( abs_path, text_name )
      all_lines    = open(text_file, 'r').readlines()
      head_line    = '\n{}\nreading file: {}\n{}'.format('='*40, text_file, '='*40)
      print( head_line )
      main_log.write( head_line )
      ## Recognizes all 1-words, 2-words and 3-words 
      all_words_lists, all_counts_lists = words_clusters( str(all_lines) )
      
      ## BEGIN: read file and store most common words
      for word_list, label, tmp_dict in zip( all_counts_lists, label_list, dict_list ):
          main_log.write( '\n{}\n{} most common {}:'.format('-'*40, words_to_print, label))
          main_log.write( '\n{} {} total {} have been read'.format( '.'*4, len(word_list), label ))
          main_log.write( '\n{}'.format(print_top_results( word_list )))
          ## Remove stopwords and punctuation
          main_log.write( '\n{} Removing all stopwords and punctuation:'.format('.'*4))
          reduced_items = [ item for item in word_list if not bool( set(item[0].split()) & set(  list(all_stopwords) + list(punctuation_list) )) ] 
          main_log.write( '\n{} {} words after neglecting stopwords and punctuation'.format( '.'*4, len(reduced_items) ))
          main_log.write( '\n{}'.format(print_top_results( reduced_items )))
          ## Initialize dictionary entry
          tmp_dict[text_name]  = reduced_items
      ## END: read file and store most common words
  
  ## BEGING: cross analysis of key-words
  print( '\n> File reading complete.\
          \n> Results have been written on "main_log.txt"\
          \n> The program will now count the occourrence of M results in all text.')
  max_words = choose_valid_integer('M')
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
      for tmp_index in range(1,int(max_words)+1):
          tot_occ, word, item = tmp_list[ tmp_index ]
          tmp_log.write( '{}{:3}."{}" appears {} times in total:\n'.format( '.'*4, tmp_index, word, tot_occ ))
          for tmp_item in item:
              tmp_log.write( '{}{:3} times in {}\n'.format( ' '*7, tmp_item[1], tmp_item[0] ))
      tmp_log.write( '\n' )
      tmp_log.close()
      print( '> Cross analysis for most occourring {} stored in "{}"'.format(label, log_name) )
  ## END:  cross analysis of key-words

  main_log.close()
  print( '\n{}\n## Total running time = {:3.3} sec.     ##'.format( '#'*40, time.time() - start))
  print( '## Thank you for using me.            ##\n{}'.format('#'*40) )


if __name__ == '__main__':
  main()
