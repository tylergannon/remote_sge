# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = remote_sge
SOURCEDIR     = source
BUILDDIR      = build

APIDOCOPTS    = -f --ext-autodoc --ext-intersphinx
SPHINXAPIDOC  = sphinx-apidoc
DOC_SRC_DIR   = ./source
SGE_MODULE_PATH   = $(PWD)/../src/sge
CLI_MODULE_PATH   = $(PWD)/../src/sge_client
SRV_MODULE_PATH   = $(PWD)/../src/sge_server

# EXCLUDES      = $(MODULE_PATH)/io/drmaa_calls.py
EXCLUDES      = 

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

docstubs:
	@$(SPHINXAPIDOC) $(APIDOCOPTS) -o $(DOC_SRC_DIR) $(SGE_MODULE_PATH) $(EXCLUDES)
	@$(SPHINXAPIDOC) $(APIDOCOPTS) -o $(DOC_SRC_DIR) $(CLI_MODULE_PATH) $(EXCLUDES)
	@$(SPHINXAPIDOC) $(APIDOCOPTS) -o $(DOC_SRC_DIR) $(SRV_MODULE_PATH) $(EXCLUDES)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)