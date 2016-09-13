#!/bin/sh -e
cd ../input/refseq/
wget -r -nH --cut-dirs=100 --no-parent -A '*.rna.fna.gz' ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/mRNA_Prot/