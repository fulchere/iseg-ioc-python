TOP=../..

include $(TOP)/configure/CONFIG
PYDEVSUP ?= /etc/epics
PY_VER ?= 2.7
include $(PYDEVSUP)/configure/CONFIG_PY

PY += iseg.py

include $(TOP)/configure/RULES
include $(PYDEVSUP)/configure/RULES_PY
