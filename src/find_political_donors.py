import sys, getopt, datetime
import os.path
from heapq import heappush as push, heappop as pop

class zip_node:
	"""
	Zip node data structure for maintaining recipient by zip
	"""
	def __init__(self, cmte_id, zip_code):
		"""
		Init method for this class
		"""
		self.cmte_id = cmte_id
		self.zip_code = zip_code

	def __key(self):
		"""
		Method that returns tuple for this class for hash computation
		"""
		return (self.cmte_id, self.zip_code)

	def __hash__(self):
		"""
		Method that returns the hash for every object
		"""
		return hash(self.__key())

	def __eq__(x, y):
		"""
		Method that further checks if two hashes are equal

		Args:
			x: zip_node object 1
			y: zip_node object 2

		Returns True if equal.
		"""
		return x.__key() == y.__key()

class date_node:
	"""
	Date node data structure for maintaining recipient by date
	"""
	def __init__(self, cmte_id, txn_date):
		"""
		Init method for this class
		"""
		self.cmte_id = cmte_id
		self.txn_date = txn_date

	def __key(self):
		"""
		Method that returns tuple for this class for hash computation
		"""
		return (self.cmte_id, self.txn_date)

	def __hash__(self):
		"""
		Method that returns the hash for every object
		"""
		return hash(self.__key())

	def __eq__(x, y):
		"""
		Method that further checks if two hashes are equal

		Args:
			x: zip_node object 1
			y: zip_node object 2

		Returns True if equal.
		"""
		return x.__key() == y.__key()

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

		# dict to store recipient ID and zip code
		self.zip_dict = {}

		# dict to store recipient ID and transaction date
		self.date_dict = {}

	def running_median(self, min_heap, max_heap, val):
		"""
		This method utilizes two heaps to maintain a running median.
		The idea is to maintain a max_heap with values less than or equal to the current median and
		a min_heap with values greater than the current median.
		
		How to find the median?
		Median is the root of the larger heap, if the sizes differ.
		Else, median is the average of roots of both heap.

		Args:
			min_heap: Min heap for the current recipient and zip code
			max_heap: Max heap for the current recipient and zip code
			val: Current transaction amount

		Returns:
			min_heap: Update min heap after new value
			max_heap: Updated max heap after new value
		"""
		# if both heaps are empty, insert the current value to min_heap
		if len(min_heap) == 0 and len(max_heap) == 0:
			push(max_heap, -1 * val)
			return min_heap, max_heap, val

		# while inserting second element, insert it to the min_heap
		# swap heaps if min_heap[0] > max_heap[0]
		elif len(max_heap) == 1 and len(min_heap) == 0:
			push(min_heap, val)
			if (-1 * max_heap[0]) > min_heap[0]:
				tmp = min_heap[0]
				min_heap[0] = max_heap[0] * -1
				max_heap[0] = tmp * -1
			return min_heap, max_heap, int(round((min_heap[0] + max_heap[0] * -1) / 2.))

		else:
			# it's ok to set median as -1 for default as donations cannot be negative
			median = -1
			if len(min_heap) != len(max_heap):
				median = min_heap[0] if len(min_heap) > len(max_heap) else (max_heap[0] * -1)
			else:
				median = int(round((min_heap[0] + max_heap[0] * -1) / 2.))

			# if the new value is less than current median, push it to max_heap
			if val <= median:
				push(max_heap, -1 * val)
			else:
				push(min_heap, val)

			# if size of both heaps differ by more than 1, balance the heaps
			if abs(len(min_heap) - len(max_heap)) > 1:
				if len(min_heap) > len(max_heap):
					push(max_heap, pop(min_heap) * -1)
				else:
					push(min_heap, pop(max_heap) * -1)

			# calculate the new median and return it with updated heaps
			new_median = -1
			if len(min_heap) != len(max_heap):
				new_median = min_heap[0] if len(min_heap) > len(max_heap) else (max_heap[0] * -1)
			else:
				new_median = int(round((min_heap[0] + max_heap[0] * -1) / 2.))

			return min_heap, max_heap, new_median

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
		# create a new zip node object
		obj = zip_node(cmte_id, zip_code)

		median = -1
		# core functionality of the method
		# calculates running median for every recipient,zip pair by maintaining 2 heaps
		if not self.zip_dict.has_key(obj):
			min_heap, max_heap, median = self.running_median([], [], txn_amount)
			self.zip_dict[obj] = [txn_amount, min_heap, max_heap]
		else:
			total_amount = self.zip_dict[obj][0] + txn_amount
			min_heap = self.zip_dict[obj][1]
			max_heap = self.zip_dict[obj][2]
			min_heap, max_heap, median = self.running_median(min_heap, max_heap, txn_amount)
			self.zip_dict[obj] = [total_amount, min_heap, max_heap]

		# print cmte_id, zip_code, min_heap, max_heap, median

		# total count and amount
		count = len(min_heap) + len(max_heap)
		amount = self.zip_dict[obj][0]

		# write the information to output file
		with open(self.OUTPUT_FILE_ZIP, 'a+') as outfile:
			line_out = '|'.join([cmte_id, zip_code, str(median), str(count), str(amount)])
			outfile.write(line_out + '\n')

	def calculate_median_by_date(self, cmte_id, txn_date, txn_amount):
		"""
		Method that calculates the running median for a recipient on a given date.
		Logs the information to the output file `OUTPUT_FILE_DATE`

		Args:
			cmte_id: String, recipient ID
			txn_date: String, transaction date
			txn_amount: int, contribution amount

		Nothing returned.
		"""
		# create a new date_node object
		obj = date_node(cmte_id, txn_date)

		median = -1
		# core functionality of the method
		# calculates running median for every recipient for a specific date (2 heaps method)
		if not self.date_dict.has_key(obj):
			min_heap, max_heap, median = self.running_median([], [], txn_amount)
			self.date_dict[obj] = [txn_amount, min_heap, max_heap, median]
		else:
			total_amount = self.date_dict[obj][0] + txn_amount
			min_heap = self.date_dict[obj][1]
			max_heap = self.date_dict[obj][2]
			min_heap, max_heap, median = self.running_median(min_heap, max_heap, txn_amount)
			self.date_dict[obj] = [total_amount, min_heap, max_heap, median]
	
	def parse_line(self, line):
		"""
		Method to parse a line from the input file and extract useful information
		"""
		# parse lines to extract relevant information
		split_line = line.split('|')
		cmte_id = split_line[0]
		zip_code = split_line[10][:5]
		txn_date = split_line[13]
		txn_amount = split_line[14]
		other_id = split_line[15]

		# constraint checks for all attributes
		if len(cmte_id) != 0 and len(txn_amount) != 0 and len(other_id) == 0:
			# validate ZIP code
			if len(zip_code) == 5:
				self.ZIP_ISVALID = True

			# validate TRANSACTION_DT
			if len(txn_date) != 8:
				self.TXN_DATE_ISVALID = False
			else:
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
			if self.ZIP_ISVALID:
				self.calculate_median_by_zip(cmte_id, zip_code, int(txn_amount))

			# if transaction date is valid, calculate median and write to output file 2 (by_date)
			if self.TXN_DATE_ISVALID:
				self.calculate_median_by_date(cmte_id, txn_date, int(txn_amount))

	def write_medianvals_by_date(self):
		"""
		Method that writes the analyzed results to OUTPUT_FILE_DATE for every recipient per date
		"""
		# sort the date dictionary by CMTE_ID and transaction date
		d_dict = self.date_dict
		d_dict = sorted(d_dict.iteritems(), key=lambda x: (x[0].cmte_id, x[0].txn_date))

		# write the information to output file
		with open(self.OUTPUT_FILE_DATE, 'a+') as outfile:
			for entry in d_dict:
				# extract information from the sorted dictionary
				cmte_id = entry[0].cmte_id
				txn_date =  entry[0].txn_date
				median = str(entry[1][3])
				count = str(len(entry[1][1]) + len(entry[1][2]))
				total_amount = str(entry[1][0])

				line_out = '|'.join([cmte_id, txn_date, median, count, total_amount])
				outfile.write(line_out + '\n')

def main(argv):
	"""
	Main method that handles the input arguments are call the appropriate function.

	Input:
		argv: command line arguments
	"""
	INPUT_FILE = ''
	OUTPUT_FILE_ZIP = ''
	OUTPUT_FILE_DATE = ''

	# command line validation
	try:
		(options, args) = getopt.getopt(argv, "h:i:z:d:", ["in=", "out1=", "out2="])
	except getopt.GetoptError as err:
		print '\nHow to run:\n'
		print 'python ./src/find_political_donors.py -i <inputfile> -z <outputfile_zip> -d <outputfile_date>\n'
		sys.exit(2)

	for option, arg in options:
		if option == '-h':
			print '\nHow to run:\n'
			print 'python ./src/find_political_donors.py -i <inputfile> -z <outputfile_zip> -d <outputfile_date>\n'
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

	# delete output files if they already exist
	if os.path.isfile(OUTPUT_FILE_ZIP):
		os.remove(OUTPUT_FILE_ZIP)
	if os.path.isfile(OUTPUT_FILE_DATE):
		os.remove(OUTPUT_FILE_DATE)

	# call the analytics method
	fpd = find_political_donors(OUTPUT_FILE_ZIP, OUTPUT_FILE_DATE)
	with open(INPUT_FILE, 'r') as infile:
		for line in infile:
			fpd.parse_line(line)
	# call the below method to write the output file for medianvals by date
	fpd.write_medianvals_by_date()

	# check if OUTPUT_FILE_ZIP exists or not, if not, create an empty file
	if not os.path.isfile(OUTPUT_FILE_ZIP):
		open(OUTPUT_FILE_ZIP, 'a').close()

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'find_political_donors.py -i <inputfile> -z <outputfile_zip> -d <outputfile_date>'
		sys.exit(2)
	main(sys.argv[1:])
