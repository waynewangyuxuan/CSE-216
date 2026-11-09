#!/bin/sh
# Compile main.tex to main.pdf with the current ACM class in template/. Needs tectonic (brew install tectonic).
cd "$(dirname "$0")" && tectonic -Z search-path=template main.tex
