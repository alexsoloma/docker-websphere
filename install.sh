#!/bin/bash

APP_NAME=$1
EAR_FILE=$2
EAR_INST_DIR=$3
/opt/IBM/WebSphere/AppServer/bin/wsadmin.sh -lang jython -port 8880 -username wasadmin -password wasadmin -f /tmp/deploy.py ${APP_NAME} ${EAR_FILE} ${EAR_INST_DIR} ${APP_NAME} maximoCell maximoNode server1

/opt/IBM/WebSphere/AppServer/bin/wsadmin.sh -lang jython -port 8880 -username wasadmin -password wasadmin -f /tmp/sharedLib.py ${APP_NAME} maximoCell maximoNode server1