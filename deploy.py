import time
import string

appName = sys.argv[0]
earFile = sys.argv[1]
installDir = sys.argv[2]
appName = sys.argv[3]
cellName = sys.argv[4]
nodeName = sys.argv[5]
serverName = sys.argv[6]


installAppMaximo(appName, earFile, cellName, nodeName, serverName, installDir)

# wsadmin -f test.py appName earFile installDir appName cellName nodeName serverName
# earFile = '/tmp/'
# appName = 'MAXIMO'
# nodeName = 'maximoNode'
# cellName = 'maximoCell'
# serverName = 'server1'
# installDir = ''

## Example 11 Install application with various task and non task options ##


def installAppMaximo(appName, earFile, cellName, nodeName, serverName, installDir, failonerror=AdminUtilities._BLANK_):
    try:
        AdminApp.install(earFile, '[-node ' + nodeName
                         + ' -cell ' + cellName
                         + ' -server ' + serverName
                         + ' -installed.ear.destination ' + installDir
                         + ' -defaultbinding.virtual.host default_host -usedefaultbindings]')

        AdminConfig.save()

        result = AdminApp.isAppReady(appName)
        while (result == "false"):
            # Wait 5 seconds before checking again
            time.sleep(5)
            print AdminApp.getDeployStatus(appName)
            result = AdminApp.isAppReady(appName)
        print("Starting application...")

        appManager = AdminControl.queryNames(
            'cell=' + cellName + ',node=' + nodeName + ',type=' + 'ApplicationManager,process=' + serverName + ',*')
        print appManager

        AdminControl.invoke(appManager, 'startApplication', appName)

        print("Started")
    except:
            # typ, val, tb = sys.exc_info()
            # if (typ==SystemExit):  raise SystemExit,`val`
            # if (failonerror != "true"):
            #    print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
            #    val = "%s %s" % (sys.exc_type, sys.exc_value)
            #    raise "ScriptLibraryException: ", `val`
            #    return -1
            # else:
            #    return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
            # #endIf

        # endTry
    return 1  # succeed
# endDef

# nodeName = '02b3d5e9eef6Node01'
# cellName = '02b3d5e9eef6Node01Cell'


# AdminApp.install( appLocation + string.lower(appName) + '.ear','[-node ' + nodeName
# 	+ ' -cell ' + cellName
# 	+ ' -server ' + serverName
# 	+ ' -installed.ear.destination ' + installDir
# 	+ ' -defaultbinding.virtual.host default_host -usedefaultbindings]')

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
