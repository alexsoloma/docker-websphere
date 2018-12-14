#!/bin/bash

APP_NAME=$1
WAR_FILE=$2
CONTENT_URI=$3
/opt/IBM/WebSphere/AppServer/bin/wsadmin.sh -lang jython -port 8880 -username wasadmin -password wasadmin -f /tmp/updateWar.py ${APP_NAME} ${WAR_FILE} ${CONTENT_URI} maximoCell maximoNode server1