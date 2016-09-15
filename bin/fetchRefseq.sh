#!/bin/sh -e
cd ../input/refseq/
wget -r -nH --cut-dirs=100 --no-parent -A '*GRCh38.p7_*.fa.gz' ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/H_sapiens/Assembled_chromosomes/seq/