import time
import string


## Example 11 Install application with various task and non task options ##
def installAppMaximo(appName, earFile, cellName,nodeName, serverName,installDir, failonerror=AdminUtilities._BLANK_ ):
    print("Starting installAppMaximo...")
    try:
        AdminApp.install(earFile ,'[-node ' + nodeName 
        	+ ' -appname ' + appName
        	+ ' -contextroot ' + appName
            + ' -cell ' + cellName 
            + ' -server ' + serverName 
            + ' -installed.ear.destination ' + installDir
            + ' -defaultbinding.virtual.host default_host -usedefaultbindings]')

        AdminConfig.save()

        result = AdminApp.isAppReady(appName)
        while (result == "false"):
           ### Wait 5 seconds before checking again
           time.sleep(5)
           print AdminApp.getDeployStatus(appName)
           result = AdminApp.isAppReady(appName)
        print("Starting application...")


        appManager = AdminControl.queryNames('cell=' + cellName + ',node=' + nodeName + ',type=' + 'ApplicationManager,process=' + serverName + ',*')
        print appManager

        AdminControl.invoke(appManager, 'startApplication', appName)

        print("Started")
    except:
        print("exception exit 0...")
        return 0
    #endTry
    return 1  
    # succeed
#endDef


def getAppStatus(appName):
    # If objectName is blank, then the application is not running.
    objectName = AdminControl.completeObjectName('type=Application,name=' + appName + ',*')
    if objectName == "":
        appStatus = 'Stopped'
    else:
        appStatus = 'Running'
    return appStatus


appName  =  sys.argv[0]
earFile  =  sys.argv[1]
installDir = sys.argv[2]
appName = sys.argv[3]
cellName = sys.argv[4]
nodeName = sys.argv[5]
serverName = sys.argv[6]


installed = installAppMaximo(appName, earFile, cellName,nodeName, serverName,installDir)
# installAppMaximo(appName, earFile, cellName,nodeName, serverName,installDir)

if installed == 0:
    AdminApp.update(appName, 'app', '[-operation update -contents ' + earFile + ' -usedefaultbindings -nodeployejb -BindJndiForEJBNonMessageBinding [["Incremen EJB module" Increment Increment.jar,META-INF/ejb-jar.xml Inc]]]')
    AdminConfig.save()
    result = AdminApp.isAppReady(appName)
    while (result == "false"):
       ### Wait 5 seconds before checking again
       time.sleep(5)
       print AdminApp.getDeployStatus(appName)
       result = AdminApp.isAppReady(appName)
    print("Starting application...")

    appStatus = getAppStatus(appName)
    if appStatus=='Stopped':
      appManager = AdminControl.queryNames('cell=' + cellName + ',node=' + nodeName + ',type=' + 'ApplicationManager,process=' + serverName + ',*')
      print appManager

      AdminControl.invoke(appManager, 'startApplication', appName)
      print("Started")
    else:
      print("Already Started!")  

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