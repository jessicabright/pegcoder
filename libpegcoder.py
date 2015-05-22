#!/usr/bin/python
# Jessica Bright jbright@cctv.org made by a kitty on a pts
#########
#modules#
#########
import os, sys, subprocess, json, shlex, fnmatch
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
	#print encodecmd  #make this a proper debug,  or log level info?
	#Run it here, while cleaning things up with shlex first
	subprocess.check_call(shlex.split(encodecmd))
	#return (something)

#def xcodtgrts(xcodstatdb):
#	
#	mystat = subprocess.check_call('cat', 'xcodstatdb')

def updtxcls(jsonls):
	fileext = os.getenv('PFILEEXT', '*.mp4')
	jfilext = os.getenv('PJFILEXT', '*.json')
	achpath = os.getenv('PACHPATH', '/mnt/archive-rsync/archive/')
	varpath = os.getenv('PVARPATH', '/var/lib/pegcoder/')
	#with open(indpatf, 'w') as indfile
	myjsonls = json.loads(open(jsonls).read())
	#print json.dumps(myjsonls, indent=4, sort_keys=True)
	for varpath, vardirs, varfile in os.walk(varpath):
		for varfile in fnmatch.filter(varfile, jfilext):
			statusjson = json.loads(open(os.path.join(varpath, varfile)).read())
			print json.dumps(statusjson, indent=4, sort_keys=True)
	#how can I avoid a nested loop here?-Need to compare all to all?	
	for rootpath, dirnames, filenames in os.walk(achpath):
		for curfile in fnmatch.filter(filenames, fileext):
			xstatus = "pending"
			#print(os.path.join(rootpath, curfile))
			flpath = os.path.join(rootpath, curfile)
			mycurstr = '{"' + flpath + '": "' + xstatus + '"}'
			#print mycurstr
			mycurjson = json.loads(mycurstr)
			print json.dumps(mycurjson, indent=4, sort_keys=True)
			#myjsonls.curfile = mycurjson
			#myjsonls.append(mycurjson)
	#print json.dumps(myjsonls, indent=4, sort_keys=True)

