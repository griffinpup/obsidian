import unittest
import os
import time
import csv_consolidator

class TestCsvConsolidator(unittest.TestCase):

    def test_consolidateCSV(self):    
        with open("test.csv", "w") as output:
            output.write("1,20.0,20.0\n1,30.0,30.0")
        csv_consolidator.consolidateCSV("test.csv", "testout.csv")
        with open("testout.csv") as input:
            first_line = input.readline()
        os.remove("test.csv")
        os.remove("testout.csv")
        self.assertEqual("1,25.0,25.0\n", str(first_line))

    def test_incorrect_csv_format(self):
        with open("test_incorrect_csv.csv", "w") as output:
            output.write("1,20,20")
        self.assertFalse(csv_consolidator.is_valid_input_CSV("test_incorrect_csv.csv"))
        os.remove("test_incorrect_csv.csv")

