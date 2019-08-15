#!../../bin/linux-x86_64/iseg

< envPaths

epicsEnvSet("PYEPICS_LIBCA", "$(EPICS_BASE)/lib/linux-x86_64/libca.so")
#epicsEnvSet("DIAGSTD_DISABLE", "YES")
#epicsEnvSet("PREFIX", "ACS_DIAG:IOC_iseg:")

dbLoadDatabase("${TOP}/dbd/iseg.dbd",0,0)
iseg_registerRecordDeviceDriver(pdbbase)

py "import iseg"
py "iseg.build()"

dbLoadRecords("$(TOP)/db/iseg.db", "P=ACS_DIAG:IOC_iseg:")

iocInit()

