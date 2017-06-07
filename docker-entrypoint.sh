#!/bin/bash
set -e

WEBSPHERE=/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/

EAR_INST_DIR=/projects/maximo/installed/

# echo $EAR_INST_DIR

# ls $WEBSPHERE

# if [ ! -d "$WEBSPHERE" ]; then
# 	echo folder is not exist
# fi

#if [ "$1" = 'startServer' ]; then

if [ ! -d "$WEBSPHERE" ]; then
	/tmp/installer/installc -acceptLicense -showProgress input /tmp/WASv85.base.install.xml
	/opt/IBM/WebSphere/AppServer/bin/managesdk.sh -setNewProfileDefault -sdkname 1.7_64
#	/opt/IBM/WebSphere/AppServer/bin/managesdk.sh -listAvailable -verbose
    /opt/IBM/WebSphere/AppServer/bin/manageprofiles.sh -response /tmp/createprofile.txt
    rm -f /tmp/WASv85.base.install.xml \
	   && rm -r -f /tmp/was \
	   && rm -r -f /tmp/installer \
	  && rm /tmp/maximo.ear \
	  && rm -f /tmp/createprofile.txt \
	  && rm -r -f /tmp/java 
	 #&& rm /tmp/deploy.py \
fi

/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/startServer.sh server1

#fi



# if [ ! -a "$EAR_INST_DIR/MAXIMO.ear" ]; then
# 	/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/bin/startServer.sh server1
# 	/opt/IBM/WebSphere/AppServer/bin/wsadmin.sh -lang jython -port 8880 -username wasadmin -password wasadmin -f /tmp/deploy.py maximo /tmp/maximo.ear $EAR_INST_DIR maximo maximoCell maximoNode server1
# fi

#tail -f /dev/null

exec "$@"