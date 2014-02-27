import mutagen
from mutagen.mp4 import *
import sys
import string
import optparse

# parse XML file and update video file w/ known tags
def apply_tags(video_file, metadata):
    modified = False

    # parse/open the video file w/ mutagen
    video = mutagen.File(video_file)

    tag_map = {
	'genre': '\xa9gen',
	'description': 'desc',
	'name': '\xa9nam',
	'title': '\xa9nam',
	'keywords': 'keyw',
	'date': '\xa9day',
	#'Genre': 'genre',
    }

    # traverse each field, matching against known tags
    for tag_name, tag_value in metadata.iteritems():
	if tag_name in tag_map:
	    tag_key = tag_map[tag_name]

	    # otherwise... handle lists
	    if ';' in tag_value:
		fields = tag_value.split(';')
		tag_value = map(string.strip, fields)

	    # update tag if different
	    if video.get(tag_key) != tag_value:
		video[tag_key] = tag_value
		modified = True

	elif tag_name == 'cover':
	    covr = []
	    if metadata.get('cover_format', 'png'):
	    	cover_fmt = MP4Cover.FORMAT_PNG
	    else:
	    	cover_fmt = MP4Cover.FORMAT_JPEG
	    covr.append(MP4Cover(tag_value, cover_fmt))
	    modified = True
	    video.tags['covr'] = covr
	elif tag_name == 'cover_file':
	    covr = []
	    cover_file = tag_value
	    data = open(cover_file, 'rb').read()
	    if cover_file.endswith('png'):
		covr.append(MP4Cover(data, MP4Cover.FORMAT_PNG))
	    else:
		covr.append(MP4Cover(data, MP4Cover.FORMAT_JPEG))

	    modified = True
	    video.tags['covr'] = covr

    # save changes (if changes made)
    if modified:
	video.save()

## MAIN
if __name__ == '__main__':

    parser = optparse.OptionParser(
	option_list = [
	    optparse.make_option("-v", "--video", help="video file",
		default=None),
	    optparse.make_option("-c", "--cover", help="cover art jpg file",
		default=None),
	])

    (options, args) = parser.parse_args()

    if not options.video:
	print 'missing required video parameter'
	sys.exit(1)

    meta = { 'genre': 'Kids', 'title': 'Shrek' }
    if options.cover:
    	meta['cover_file'] = options.cover

    apply_tags(options.video, meta)
