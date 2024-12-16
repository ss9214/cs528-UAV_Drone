import re


def extract_runs(filename, direction):
    with open(filename, 'r') as file:
        data = file.readlines()

    runs = []
    current_run = []
    is_recording = False

    for line in data:
        # Detect the start of a new "RUN"
        if re.search(r"RUN \d+", line):
            # If we are already recording a run, save it and start a new one
            if current_run:
                runs.append(current_run)
                current_run = []
            is_recording = True
        
        # If recording, add the line to the current run
        if is_recording:
            current_run.append(line.strip())
    
    # Append the last run if we have reached the end of the file
    if current_run:
        runs.append(current_run)

    # Save only the first 40 runs
    # print(len(runs))
    for i, run in enumerate(runs[:40]):
        with open(f"../{direction}/{direction}_{i+1:02}.txt", 'w') as f:
            # print(f"creating textfile {i+21:02}")
            f.write("\n".join(run))

# Replace 'data.txt' with the actual file containing your data
direction = "none"
extract_runs(f'{direction}log.txt', direction)
