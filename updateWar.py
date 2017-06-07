import time
import string

appName  =  sys.argv[0]
warFile  =  sys.argv[1]
contentUri = sys.argv[2]
cellName = sys.argv[3]
nodeName = sys.argv[4]
serverName = sys.argv[5]

def getAppStatus(appName):
    # If objectName is blank, then the application is not running.
    objectName = AdminControl.completeObjectName('type=Application,name=' + appName + ',*')
    if objectName == "":
        appStatus = 'Stopped'
    else:
        appStatus = 'Running'
    return appStatus

AdminApp.update(appName, 'modulefile', '[-operation addupdate -contents ' + warFile + ' -contenturi ' + contentUri + ']')
AdminConfig.save()
result = AdminApp.isAppReady(appName)
while (result == "false"):
   ### Wait 5 seconds before checking again
   time.sleep(5)
   print AdminApp.getDeployStatus(appName)
   result = AdminApp.isAppReady(appName)
print("Starting application...")

appStatus = getAppStatus(appName)
appManager = AdminControl.queryNames('cell=' + cellName + ',node=' + nodeName + ',type=' + 'ApplicationManager,process=' + serverName + ',*')

if appStatus=='Stopped':
  print appManager

  AdminControl.invoke(appManager, 'startApplication', appName)
  print("Started")
else:
  print("Already Started!")
  print("Stopping app")
  AdminControl.invoke(appManager, 'stopApplication', appName)
  print("restarting app")
  AdminControl.invoke(appManager, 'startApplication', appName)

# wsadmin -f test.py appName earFile installDir appName cellName nodeName serverName
# earFile = '/tmp/'
# appName = 'MAXIMO'
# nodeName = 'maximoNode'
# cellName = 'maximoCell'
# serverName = 'server1'
# installDir = ''


# nodeName = '02b3d5e9eef6Node01'
# cellName = '02b3d5e9eef6Node01Cell'


# AdminApp.install( appLocation + string.lower(appName) + '.ear','[-node ' + nodeName 
#     + ' -cell ' + cellName 
#     + ' -server ' + serverName 
#     + ' -installed.ear.destination ' + installDir
#     + ' -defaultbinding.virtual.host default_host -usedefaultbindings]')

# AdminConfig.save()

# result = AdminApp.isAppReady(appName)
# while (result == "false"):
#    ### Wait 5 seconds before checking again
#    time.sleep(5)
#    print AdminApp.getDeployStatus(appName)
#    result = AdminApp.isAppReady(appName)
# print("Starting application...")


# appManager = AdminControl.queryNames('cell=' + cellName + ',node=' + nodeName + ',type=' + 'ApplicationManager,process=' + serverName + ',*')
# print appManager

# AdminControl.invoke(appManager, 'startApplication', appName)

# print("Started")