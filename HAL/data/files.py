import os



def read_file(file_path: str) -> str:
    """
    This function reads the content of a file specified by the given path and returns it as a string.

    Args:
        file_path (str): The path to the file from which content will be read.

    Returns:
        str: The content of the file as a string.

    Example:
        >>> content = read_file("example.txt")
        >>> print(content)
        This will read the content of "example.txt" and print it.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If there is an issue opening or reading from the file.
    
    """
    with open(file_path, 'r') as file:
        content = file.read()
        return content
    
      






def write_file(file_path: str, content: any) -> None:
    """
    This function writes the specified content to a file at the given path. If the file already exists, 
    it will be overwritten with the new content. If the file does not exist, it will be created.

    Args:
        file_path (str): The path of the file where content will be written.
        content (any): The content to write to the file. This can be a string, list, or any other type.
                       It will be converted to a string before being written to the file.

    Returns:
        None: This function does not return any value.

    Example:
        >>> write_file("output.txt", "This is the content of the file.")
        This writes the string "This is the content of the file." to the "output.txt" file.

    Raises:
        IOError: If there is an issue opening or writing to the file.
    
    """
    with open(file_path, 'w') as file:
        file.write(content)







def append_to_file(file_path: str, content: any) -> None:
    """
    This function appends the specified content to a file at the given path. If the file does not exist,
    it will be created.

    Args:
        file_path (str): The path of the file to which content will be appended.
        content (any): The content to be appended to the file. This can be a string, list, or any other type.
                       It will be converted to a string before being written to the file.

    Returns:
        None

    """
    with open(file_path, "a") as file:
        file.write(content)






def create_folder(folder_name: str) -> None:
    """
    Create a new folder.

    Args:
        folder_path (str): Name of the folder to create.
    
    Returns:
        None
    """
    try:
        os.makedirs(folder_name, exist_ok=False)
        print(f'Folder {folder_name} created succesfully.')
    except:
        print(f'Folder {folder_name} already exists.')







def rename_files(folder_path: str, prefix="", start_index=0) -> None:
    """
    Renames all files in the given folder with a specified prefix and index.

    Args:
        folder_path (str): Folder to renamen.
        prefix (str): Prefix of the new files name. Default is `""`.
        start_index (int): Start index for renaming the files. Default is `0`

    Returns:
        None

    """
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    files = sorted(os.listdir(folder_path))  # Sort to maintain order
    dash = '_' if prefix != '' else ''
    for index, filename in enumerate(files, start=start_index):
        old_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(old_path):  # Ensure it's a file, not a folder
            extension = os.path.splitext(filename)[1]  # Keep the original file extension
            new_name = f"{prefix}{dash}{index}{extension}"
            new_path = os.path.join(folder_path, new_name)
            
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_name}")







def delete_file(file_path: str) -> None:
    """
    Deletes a file if it exists.
    
    Args:
        file_path (str): File to delete.
    
    Returns
        None
    """
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied for '{file_path}'.")







def delete_folder(folder_path: str) -> None:
    """
    Deletes an empty folder.
    
    Args:
        folder_path (str): Folder to delete.

    Returns:
        None
    """
    try:
        os.rmdir(folder_path)
        print(f"Folder '{folder_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
    except OSError:
        print(f"Error: Folder '{folder_path}' is not empty.")