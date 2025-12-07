FQBN := arduino:avr:uno
MCU := atmega328p
BAUD_PROG := 115200
BAUD_MONITOR := 9600
PROGRAMMER := arduino

INO := $(basename $(notdir $(wildcard *.ino)))
HEX := $(INO).ino.hex


TMPDIR := ./tmp-arduino-build-$(USER)

all: $(HEX)

.PHONY: install-core
install-core:
	@if ! arduino-cli core list | grep -q '^arduino:avr'; then\
		echo "Installing arduino:avr ..."; \
		arduino-cli core update-index; \
		arduino-cli core install arduino:avr; \
	else \
		echo "arduino:avr already installed"; \
	fi


$(HEX): $(INO).ino | install-core
	mkdir -p $(TMPDIR)/$(INO)
	cp $(INO).ino $(TMPDIR)/$(INO)/$(INO).ino
	arduino-cli compile --fqbn $(FQBN) --output-dir $(TMPDIR)/$(INO) \
		--verbose $(TMPDIR)/$(INO)
	cp $(TMPDIR)/$(INO)/$(HEX) .
	rm -rf $(TMPDIR)

ifneq ($(filter upload monitor,$(MAKECMDGOALS)),)
ifeq ($(shell uname),Linux)
PORT ?= $(shell ls /dev/ttyUSB* 2>/dev/null | head -n 1)
else
PORT ?= $(shell ls /dev/cu.usb* 2>/dev/null | head -n 1)
endif
endif

upload: $(HEX)
	@if [ -z "$(PORT)" ]; then \
		echo "Kein Port gefunden!"; \
		exit 1; \
	fi
	avrdude -v -p $(MCU) -c $(PROGRAMMER) -P $(PORT) -b $(BAUD_PROG) -D \
		-U flash:w:$(HEX):i

monitor:
	@if [ -z "$(PORT)" ]; then \
		echo "Kein Port gefunden!"; \
		exit 1; \
	fi
	mkdir -p $(TMPDIR)/
	echo 'bindkey "^X" colon "kill\015"' > $(TMPDIR)/screen.rc
	echo 'caption always "Quit with Control-X"' >> $(TMPDIR)/screen.rc
	screen -c $(TMPDIR)/screen.rc $(PORT) $(BAUD_MONITOR)	
	rm -rf $(TMPDIR)

clean:
	rm -f $(HEX)

