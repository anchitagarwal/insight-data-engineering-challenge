import sys, getopt, datetime

class find_political_donors:
	def __init__(self, OUTPUT_FILE_ZIP, OUTPUT_FILE_DATE):
		"""
		Init method for this class
		"""		
		# variables for sanity check
		self.TXN_DATE_ISVALID = False
		self.ZIP_ISVALID = False

		# output files
		self.OUTPUT_FILE_ZIP = OUTPUT_FILE_ZIP
		self.OUTPUT_FILE_DATE = OUTPUT_FILE_DATE

	def calculate_median_by_zip(self, cmte_id, zip_code, txn_amount):
		"""
		Method that calculates the running median for a recipient grouped by zip codes.
		Logs the information to the output file `OUTPUT_FILE_ZIP`

		Args:
			cmte_id: String, recipient ID
			zip_code: String, ZIP code
			txn_amount: int, contribution amount

		Nothing returned.
		"""
		

	def calculate_median_by_date(self, cmte_id, txn_date, txn_amount):
		"""
		"""
	
	def parse_line(self, line):
		"""
		Method to parse a line from the input file and extract useful information
		"""
		# parse lines to extract relevant information
		split_line = line.split('|')
		cmte_id = split_line[0]
		zip_code = split_line[10][:5]
		txn_date = split_line[13]
		txn_amount = int(split_line[14])
		other_id = split_line[15]

		# constraint checks for all attributes
		if len(cmte_id) != 0 and len(txn_amount) != 0 and len(other_id) == 0:
			# validate ZIP code
			if len(zip_code) == 5:
				self.ZIP_ISVALID = True

			# validate TRANSACTION_DT
			if len(txn_date) == 8:
				month = int(txn_date[:2])
				day = int(txn_date[2:4])
				year = int(txn_date[4:])
				# datetime.datetime() raises ValueError if date is invalid
				try:
					txn_datetime = datetime.datetime(year=year, month=month, day=day)
					# validates if the input date is not in the future
					if txn_datetime <= datetime.datetime.now():
						self.TXN_DATE_ISVALID = True
				except ValueError as err:
					self.TXN_DATE_ISVALID = False

			# if ZIP code is valid, calculate median and write to output file 1 (by_zip)
			if ZIP_ISVALID:
				calculate_median_by_zip(cmte_id, zip_code, txn_amount)

			# if transaction date is valid, calculate median and write to output file 2 (by_date)
			if TXN_DATE_ISVALID:
				calculate_median_by_date(cmte_id, zip_code, txn_amount)

		import pdb
		pdb.set_trace()

def main(argv):
	"""
	Main method that handles the input arguments are call the appropriate function.

	Input:
		argv: command line arguments
	"""
	INPUT_FILE = ''
	OUTPUT_FILE_ZIP = ''
	OUTPUT_FILE_DATE = ''
	fpd = find_political_donors(OUTPUT_FILE_ZIP, OUTPUT_FILE_DATE)

	# command line validation
	try:
		(options, args) = getopt.getopt(argv, "h:i:z:d:", ["in=", "out1=", "out2="])
	except getopt.GetoptError as err:
		print err
		print 'find_political_donors.py -i <inputfile> -z <outputfile_zip> -d <outputfile_date>'
		sys.exit(2)

	for option, arg in options:
		if option == '-h':
			print 'find_political_donors.py -i <inputfile> -z <outputfile_zip> -d <outputfile_date>'
			sys.exit()
		elif option in ('-i', '--in'):
			INPUT_FILE = arg
		elif option in ('-z', '--out1'):
			OUTPUT_FILE_ZIP = arg
		elif option in ('-d', '--out2'):
			OUTPUT_FILE_DATE = arg

	print 'Input file is ', INPUT_FILE
	print 'Output file (zip) is ', OUTPUT_FILE_ZIP
	print 'Output file (date) is ', OUTPUT_FILE_DATE

	with open(INPUT_FILE, 'r') as infile:
		for line in infile:
			fpd.parse_line(line)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'find_political_donors.py -i <inputfile> -z <outputfile_zip> -d <outputfile_date>'
		sys.exit(2)
	main(sys.argv[1:])