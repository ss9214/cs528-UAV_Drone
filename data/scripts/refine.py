import csv
import os

def modify_csv(direction):
    """
    Modifies the header of a CSV file and removes the first column.

    Args:
        file_path (str): Path to the CSV file to be modified.
    """

    for i in range(1,81):
        file_path = f"./csv_data/{direction}_{i:02}.csv"
        temp_file = f"./{direction}/{direction}_{i:02}.csv"

        # Define the new header
        new_header = ['accl_x', 'accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z']

        with open(file_path, 'r') as infile, open(temp_file, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # Read the original header
            old_header = next(reader)

            # Write the new header
            writer.writerow(new_header)

            # Process the rest of the rows
            for row in reader:
                # Remove the first column and write the updated row
                writer.writerow(row[1:])

# Example usage
# file_path = "../down/down_01.csv"  # Replace with your CSV file path
modify_csv("forward")


