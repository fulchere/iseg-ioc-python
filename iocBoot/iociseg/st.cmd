#!../../bin/linux-x86_64/iseg

## You may have to change iseg to something else
## everywhere it appears in this file

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/iseg.dbd"
iseg_registerRecordDeviceDriver pdbbase

## Load record instances
dbLoadTemplate "db/user.substitutions"
dbLoadRecords "db/dbSubExample.db", "user=fulcher"
dbLoadRecords "db/iseg.db", "user=fulcher,P=ACS_DIAG:IOC_iseg:"

## Set this to see messages from mySub
#var mySubDebug 1

## Run this to trace the stages of iocInit
#traceIocInit

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncExample, "user=fulcher"
