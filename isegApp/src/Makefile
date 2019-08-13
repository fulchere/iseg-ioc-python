TOP=../..

include $(TOP)/configure/CONFIG
PYDEVSUP ?= /etc/epics
PY_VER ?= 2.7
include $(PYDEVSUP)/configure/CONFIG_PY

PROD_IOC = iseg
DBD += iseg.dbd

iseg_DBD += base.dbd
iseg_DBD += pyDevSup.dbd

iseg_LIBS += pyDevSup$(PY_LD_VER)

iseg_SRCS += iseg_registerRecordDeviceDriver.cpp
iseg_SRCS_DEFAULT += isegMain.cpp

iseg_LIBS += $(EPICS_BASE_IOC_LIBS)

DIAGSTD ?= /usr/lib/epics
include $(DIAGSTD)/configure/fribdiagstdMakefile
include $(TOP)/configure/RULES
include $(PYDEVSUP)/configure/RULES_PY
