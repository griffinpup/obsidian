import sys
import re

def consolidateCSV(csvPath, outputFile):
    """ Takes the csv file located at csvPath that was downloaded from 
    https://api.bitcoincharts.com/v1/csv/ and consolidates the duplicate 
    timestamps into one entry with the price and volume values being the 
    average of all entries with that timestamp. It is required that the 
    csv file located at csvPath has the form: 
        [timestamp], [price], [volume]
    """
    print("beginning consolidation of " + csvPath + " to output file " + \
          outputFile + "...\nthis may take a while...\n")

    with open(csvPath) as input:
        firstLine = input.readline().split(",")
        currentTimeStamp = firstLine[0]
        price_sum = float(firstLine[1])
        volume_sum = float(firstLine[2])
        with open(outputFile, "w") as output:
            n_lines_since_reset = 1
            for i in input:
                current_line = i.split(",")
                if current_line[0] != currentTimeStamp:
                    output.write(currentTimeStamp + "," \
                                 + str(price_sum / n_lines_since_reset) + "," \
                                 + str(volume_sum / n_lines_since_reset) + "\n")
                    currentTimeStamp = current_line[0]
                    price_sum = float(current_line[1])
                    volume_sum = float(current_line[2])
                    n_lines_since_reset = 1
                else:
                    price_sum += float(current_line[1])
                    volume_sum += float(current_line[2])
                    n_lines_since_reset += 1
            output.write(currentTimeStamp + "," \
                         + str(price_sum / n_lines_since_reset) + "," \
                         + str(volume_sum / n_lines_since_reset) + "\n")
    
    print("consolidation completed successfully.\n")

def is_valid_input_CSV(csvPath):
    """ Analyzes the first line in the given csv path and checks to see if 
    it is in the expected format.
    """
    csv_line_regex = r"^\d+,\d+\.\d+,\d+\.\d+$"
    with open(csvPath) as input:
        first_line = input.readline()
        if re.match(csv_line_regex, first_line):
            return True
    return False

if len(sys.argv) != 3:
    print("Incorrect command line arguments. The correct format is " + \
          "\"python3 [csvPath] [outputFile]\"")
elif not is_valid_input_CSV(sys.argv[1]):
    print("Input file is not in the format [timestamp],[price],[volume]. Make " \
          + "sure that the CSV file was downloaded from " \
          + "https://api.bitcoincharts.com/v1/csv/ and try again")
else:
    consolidateCSV(sys.argv[1], sys.argv[2])
