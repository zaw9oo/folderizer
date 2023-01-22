import os
import argparse

parser = argparse.ArgumentParser(
    description="Clean up directory and put files into according folders."
)

parser.add_argument(
    "--path",
    type=str,
    default=".",
    help="Directory path of the to be caleaned directory",
)

args = parser.parse_args()
path = args.path

print(f"Cleaning up directory {path}")

# get all files from given directory
dir_content = os.listdir(path)

# create realtive paths
path_dir_contents = [os.path.join(path,file) for file in dir_content]

# check relative paths
#print(f"Content paths: {path_dir_contents}")

# filter regular file or dir/folder
files = [file for file in path_dir_contents if os.path.isfile(file)]
folders = [folder for folder in path_dir_contents if os.path.isdir(folder)]

# count moved files and list of already created folder
# to avoid multiple creations
moved = 0
created_folders = []

print(f"Cleaning up {len(files)} of {len(dir_content)} elements.")

# go through all files and move them into according folders
for file in files:
    full_file_path, file_type = os.path.splitext(file)
    file_dir_path = os.path.dirname(full_file_path)
    file_name = os.path.basename(full_file_path)

    #print(file_type)
    #print(full_file_path)
    #print(file_dir_path)
    #print(file_name)

    #break

    # skip current program file and hidden files
    if file_name == "folderizer" or file_name.startswith('.'):
        continue
    
    # create sub-folder if not exists
    subfolder_path = os.path.join(path, file_type[1:].lower())

    if subfolder_path not in folders and subfolder_path not in created_folders:
        try:
            os.mkdir(subfolder_path)
            created_folders.append(subfolder_path)
            print(f"Folder {subfolder_path} created.")
        except FileExistsError as err:
            print(f"Folder already exists at {subfolder_path}... {err}")

    # new file path
    new_full_file_path = os.path.join(subfolder_path, file_name) + file_type
    os.rename(file, new_full_file_path)
    moved += 1

    #print(f"Moved file: {file} to: {new_full_file_path}")

print(f"Renamed {moved} of {len(files)}")


