#!python

import tmdb
import sys

g_tmdb = False
api_key = '0d03addfb7acd316d4e5d6f79fad5ae7'

def tmdb_init():
    global g_tmdb
    g_tmdb = True
    tmdb.configure(api_key)

def tmdb_search(sname):
    if not g_tmdb:
    	tmdb_init()
    movies = tmdb.Movies(sname)
    results = []
    for movie in movies:
    	results.append(movie)
	if len(results) >= 5:
	    break
    return results

def show_search_result(result):
    for x in xrange(len(result)):
    	r = result[x]
	print "%d - %s (%s)" % (x, r.get_title(), r.get_release_date())

def tmdb_get_meta(movie_id):
    import urllib
    if not g_tmdb:
    	tmdb_init()
    tmdb_movie = tmdb.Movie(movie_id)
    meta = {
    	'title': tmdb_movie.get_title(),
    	'date': tmdb_movie.get_release_date(),
    	'description': tmdb_movie.get_overview(),
    }

    # get poster
    p_fd = urllib.urlopen(tmdb_movie.get_poster())
    meta['cover'] = p_fd.read()
    p_fd.close()

    # get genres
    meta['genre'] = []
    tmdb_genres = tmdb_movie.get_genres()
    for gdict in tmdb_genres:
    	meta['genre'].append(gdict['name'])

    return meta

if __name__ == '__main__':
    import pprint
    search_key = sys.argv[1]
    rslts = tmdb_search(search_key)
    meta = tmdb_get_meta(rslts[0].get_id())

    pprint.pprint(meta)
