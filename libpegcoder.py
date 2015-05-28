#!/usr/bin/python
# Jessica Bright jbright@cctv.org made by a kitty on a pts
#########
#modules#
#########
import os, sys, io, subprocess, json, shlex, fnmatch
###########
#functions#
###########
def encode(encodejson, encodecmd, infilename, susrpath, org, workspace):
	outfilename = os.path.basename(infilename)
	#infilename = argv.pop()
	#Setup the command
	encodejsonpathd = susrpath + "encoders/" + encodejson
	myjson = json.loads(open(encodejsonpathd).read())
	encodecmd = encodecmd + " -i " + infilename
	optlib = json.loads(open(susrpath + "optlibs/" + myjson['encoder'] + ".json").read())
	for opt in optlib:
		encodecmd = encodecmd + " " + optlib[opt] + " " + myjson[opt]
	#The scale option is ugly, so we'll add it here
	encodecmd = encodecmd + " -vf scale=" + myjson['scale']
	encodecmd = encodecmd + " " + workspace + outfilename
	print encodecmd  #make this a proper debug,  or log level info?
	#Run it here, while cleaning things up with shlex first
	#subprocess.check_call(shlex.split(encodecmd))
	#return (something)

#get status from exsisting status json
def getstatus(svarpath, jfilext, jsonstatls):
	for mysvarpath, vardirs, varfile in os.walk(svarpath):
                for varfile in fnmatch.filter(varfile, jfilext):
                        jsonstatls.append(json.loads(open(os.path.join(mysvarpath, varfile)).read()))
        return jsonstatls

#get list of all current mp4 files
def getcurfiles(achpath, fileext, curfilels):
	for rootpath, dirnames, filenames in os.walk(achpath):
		for curfile in fnmatch.filter(filenames, fileext):
			pathfile = os.path.join(rootpath, curfile)
			curfilels.append(pathfile)
	return curfilels

#update status json files
def updtjsls(svarpath, jsonstatls, jstattemp, curfilels):
	cflag = "True"
	mytemplate = json.loads(open(jstattemp).read())
	for filename in curfilels:
		for jsonobj in jsonstatls:
			if jsonobj['file'] == filename:
				cflag = "False"
		if cflag == "True":
			mynewjson = mytemplate
			mynewjson['file'] = filename
			mypath, myfilename = os.path.split(filename)
			newpathf = svarpath + myfilename + ".json"
			with open(newpathf, 'w') as myoutfile:
				json.dump(mynewjson, myoutfile)
		cflag = "True"
		
###Think I need to buildthe daemonish logic here at some point, keep it in this function for now...
def chkupencode(jsonstatls, encodecmd, susrpath, org, workspace):
	for jsonobj in jsonstatls:
		infilename = jsonobj['file']
		if jsonobj['status-playback'] == "pending":
			infilename = jsonobj['file']
			encodefile = org + ".pb." + jsonobj['encoder-playback'] + ".json"
			encode(encodefile, encodecmd, infilename, susrpath, org, workspace)
		elif jsonobj['status-vod'] == "pending":
			outfilename = org + ".vod." + jsonobj['file']
			print "vod pending run..."
			
			
			

