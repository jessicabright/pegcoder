#!/usr/bin/python
# Jessica Bright jbright@cctv.org made by a kitty on a pts
#########
#modules#
#########
import json, subprocess, shlex
###########
#functions#
###########
def encode(encodejson):
	myjson = json.loads(open(encodejson).read())
	encodecmd = "ffmpeg"
	#setup the inputfile first...
	encodecmd = encodecmd + " -i " + myjson['workspace'] + myjson['infilename']
	#now let's setup the bulk of our options, may have to think about how I'm pulling this in more later...
	optlib = json.loads(open("/home/ubuntu/gitroot/snakes/optlibs/opt_" + myjson['encoder'] + ".json").read())
	for opt in optlib:
		encodecmd = encodecmd + " " + optlib[opt] + " " + myjson[opt]
	#the scale option is ugly, so I'll add it here
	encodecmd = encodecmd + " -vf scale=" + myjson['scale']
	#finally our output target
	encodecmd = encodecmd + " " + myjson['workspace'] + myjson['outfilename']
	#let's use the shlex module to clean things up for a non-shell subprocess
	#print encodecmd  #make this a proper debug, info level?
	subprocess.check_call(shlex.split(encodecmd))

def fetchin(myjson):
	print myjson['srcspace']
	print "Let's fetch some stuff based on some other stuff, but fakeing it for now"
