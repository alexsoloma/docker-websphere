
cellName = sys.argv[0]
nodeName = sys.argv[1]
serverName = sys.argv[2]

varName = "DB2UNIVERSAL_JDBC_DRIVER_PATH"
newVarValue = "/tmp/SQLLIB/java"
driverName = "DB2 Universal JDBC Driver Provider"

# cellName = ""

# node = AdminConfig.getid("/Node:'+ nodeName+ '/")

def modVariable(cellName,varName,newVarValue):
    print "varName = " + varName
    cell = AdminConfig.getid("/Cell:" + cellName + "/")
    varSubstitutions = AdminConfig.list("VariableSubstitutionEntry",cell).split(java.lang.System.getProperty("line.separator"))
    print varSubstitutions
    isExisting = "NO"
    for varSubst in varSubstitutions:
            getVarName = AdminConfig.showAttribute(varSubst, "symbolicName")
            print getVarName + "=" + AdminConfig.showAttribute(varSubst, "value")
            # print "old value = " + AdminConfig.showAttribute(varSubst, "value")
            if getVarName == varName:
                print "old value = " + AdminConfig.showAttribute(varSubst, "value")
                AdminConfig.modify(varSubst,[["value", newVarValue]])
                print "new value = " + AdminConfig.showAttribute(varSubst, "value")
                isExisting = "YES"
                break
            else:
                print " not equal"

    if isExisting == "NO":
        print "not existing "
        AdminTask.setVariable('[-variableName ' + varName + ' -scope Cell=' + cellName + ']')          

providers = [ provider for provider in AdminTask.listJDBCProviders(['-scope', 'Cell=' + cellName]).split(java.lang.System.getProperty("line.separator")) if AdminConfig.showAttribute(provider,'name') == driverName ]
if len(providers) == 0:
    print "create new jdbc provider " + driverName
    AdminTask.createJDBCProvider(['-scope', 'Cell=' + cellName, '-databaseType', 'DB2', '-providerType', 'DB2 Universal JDBC Driver Provider',
        '-implementationType', 'Connection pool data source', '-name', driverName,
         '-description', 'One-phase commit DB2 JCC provider that supports JDBC 3.0. Data sources that use this provider support only 1-phase commit processing, unless you use driver type 2 with the application server for z/OS. If you use the application server for z/OS, driver type 2 uses RRS and supports 2-phase commit processing.', '-classpath',
          '${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc.jar;${UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cu.jar;${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cisuz.jar', '-nativePath', '${DB2UNIVERSAL_JDBC_DRIVER_NATIVEPATH}'])
    providers = [ provider for provider in AdminTask.listJDBCProviders(['-scope', 'Cell=' + cellName]).split(java.lang.System.getProperty("line.separator")) if AdminConfig.showAttribute(provider,'name') == driverName ]
else:
    print driverName + " exist, skip create "

print AdminTask.listJDBCProviders(['-scope', 'Cell=' + cellName])




modVariable(cellName,varName,newVarValue)

dataSourceName = "maximo"
dataSourceJdbc = "jdbc/maximo"
databaseName = "maxdbtw"
serverName = "db2"
portNumber = "50000"
authenAlias = "maximoNode/maximoDB"

uid = "db2inst1"
pwd = "passw0rd"
desc = "Maximo DB Alias"
DataBaseAccessAlias = authenAlias
secMgrID = AdminConfig.list('Security')

print secMgrID
try:
    jaasID = AdminConfig.create( 'JAASAuthData', secMgrID,  \
     [ ['alias', DataBaseAccessAlias],                  \
     ['description', desc],                             \
     ['userId', uid], ['password',pwd] ] )
    AdminConfig.save()
except:
    print DataBaseAccessAlias + " exist "

  # jdbcID = AdminConfig.getid('/ServerCluster:MyCluster/JDBCProvider:MyWasJDBCDriver
#   ds = AdminTask.createDatasource( jdbcID , '[-name testuser -jndiName jdbc/TEST -description "New wsadmin JDBC Datasource" -category "Test Jdbc" -dataStoreHelperClassName com.ibm.websphere.rsadapter.Oracle11gDataSt
# oreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias ' + DataBaseAccessAlias + '  -configureResourceProperties [[URL java.lang.String jdbc:oracle:thin:@IP:1521:dbname]]]')

# dataSources = [ ds for ds in AdminTask.listDatasources(['-scope', 'Cell=' + cellName]).split(java.lang.System.getProperty("line.separator")) if AdminConfig.showAttribute(ds,'name') == dataSourceName ]
# if len(dataSources) == 0:
#     print "create new datasource name = " + dataSourceName
try:
    AdminTask.createDatasource(providers[0], '[-name "' + dataSourceName + '" -jndiName ' + dataSourceJdbc 
        + ' -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper'
        + ' -componentManagedAuthenticationAlias ' + authenAlias #+ ' -containerManagedAlias ' + authenAlias 
        + ' -configureResourceProperties '
        + ' [[databaseName java.lang.String ' + databaseName+ '] [driverType java.lang.Integer 4] '
        + ' [serverName java.lang.String ' + serverName + ']' 
        + ' [portNumber java.lang.Integer ' + portNumber + ']]]') 
# else:
except:
    print "datasource " + dataSourceName + " exist."
# print providers
# print AdminConfig.show(providers[0])
# print AdminTask.listDatasources(['-scope', 'Cell=' + cellName])

AdminConfig.save()