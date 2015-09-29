#!/bin/bash
. ./install-env
userexists=false
getent passwd $DAEMONUSER >/dev/null 2>&1 && userexists=true
if $userexists; then
	echo "$DAEMONUSER exists, skipping user creation..."
	echo "Changeing $PSVARPATH ownership to $DAEMONUSER"
	chown $DAEMONUSER:$DAEMONUSER $PSVARPATH
else
	adduser --home $PSVARPATH --gecos "pegcoder daemon" --disabled-password $DAEMONUSER
fi
mkdir -p $PACHPATH
mkdir -p $PSUSRPATH
mkdir -p $PWRKSPACE
mkdir -p $PSVARPATH
cp ./install-env $PSVARPATH/pegcoder-env
echo ". ./pegcoder-env" >>$PSVARPATH/.profile
cp ../libpegcoder.py $PSUSRPATH
cp ../pegcoder $INSTALLPATH
cp -Rvp ../usr/lib/pegcoder/* $PSUSRPATH
chown -R $DAEMONUSER:$DAEMONUSER $PSUSRPATH
chown -R $DAEMONUSER:$DAEMONUSER $PWRKSPACE
chown -R $DAEMONUSER:$DAEMONUSER $PSVARPATH
