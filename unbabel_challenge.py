"""
-------------------------------------
Unbabel Backend Engineering Challenge
			Ricardo Miguel
				12/2022
-------------------------------------
Options:
	-h --help             Show this help message and exit
    --input_file          JSON file containing a stream of translation events
    --window_size         Defines time window within which the moving average delivery time of all translations is computed
"""

import json
import math
import argparse
from datetime import datetime, timedelta

def main(events, window_size):

	t_init   	= datetime.strptime(events[0]['timestamp'],'%Y-%m-%d %H:%M:%S.%f')  # Timestamp for first translation delivered
	t_end    	= datetime.strptime(events[-1]['timestamp'],'%Y-%m-%d %H:%M:%S.%f') # Timestamp for last translation delivered
	t_delta  	= (t_end - t_init).total_seconds() /60 # Number of minutes between first and last translation events
	time_window = timedelta(minutes = window_size)
	curr_time 	= t_init.replace(second=0, microsecond=0) 

	list_of_durations = [] # Stores relevant translation durations for further average computing
	list_of_dicts     = [] # Stores final data to dump in json file

	idx_in  = 0 # Index in list of events pointing at the next translation event to be included in the average
	idx_out = 0 # Index in list of events pointing at the at next translation event to be removed from the average

	# Making sure that the output file ranges across all event timestamps
	if t_delta < (t_end.minute - t_init.minute):
		t_delta += 1
		
	# For each minute, check if translation event should be either included or excluded from the computation of the arithmetic mean
	for minute in range(math.ceil(t_delta) + 1):

		# Selecting the next translation events to be included in the average
		for event in events[idx_in:]:

			event_time = datetime.strptime(event['timestamp'],'%Y-%m-%d %H:%M:%S.%f')

			if curr_time >= event_time:
				list_of_durations.append(event['duration'])
				idx_in += 1
			else:
				break

		# Selecting the next translation events to be removed from the average
		for event in events[idx_out:]:

			event_time = datetime.strptime(event['timestamp'],'%Y-%m-%d %H:%M:%S.%f')

			if (curr_time - time_window) >= event_time:
				list_of_durations.pop(0)
				idx_out += 1
			else:
				break
		
		event_dict = {"date" : str(curr_time), "average_delivery_time" : avg_list(list_of_durations)}
		list_of_dicts.append(event_dict)

		curr_time += timedelta(minutes = 1)

	# Dumping the list of dictionaries in output_file.json
	with open("output_file.json", "w") as output_file:
		json.dump(list_of_dicts,output_file, indent = 1)

def avg_list(ls) -> float:
	"""
	Computes the arithmetic mean of the numbers in a list ls
	"""

	if len(ls) == 0:
		return 0
	else: 
		return round(sum(ls)/len(ls),1)

if __name__ == "__main__":

	# Parser for command-line options and arguments
	parser = argparse.ArgumentParser(
		prog 		= "Unbabel Challenge 2022",
		description = "Backend engineering challenge consisting in a simple command line application that parses a stream of translations and computes the average delivery time per minute, within a specified time window."
	)

	parser.add_argument('--input_file' , help = "json file containing a stream of translation events", type = argparse.FileType('r'), required = True)
	parser.add_argument('--window_size', help = "defines the time window within which the moving average delivery time of all translations is computed", type = int, required = True)

	args = parser.parse_args()

	try:
		events = json.load(args.input_file)
		window_size = args.window_size

		if window_size < 0 or not isinstance(window_size, int):
			raise argparse.ArgumentTypeError("'window_size' must be a positive integer.")

		main(events, window_size)

	except ValueError:
		print("Deserializing JSON failed. \nInclude a valid format.")
		print("[{\"timestamp\": <string>,\"translation_id\": <string>,\"source_language\": <string>,\"target_language\": <string>,\"client_name\": <string>,\"event_name\": <string>,\"nr_words\": <int>, \"duration\": <int>}, ...]")

	except IndexError:
		print("List of JSONs is empty.")