TARGETS += \
	knowledge \
	simple-schedule \
	artificial-trace-generation \
	simple-lppm-comparison \
	extend \
	stop-after-lppm \
 	start-after-lppm
 
all: 
	set -e; for d in $(TARGETS); do $(MAKE) -C $$d ; done

clean: 
	set -e; for d in $(TARGETS); do $(MAKE) clean -C $$d ; done
