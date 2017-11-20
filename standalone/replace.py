import os
import sys

def replace_string(old_filename, new_filename, old_strings, new_strings):
    if not os.path.isfile(old_filename):
        print ('Error replacing string')
        exit()

    old_file = open(old_filename, 'r')
    new_file = open(new_filename, 'w')
    
    content = old_file.read()
    old_file.close()

    for key, value in enumerate(old_strings): 
        content = content.replace(value, new_strings[key])

    new_file.write(content)
    new_file.close()
    
if __name__ == '__main__':
    if len(sys.argv) < 5:
        print "Usage: python replace.py <filename> <new_filename> <old_strings> <new_strings"
        print "Strings should be separated by a comma"
        exit()
        
    old_strings = sys.argv[3].split(',')
    new_strings = sys.argv[4].split(',')
    
    replace_string(sys.argv[1], sys.argv[2], old_strings, new_strings)