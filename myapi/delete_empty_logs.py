import os


def delete_empty_logs(folder_path):
    if not os.path.exists(folder_path): return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.getsize(file_path) == 0:
            os.remove(file_path)