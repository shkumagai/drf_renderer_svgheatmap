PIP_COMPILE_CMD := pipx run --spec=pip-tools pip-compile
SRCS := base.in development.in packaging.in testing.in
OBJS := $(SRCS:%.in=%.txt)

.PHONY: all
all:
	$(MAKE) $(OBJS)
	$(MAKE) requirements.txt

.PHONY: upgrade
upgrade:
	OPTS=--upgrade $(MAKE) $(OBJS)
	OPTS=--upgrade $(MAKE) requirements.txt

.PHONY: upgrade-django
upgrade-django:
	OPTS=--upgrade-package=Django $(MAKE) $(OBJS)
	OPTS=--upgrade-package=Django $(MAKE) requirements.txt

%.txt: %.in
	$(PIP_COMPILE_CMD) $(OPTS) --output-file=$@ $^
	[ $@ == "requirements.txt" ] || touch requirements.in
