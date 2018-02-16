import sys
import re

def consolidate_CSV(csv_path, outputFile):
    """ Takes the csv file located at csv_path that was downloaded from 
    https://api.bitcoincharts.com/v1/csv/ and consolidates the duplicate 
    timestamps into one entry with the price and volume values being the 
    average of all entries with that timestamp. It is required that the 
    csv file located at csv_path has the form: 
        [timestamp], [price], [volume]
    """
    print("beginning consolidation of " + csv_path + " to output file " + \
          outputFile + "...\nthis may take a while...\n")

    with open(csv_path) as input:
        first_line = input.readline().split(",")
        current_time_stamp = first_line[0]
        price_sum = float(first_line[1])
        volume_sum = float(first_line[2])
        with open(outputFile, "w") as output:
            n_lines_since_reset = 1
            for i in input:
                current_line = i.split(",")
                if current_line[0] != current_time_stamp:
                    output.write(current_time_stamp + "," \
                                 + str(price_sum / n_lines_since_reset) + "," \
                                 + str(volume_sum / n_lines_since_reset) + "\n")
                    current_time_stamp = current_line[0]
                    price_sum = float(current_line[1])
                    volume_sum = float(current_line[2])
                    n_lines_since_reset = 1
                else:
                    price_sum += float(current_line[1])
                    volume_sum += float(current_line[2])
                    n_lines_since_reset += 1
            output.write(current_time_stamp + "," \
                         + str(price_sum / n_lines_since_reset) + "," \
                         + str(volume_sum / n_lines_since_reset) + "\n")
    
    print("consolidation completed successfully.\n")

def is_valid_input_CSV(csv_path):
    """ Analyzes the first line in the given csv path and checks to see if 
    it is in the expected format.
    """
    csv_line_regex = r"^\d+,\d+\.\d+,\d+\.\d+$"
    with open(csv_path) as input:
        first_line = input.readline()
        if re.match(csv_line_regex, first_line):
            return True
    return False

if len(sys.argv) != 3:
    print("Incorrect command line arguments. The correct format is " + \
          "\"python3 [csv_path] [outputFile]\"")
elif not is_valid_input_CSV(sys.argv[1]):
    print("Input file is not in the format [timestamp],[price],[volume]. Make " \
          + "sure that the CSV file was downloaded from " \
          + "https://api.bitcoincharts.com/v1/csv/ and try again")
else:
    consolidate_CSV(sys.argv[1], sys.argv[2])
