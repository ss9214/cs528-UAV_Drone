import os

# Get all CSV files in the current directory
csv_files = [f for f in os.listdir() if f.endswith('.csv')]

# Process each CSV file
for csv_file in csv_files:
    # Read the file
    with open(csv_file, 'r') as file:
        content = file.read()
    
    # Replace acce with accl
    modified_content = content.replace('acce_', 'accl_')
    
    # Write back to file
    with open(csv_file, 'w') as file:
        file.write(modified_content)

print(f"Processed {len(csv_files)} CSV files")