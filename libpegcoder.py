#!/usr/bin/python
# Jessica Bright jbright@cctv.org made by a kitty on a pts
#########
#modules#
#########
import os, subprocess, json, shlex
from sys import argv
###########
#functions#
###########
def encode(encodejson):
	#Setup our enviorment
	optlibdir = os.getenv('POPTLIBDIR', '/usr/lib/pegcoder/optlibs/')
	encodecmd = os.getenv('PENCODECMD', 'ffmpeg')
	srcspace = os.getenv('PSRCSPACE', '~/media/')
	workspace = os.getenv('PWRKSPACE', '/tmp/')
	outfilename = argv.pop()
	infilename = argv.pop()
	#Setup the command
	myjson = json.loads(open(encodejson).read())
	encodecmd = encodecmd + " -i " + workspace + infilename
	optlib = json.loads(open(optlibdir + myjson['encoder'] + ".json").read())
	for opt in optlib:
		encodecmd = encodecmd + " " + optlib[opt] + " " + myjson[opt]
	#The scale option is ugly, so we'll add it here
	encodecmd = encodecmd + " -vf scale=" + myjson['scale']
	encodecmd = encodecmd + " " + workspace + outfilename
	#print encodecmd  #make this a proper debug, info level?
	#Run it here, cleaning things up with shlex
	subprocess.check_call(shlex.split(encodecmd))
