#!python

import sys
import re
import os.path

def get_search_name(filename):

    # strip directory
    sname = os.path.basename(filename)
    # strip extension
    sname = os.path.splitext(sname)[0]
    # replace underscores
    sname = sname.replace("_", " ")

    sname = re.sub(r'((?<=[a-z])[A-Z]|'\
		     '(?<=[0-9])[A-Za-z]|'\
		     '(?<=[A-Za-z])[0-9]|'\
		     '(?<![\A\s])[A-Z](?=[a-z]))', r' \1', sname)

    return sname.strip()

if __name__ == '__main__':
    filename = sys.argv[1]
    search_name = get_search_name(filename)
    print '%s yields %s' % (filename, search_name)
