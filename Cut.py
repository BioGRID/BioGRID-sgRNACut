#!/bin/env python

# Take a directory of zipped or unzipped files
# and generate a set of sgRNAs

import sys, string, argparse
import gzip, re
import MySQLdb
import Config
import Database
from os import listdir
from os.path import isfile, join

from classes import FastaParser

DB_COMMIT_COUNT = 25000

fileFormats = ['FASTA']
inputFormats = ['REFSEQ','ENSEMBL','ACEVIEW']
variants = {
	"SP" : re.compile( r'([AGCT]{20})([AGCT]{1}GG)', re.IGNORECASE )
}
chromosomeRE = re.compile( r'.*_(.*)\.mfa\.gz', re.IGNORECASE )

# Process Command Line Input
argParser = argparse.ArgumentParser( description = 'Cut sgRNA sequence fragments from sequences' )
argParser.add_argument( '--verbose', '-v', action='store_true', help='Display output while the process is running' )
argParser.add_argument( '--gzip', '-gz', action='store_true', help='Include this flag if input files are gzipped' )
argParser.add_argument( '--format', '-fm', action='store', type = str, nargs = '?', const='FASTA', choices=fileFormats, help = 'Types of files being parsed. Options are FASTA' );
argParser.add_argument( '--variant', '-var', action='store', type = str, nargs = '?', choices=variants.keys( ), help = 'Enter the type of sgRNA cut to be performed', required=True )
argParser.add_argument( '--type', '-t', action='store', type=str, nargs=1, help = 'Enter a type of record being parsed', choices=inputFormats, required=True )
argGroup = argParser.add_mutually_exclusive_group( required=True )
argGroup.add_argument( '--file', '-f', action='store', type = str, nargs = 1, help = 'A file name to parse' )
argGroup.add_argument( '--dir', '-d', action='store', type = str, nargs = 1, help = 'A directory containing 1 or more files to parse' )
inputArgs = argParser.parse_args( )

print inputArgs

# Get files to process

if inputArgs.verbose :
	print "Generating list of files to parse..."

files = []
if inputArgs.file :
	files = inputArgs.file
else :
	for file in listdir(inputArgs.dir[0]) : 
		filePath = join(inputArgs.dir[0], file)
		if isfile(filePath) :
			files.append(filePath)

if inputArgs.verbose :
	print "Files to parse..."
	print files
	
# Parse details and sequences out of each file

if( inputArgs.format == "FASTA" ) :
	# use FASTA Parser
	fasta = FastaParser.FastaParser( )
	
	for file in files :
	
		match = chromosomeRE.search( file )
		chromosome = "chr14" #match.group(1)
	
		if inputArgs.verbose :
			print "Working on File: " + str(file)
	
		sequences = fasta.parse( file, inputArgs.gzip )
		
		if inputArgs.verbose :
			print "-- Found: " + str(len(sequences)) + " sequences"
		
		with Database.db as cursor :
			
			matchCount = 0
			for seqID, seq in sequences.items( ) :
				print seq
				sys.exit( )
				matches = variants["SP"].finditer( seq )

				for match in matches :
					matchCount = matchCount + 1
					#cursor.execute( "INSERT INTO " + Config.DB_NAME + ".sgRNAs VALUES( '0', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW( ), %s )", [match.group(1), inputArgs.type, seqID, inputArgs.variant, match.group(2), match.start( ), match.end(1), match.start(2), match.end(2), chromosome, 'active'] )
					
					if 0 == (matchCount % DB_COMMIT_COUNT ) :
						Database.db.commit( )
						if inputArgs.verbose :
							print "-- Found: " + str(DB_COMMIT_COUNT) + " matches. Now at " + str(matchCount) + " total for this file..." 
						
			if inputArgs.verbose :
				print "---- Found " + str(matchCount) + " Total sgRNAs in this file..." 	
					
				Database.db.commit( )
			Database.db.commit( )
			

sys.exit( )