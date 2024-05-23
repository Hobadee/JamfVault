VENVDIR=.venv
BINDIR=$(VENVDIR)/bin
PYTHON=$(BINDIR)/python
TESTBIN=$(BINDIR)/pytest
EXAMPLEFILE=example.py

ifeq ($(OS),Windows_NT)
	# Generic Windows settings
	CMD_DEL=del
	
	# Architecture-specific settings
    # CCFLAGS += -D WIN32
    ifeq ($(PROCESSOR_ARCHITEW6432),AMD64)
        # CCFLAGS += -D AMD64
    else
        ifeq ($(PROCESSOR_ARCHITECTURE),AMD64)
            # CCFLAGS += -D AMD64
        endif
        ifeq ($(PROCESSOR_ARCHITECTURE),x86)
            # CCFLAGS += -D IA32
        endif
    endif
else
	# Generic *NIX settings
	CMD_DEL=rm
	
	# Architecture-specific settings
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Linux)
        # CCFLAGS += -D LINUX
    endif
    ifeq ($(UNAME_S),Darwin)
        # CCFLAGS += -D OSX
    endif
    UNAME_P := $(shell uname -p)
    ifeq ($(UNAME_P),x86_64)
        # CCFLAGS += -D AMD64
    endif
    ifneq ($(filter %86,$(UNAME_P)),)
        # CCFLAGS += -D IA32
    endif
    ifneq ($(filter arm%,$(UNAME_P)),)
        # CCFLAGS += -D ARM
    endif
endif


all:

shell: doShell

example: doExample

test: doUnitTest

doShell:
	$(PYTHON)

doExample:
	$(PYTHON) -i $(EXAMPLEFILE)

doUnitTest:
	$(TESTBIN)

doLazyUnitTest:
	$(TESTBIN) -x
