
# Parse FASTA details into a dictionary

import sys, string
import Config
import gzip

class FastaParser( ) :

	def __init__( self ) :		
		self.reset( )
		
	def reset( self ) :
		self.sequences = { }
		self.currentHeading = ""
		self.currentSeq = ""
		
	def parse( self, file, isGzip ) :
		
		"""
		Step through a FASTA file and process details into
		the sequences dict
		"""
		
		self.reset( )
		
		if isGzip :
			
			with gzip.open( file, 'r' ) as fp :
				self.processFile( fp )
				
		else :
		
			with open( file, 'r' ) as fp :
				self.processFile( fp )
				
		return self.sequences
				
	def processFile( self, fp ) :
	
		"""
		Fetch each sequence and header combo
		for inserting into the sequences dict
		"""
	
		data = fp.read( );
		dataSplit = data.split( "\n" )
		
		self.processRecord( )
		self.currentHeading = dataSplit[0].split( "|" )
		self.currentSeq = ""
		
		dataSplit.pop( )
		self.currentSeq = "".join(dataSplit)
		
		# lineCount = 0
		# for line in fp.readlines( ) :
			# line = line.strip( )
			# lineCount = lineCount + 1
			
			# print "Reading Line: " + str(lineCount)
			
			# if len(line) <= 0 :
				# continue
					
			# if ">" == line[0] :
			
				# Insert the old record and then prepare
				# for the new one
				# self.processRecord( )
				# self.currentHeading = line.split( "|" )
				# self.currentSeq = ""
				
			# else :
			
				# Append the sequence with the latest line
				# self.currentSeq = self.currentSeq + line
				
		# Do this one last time to capture the last one 
		# in the file
		self.processRecord( )
				
	def processRecord( self ) :
	
		"""
		Insert the fetched data into the dictionary
		"""
	
		if self.currentSeq != "" :
			splitID = self.currentHeading[3].split( "." )
			self.sequences[splitID[0]] = self.currentSeq
			