import os
import shutil


def get_files_in_folder(folder):
    return_files = []
    files = os.listdir(folder)
    for file in files:
        file_path = os.path.join(folder, file)
        if os.path.isdir(file_path):
            continue
        else:
            return_files.append(file)
    
    return return_files


def move_files_into_folders(files, audiobook_folder, destination_folder):
    for file in files:
        new_folder_name = os.path.splitext(file)[0]
        file_path = os.path.join(audiobook_folder, file)
        new_folder_path = os.path.join(destination_folder, new_folder_name)

        if file.endswith(".m4b") or file.endswith(".mp3") and not os.path.exists(new_folder_path):
            if os.path.exists(new_folder_path):
                print(f"Folder {new_folder_path} already exists")
                continue
            os.mkdir(new_folder_path)
            # shutil.move(file_path, new_folder_path)
            shutil.copy(file_path, new_folder_path)
            print(f"copying {file_path} to {new_folder_path}")


audiobook_folder = "L:\\Plex-Media-Server\\Audiobooks\\books"
final_folder = "L:\\Plex-Media-Server\\Audiobooks\\final"
files = get_files_in_folder(audiobook_folder)

move_files_into_folders(files, audiobook_folder, final_folder)