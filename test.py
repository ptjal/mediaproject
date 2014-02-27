#!python

import sys
from tmdb_meta import *
import mp4tag
import media_path

if __name__ == '__main__':
    import pprint
    media_file = sys.argv[1]

    sname = media_path.get_search_name(media_file)
    print '-' * 70
    print 'Searching for: %s' % sname
    
    print 'Found:'
    rslts = tmdb_search(sname)
    show_search_result(rslts)

    meta = tmdb_get_meta(rslts[0].get_id())

    mp4tag.apply_tags(media_file, meta)

