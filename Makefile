DOCKER_BUILDDIR := $(abspath scripts/docker/build)
DOCKER_DIR := $(abspath scripts/docker)

TARBALLS := \
	app.tar \
	dictionary.tar

BUILD_TARBALLS := $(addprefix $(DOCKER_BUILDDIR)/,$(TARBALLS))

PYTHON_FILES := $(shell find app anagramizer -name "*.py")
PYTHON_REQUIREMENTS := $(shell find . -name "requirements.txt")
DICTIONARY_FILE := $(shell find . -name "dictionary.txt.gz")

all: tarballs build start

clean: stop
	rm -r $(DOCKER_BUILDDIR)

tarballs: $(BUILD_TARBALLS)

$(DOCKER_BUILDDIR)/app.tar: $(PYTHON_FILES) | $(DOCKER_BUILDDIR)
	tar czvf $@ $(PYTHON_FILES) $(PYTHON_REQUIREMENTS)

$(DOCKER_BUILDDIR)/dictionary.tar: $(DICTIONARY_FILE) | $(DOCKER_BUILDDIR)
	tar czvf $@ $(DICTIONARY_FILE)

$(DOCKER_BUILDDIR):
	mkdir -p $(DOCKER_BUILDDIR)


# DOCKER
build: ## Build the container
	docker build -t anagramizer:latest $(DOCKER_DIR)

start: ## Start the container
	docker run -it -d -p=3000:3000 --name=anagramizer --env "ANAGAMIZER_DICTIONARY=/var/lib/anagramizer/dictionary.txt.gz" anagramizer:latest app --bind=0.0.0.0:3000

stop: ## Stop and remove the container.
	docker stop anagramizer; docker rm anagramizer

