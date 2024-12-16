import re

def extract_csv_values(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    csv_lines = ["accl_x,accl_y,accl_z,gyro_x,gyro_y,gyro_z"]
    for line in lines:
        # Check if the line contains the data values
        match = re.search(r"(\s?-?\d+\.\d+,)+", line)
        if match:
            # Extract the matched CSV data
            csv_lines.append(match.group())

    # Write the extracted CSV values to the output file
    with open(output_file, 'w') as f:
        f.write("\n".join(csv_lines))

# Loop through each of the first 20 files and extract CSV values
direction = "none"
for i in range(1, 41):
    run = i+0
    input_file = f"../{direction}/{direction}_{run:02}.txt"
    output_file = f"../{direction}/{direction}_{run:02}.csv"
    extract_csv_values(input_file, output_file)
