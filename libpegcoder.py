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

def getstatus(svarpath, jfilext, jsonstatls):
	for mysvarpath, vardirs, varfile in os.walk(svarpath):
                for varfile in fnmatch.filter(varfile, jfilext):
                        jsonstatls.append(json.loads(open(os.path.join(mysvarpath, varfile)).read()))
        return jsonstatls

def getcurfiles(achpath, fileext, curfilels):
	for rootpath, dirnames, filenames in os.walk(achpath):
		for curfile in fnmatch.filter(filenames, fileext):
			pathfile = os.path.join(rootpath, curfile)
			curfilels.append(pathfile)
	return curfilels

def updtjsls(svarpath, jsonstatls, jstattemp, curfilels):
	cflag = "True"
	mytemplate = json.loads(open(jstattemp).read())
	print mytemplate
	for filename in curfilels:
		for jsonobj in jsonstatls:
			if jsonobj['file'] == filename:
                                cflag = "False"
                if cflag == "True":
			mynewjson = mytemplate
			mynewjson['file'] = filename
			mypath, myfilename = os.path.split(filename)
			newpathf = svarpath + myfilename + ".json"
			print json.dumps(mynewjson, indent=4, sort_keys=True)
			#with open(newpathf, 'w') as myoutfile:
    			#	json.dump(mynewjson, myoutfile, indent=4)
			#myoutfile.close()
                        #create json file
                cflag = "True"
			
def updtxcls(jsonls):
	fileext = os.getenv('PFILEEXT', '*.mp4')
	achpath = os.getenv('PACHPATH', '/mnt/archive-rsync/archive/')
	#with open(indpatf, 'w') as indfile
	#myjsonls = json.loads(open(jsonls).read())
	#print json.dumps(myjsonls, indent=4, sort_keys=True)
	for rootpath, dirnames, filenames in os.walk(achpath):
		for curfile in fnmatch.filter(filenames, fileext):
			xstatus = "pending"
			#print(os.path.join(rootpath, curfile))
			flpath = os.path.join(rootpath, curfile)
			mycurstr = '{"' + flpath + '": "' + xstatus + '"}'
			#print mycurstr
			mycurjson = json.loads(mycurstr)
			#print json.dumps(mycurjson, indent=4, sort_keys=True)
			#myjsonls.curfile = mycurjson
			#myjsonls.append(mycurjson)
	#print json.dumps(myjsonls, indent=4, sort_keys=True)

