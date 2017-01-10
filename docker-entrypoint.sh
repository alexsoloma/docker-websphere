#!/bin/bash
set -e

WEBSPHERE=/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/

EAR_INST_DIR=/projects/maximo/installed/

#if [ "$1" = 'startServer' ]; then

if [ ! -a "$WEBSPHERE" ]; then
	/tmp/installer/installc -acceptLicense -showProgress input /tmp/WASv85.base.install.xml
    /opt/IBM/WebSphere/AppServer/bin/manageprofiles.sh -response /tmp/createprofile.txt
fi

    # exec /opt/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/startServer.sh server1
#fi



if [ ! -a "$EAR_INST_DIR/MAXIMO.ear" ]; then
	/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/startServer.sh server1
	/opt/IBM/WebSphere/AppServer/bin/wsadmin.sh -lang jython -port 8880 -username wasadmin -password wasadmin -f /tmp/deploy.py MAXIMO /tmp/MAXIMO.ear $EAR_INST_DIR maximoCell maximoNode server1
fi

#tail -f /dev/null

exec "$@"