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
	#print settings['targettype']
	outfilename = os.path.basename(infilename)
	encodejsonpathd = settings['susrpath'] + "encoders/" + encodefile
	myjson = json.loads(open(encodejsonpathd).read())
	encodecmd = settings['encodecmd'] + " -i " + infilename
	if settings['targettype'] == "audio":
		encodecmd = encodecmd + " -vn"
	optlib = json.loads(open(settings['susrpath'] + "optlibs/" + myjson['encoder'] + ".json").read())
	for opt in optlib:
		encodecmd = encodecmd + " " + optlib[opt] + " " + myjson[opt]
	encodecmd = encodecmd + " " + settings['workspace'] + settings['targettype'] + "-" + outfilename
	#print encodecmd  #make this a proper debug,  or log level info?
	subprocess.check_call(shlex.split(encodecmd))
	#check on status of ffmpeg or file or mediainfo and return something like 'encoded'?
	#return (something)

#get status from exsisting status json
def getstatus(settings):
	jsonstatls = []
	for mysvarpath, vardirs, varfile in os.walk(settings['svarpath']):
                for varfile in fnmatch.filter(varfile, settings['jfilext']):
                        jsonstatls.append(json.loads(open(os.path.join(mysvarpath, varfile)).read()))
        return jsonstatls

#get list of all current mp4 files
def getcurfiles(settings):
	curfilels = []
	for rootpath, dirnames, filenames in os.walk(settings['achpath']):
		for curfile in fnmatch.filter(filenames, settings['fileext']):
			pathfile = os.path.join(rootpath, curfile)
			curfilels.append(pathfile)
	return curfilels

#create json files that don't exsist already
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
			mynewjson['json'] = newpathf
			with open(newpathf, 'w') as myoutfile:
				json.dump(mynewjson, myoutfile)
		cflag = "True"

#encode files based on orginizational settings using jsonstatls
def chkupencode(settings, jsonstatls):
	for jsonobj in jsonstatls:
		infilename = jsonobj['file']
		if jsonobj['status-playback'] == "pending":
			settings['targettype'] = "playback"
			encodefile = "pb." + jsonobj['encoder-playback'] + ".json"
			encode(settings, encodefile, infilename)
			jsonobj['status-playback'] = "processed"
			with open(jsonobj['json'], 'w') as myoutfile:
				json.dump(jsonobj, myoutfile)
		if jsonobj['status-vod'] == "pending":
			settings['targettype'] = "ondemand"
			encodefile = "vod." + jsonobj['encoder-vod'] + ".json"
			encode(settings, encodefile, infilename)
			jsonobj['status-vod'] = "processed"
			with open(jsonobj['json'], 'w') as myoutfile:
				json.dump(jsonobj, myoutfile)
		if jsonobj['status-audio'] == "pending":
			settings['targettype'] = "audio"
			encodefile = "vbr." + jsonobj['encoder-audio'] + ".json"
			encode(settings, encodefile, infilename)
			jsonobj['status-playback'] = "processed"
			with open(jsonobj['json'], 'w') as myoutfile:
				json.dump(jsonobj, myoutfile)
