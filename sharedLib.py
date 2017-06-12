# import ast

appName  =  sys.argv[0]
cellName = sys.argv[1]
nodeName = sys.argv[2]
serverName = sys.argv[3]

def wsadminToList(inStr):
        inStr = inStr.rstrip();
        outList=[]
        if (len(inStr)>0 and inStr[0]=='[' and inStr[-1]==']'):
                tmpList = inStr[1:-1].split(" ")
        else:
                tmpList = inStr.split("\n")   #splits for Windows or Linux
        for item in tmpList:
                item = item.rstrip();         #removes any Windows "\r"
                if (len(item)>0):
                      outList.append(item)
        return outList
#endDef


def createSharedLibrary(appName,cellName,nodeName,serverName,sharedLibName,classPath):
	n1 = AdminConfig.getid('/Cell:' + cellName + '/Node:' + nodeName + '/')
	# print n1
	library = AdminConfig.getid('/Library:'+ sharedLibName + '/')
	# print library
	if library == "":
		print "not exist shared library ,creating  " + sharedLibName
		library = AdminConfig.create('Library', n1, [['name', sharedLibName], ['classPath', classPath]])
		# print library


def createLibraryRef(appName,sharedLibName,contentUri):

	deployment = AdminConfig.getid('/Deployment:' + appName + '/')
	# print deployment

	appDeploy = AdminConfig.showAttribute(deployment, 'deployedObject')
	# print appDeploy
	# classLoad1 = AdminConfig.showAttribute(appDeploy, 'classloader')
	# print classLoad1

	# return string
	modules = AdminConfig.showAttribute(appDeploy, 'modules')
	#convert to list object
	modules = wsadminToList(modules)
	# for module in modules:
	# 	print module
	# filter the target module
	modules = [module for module in modules if AdminConfig.showAttribute(module,'uri')==contentUri]
	# get class loader
	if len(modules) > 0:

		print "create shared library reference for module" + contentUri
		moduleClassLoader =  AdminConfig.showAttribute(modules[0],'classloader')
	# print AdminConfig.list('LibraryRef')

	# libObj = [lib for lib in AdminConfig.list('LibraryRef').split('\n') if lib.find(sharedLibName) == 0]

		libRef = [lib for lib in AdminConfig.list('LibraryRef').split('\n') if AdminConfig.showAttribute(lib,'libraryName')==sharedLibName]

	# print libRef

		if len(libRef) == 0:
			print "not existing , creating "
			libRef = AdminConfig.create('LibraryRef', moduleClassLoader, [['libraryName', sharedLibName]])
			print libRef
		else:
			print "library reference existed,quit"
	else:
		print "could not find module you targeted,please double check"

contentUri = "platform-0.0.1-SNAPSHOT.war"
sharedLibName = "springsharedlib"
classPath =  '/tmp/lib'

createSharedLibrary(appName,cellName,nodeName,serverName,sharedLibName,classPath)
createLibraryRef(appName,sharedLibName,contentUri)

AdminConfig.save()


# libRefNames = [libRefName for libRefName in libRef if AdminConfig.showAttribute(libRefName,'libraryName')==sharedLibName]
# for libRefName in libRef:
# 	# refId = AdminConfig.getid(libRefName)
# 	print AdminConfig.showAttribute(libRefName,'libraryName')

# if libRef == "":


#AdminNodeManagement.syncActiveNodes()