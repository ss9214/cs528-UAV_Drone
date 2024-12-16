import os

def delete_file(direction):
    """
    Deletes the specified file if it exists.
    
    Parameters:
        file_path (str): The path of the file to be deleted.
    """
    i = 1
    while(os.path.exists(f"../{direction}/{direction}_{i:02}.txt")):
        os.remove(f"../{direction}/{direction}_{i:02}.txt")
        i += 1


delete_file("none")
