#!/usr/bin/python
# Jessica Bright jbright@cctv.org made by a kitty on a pts
#########
#modules#
#########
import os, sys, io, subprocess, json, shlex, fnmatch
###########
#functions#
###########
def encode(settings, encodefile, infilename):
	outfilename = os.path.basename(infilename)
	#Setup the command
	encodejsonpathd = settings['susrpath'] + "encoders/" + encodefile
	myjson = json.loads(open(encodejsonpathd).read())
	encodecmd = settings['encodecmd'] + " -i " + infilename
	optlib = json.loads(open(settings['susrpath'] + "optlibs/" + myjson['encoder'] + ".json").read())
	for opt in optlib:
		encodecmd = encodecmd + " " + optlib[opt] + " " + myjson[opt]
	#The scale option is ugly, so we'll add it here
	encodecmd = encodecmd + " -vf scale=" + myjson['scale']
	encodecmd = encodecmd + " " + settings['workspace'] + outfilename
	#print encodecmd  #make this a proper debug,  or log level info?
	#Run it here, while cleaning things up with shlex first
	subprocess.check_call(shlex.split(encodecmd))
	#check on status of ffmpeg or file or mediainfo and return something like 'encoded'?
	#return (something)

#get status from exsisting status json
def getstatus(settings, jsonstatls):
	for mysvarpath, vardirs, varfile in os.walk(settings['svarpath']):
                for varfile in fnmatch.filter(varfile, settings['jfilext']):
                        jsonstatls.append(json.loads(open(os.path.join(mysvarpath, varfile)).read()))
        return jsonstatls

#get list of all current mp4 files
def getcurfiles(settings, curfilels):
	for rootpath, dirnames, filenames in os.walk(settings['achpath']):
		for curfile in fnmatch.filter(filenames, settings['fileext']):
			pathfile = os.path.join(rootpath, curfile)
			curfilels.append(pathfile)
	return curfilels

#update status json files
def updtjsls(settings, jsonstatls, curfilels):
	cflag = "True"
	mytemplate = json.loads(open(settings['susrpath'] + "templates/status-template.json").read())
	for filename in curfilels:
		for jsonobj in jsonstatls:
			if jsonobj['file'] == filename:
				cflag = "False"
		if cflag == "True":
			mynewjson = mytemplate
			mynewjson['file'] = filename
			mypath, myfilename = os.path.split(filename)
			newpathf = settings['svarpath'] + myfilename + ".json"
			with open(newpathf, 'w') as myoutfile:
				json.dump(mynewjson, myoutfile)
		cflag = "True"

#encode files based on orginizational settings using jsonstatls
def chkupencode(settings, jsonstatls, org):
	for jsonobj in jsonstatls:
		infilename = jsonobj['file']
		if jsonobj['status-playback'] == "pending":
			infilename = jsonobj['file']
			encodefile = org + ".pb." + jsonobj['encoder-playback'] + ".json"
			encode(settings, encodefile, infilename)
		if jsonobj['status-vod'] == "pending":
			outfilename = org + ".vod." + jsonobj['file']
			encodefile = org + ".vod." + jsonobj['encoder-vod'] + ".json"
			encode(settings, encodefile, infilename)
