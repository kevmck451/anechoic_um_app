# Functions for utilities

from datetime import datetime
import time
import csv


class CSVFile:
    def __init__(self, exp_num):

        # Get the current date and time
        current_time = datetime.now()

        # Format the date and time in a file-friendly format (e.g., YYYYMMDD_HHMMSS)
        file_name = current_time.strftime("%Y-%m-%d_%I-%M-%S_%p")

        csv_file_path = f'../output/{file_name}_Ex{exp_num}.csv'

        # Headers for the CSV file
        headers = ["stimulus number", "sample played", "speaker projected", "speaker selected", "reaction time",
                   "number selections"]

        # Open the file in write mode and create a CSV writer object
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write the headers
            writer.writerow(headers)

        # Output the created file name
        self.file_path = csv_file_path
        self.header, self.data = self._read_csv_file()

    def _read_csv_file(self):
        with open(self.file_path, 'r', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            data = list(csvreader)
        header = [column.strip('\ufeff') for column in data[0]]  # Remove the BOM character from the first column
        return header, data[1:]

    def write_row_at(self, row_number, data):
        # Read the entire file
        _, current_data = self._read_csv_file()

        # Ensure the row_number is within the bounds
        if 0 <= row_number <= len(current_data):
            # If row_number is equal to the length of current_data, it means append
            if row_number == len(current_data):
                current_data.append(data)
            else:
                # Replace or insert the data at the specified row number
                current_data[row_number] = data
        else:
            raise IndexError("Row number out of bounds")

        # Rewrite the file with the modified data
        with open(self.file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write the header
            csvwriter.writerow(self.header)
            # Write the modified data
            csvwriter.writerows(current_data)


# TIME CLASS TO GIVE STATS ABOUT HOW LONG FUNCTION TAKES
class time_class:
    def __init__(self, name):
        self.start_time = time.time()
        self.name = name

    def stats(self):
        total_time = round((time.time() - self.start_time), 1)
        mins = int(total_time // 60)  # Get the full minutes
        secs = int(total_time % 60)  # Get the remaining seconds

        # Formatting for two digits
        mins_str = f'{mins:02d}'
        secs_str = f'{secs:02d}'

        # Combine minutes and seconds in the format "00:00"
        formatted_time = f'{mins_str}:{secs_str}'

        return formatted_time

    def reaction_time(self):
        reaction_time = round((time.time() - self.start_time), 2)
        # print(reaction_time)
        return reaction_time
