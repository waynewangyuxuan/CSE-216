#!/bin/sh
# Compile main.tex and supplement_details.tex to PDF with the current ACM class in template/. Needs tectonic (brew install tectonic).
cd "$(dirname "$0")" && tectonic -Z search-path=template main.tex && tectonic -Z search-path=template supplement_details.tex
