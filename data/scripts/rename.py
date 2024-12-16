import os

direction = "right"
# i = 1

for i in range(2,81):
    os.rename(f"../{direction}/{direction}_{i:02}.csv", f"../{direction}/{direction}turn_{i:02}.csv")