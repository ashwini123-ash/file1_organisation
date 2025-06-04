from pathlib import Path
import shutil
import logging
from typing import Dict, List, Optional

# Configuration
FILE_CATEGORIES: Dict[str, List[str]] = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.rtf'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
    'Videos': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm'],
    'Music': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma'],
}

MISC_FOLDER = "MISC"
LOG_FILENAME = 'file_organizer.log'


def setup_logging() -> None:
    """Configure logging for the file organizer."""
    logging.basicConfig(
        filename=LOG_FILENAME,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def get_file_category(extension: str) -> str:
    """Determine the category for a given file extension."""
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return 'Others'


def get_destination_folder_name(file_extension: str) -> str:
    """Get the destination folder name for a file based on its extension."""
    if not file_extension:
        return MISC_FOLDER
    
    category = get_file_category(file_extension)
    if category == 'Others':
        # Use extension without dot as folder name for uncategorized files
        folder_name = file_extension[1:] if file_extension.startswith('.') else file_extension
        return folder_name if folder_name else MISC_FOLDER
    
    return category


def get_source_directory() -> Optional[Path]:
    """Get and validate the source directory from user input."""
    source_path = input("Enter the source directory path: ")
    source_dir = Path(source_path)
    
    if not source_dir.exists():
        print("The specified directory does not exist.")
        logging.error(f"Directory does not exist: {source_dir}")
        return None
    
    if not source_dir.is_dir():
        print("The specified path is not a directory.")
        logging.error(f"Path is not a directory: {source_dir}")
        return None
    
    return source_dir


def create_destination_directory(base_dir: Path, folder_name: str) -> Optional[Path]:
    """Create destination directory if it doesn't exist."""
    destination_dir = base_dir / folder_name
    try:
        destination_dir.mkdir(parents=True, exist_ok=True)
        return destination_dir
    except OSError as e:
        print(f"Error creating directory {destination_dir}: {e}")
        logging.error(f"Error creating directory {destination_dir}: {e}")
        return None


def get_unique_filename(destination_dir: Path, filename: str) -> str:
    """Generate a unique filename if the original already exists."""
    base_path = destination_dir / filename
    if not base_path.exists():
        return filename
    
    # Split filename and extension
    name_part = base_path.stem
    extension = base_path.suffix
    counter = 1
    
    # Keep incrementing counter until we find a unique name
    while True:
        new_filename = f"{name_part}_{counter}{extension}"
        new_path = destination_dir / new_filename
        if not new_path.exists():
            return new_filename
        counter += 1


def move_file(source_file: Path, destination_dir: Path) -> bool:
    """Move a file to the destination directory, handling duplicates by renaming."""
    # Get unique filename if original already exists
    unique_filename = get_unique_filename(destination_dir, source_file.name)
    destination_path = destination_dir / unique_filename
    
    try:
        shutil.move(str(source_file), str(destination_path))
        if unique_filename != source_file.name:
            print(f"Moved file: {source_file.name} to {destination_dir} (renamed to {unique_filename})")
            logging.info(f"Moved file: {source_file.name} to {destination_dir}, renamed to {unique_filename}")
        else:
            print(f"Moved file: {source_file.name} to {destination_dir}")
            logging.info(f"Moved file: {source_file.name} to {destination_dir}")
        return True
    except OSError as e:
        print(f"Error moving file {source_file.name} to {destination_dir}: {e}")
        logging.error(f"Error moving file {source_file.name} to {destination_dir}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error moving file {source_file.name} to {destination_dir}: {e}")
        logging.error(f"Unexpected error moving file {source_file.name} to {destination_dir}: {e}")
        return False


def process_file(file_path: Path, source_dir: Path) -> bool:
    """Process a single file and move it to the appropriate category folder."""
    file_extension = file_path.suffix.lower()
    
    # Log file discovery
    if not file_extension:
        print(f"No extension for file: {file_path.name}")
        logging.info(f"No extension for file: {file_path.name}")
    else:
        category = get_file_category(file_extension)
        if category == 'Others':
            print(f"Found file: '{file_path.name}', extension: {file_extension} (Uncategorized)")
            logging.info(f"Found file: {file_path.name}, extension: {file_extension}, uncategorized")
        else:
            print(f"Found file: '{file_path.name}', extension: {file_extension} (Category: {category})")
            logging.info(f"Found file: {file_path.name}, extension: {file_extension}, category: {category}")
    
    # Determine destination folder
    folder_name = get_destination_folder_name(file_extension)
    destination_dir = create_destination_directory(source_dir, folder_name)
    
    if destination_dir is None:
        return False
    
    return move_file(file_path, destination_dir)


def organize_files_in_directory(source_dir: Path) -> int:
    """Organize all files in the source directory and return count of moved files."""
    files_moved = 0
    print(f"Organizing files in: {source_dir.resolve()}")
    logging.info(f"Organizing files in: {source_dir.resolve()}")
    
    for item in source_dir.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            if process_file(item, source_dir):
                files_moved += 1
    
    return files_moved


def organize_files() -> None:
    """Main function to organize files in a directory."""
    setup_logging()
    print("-----Basic File Organizer-----")
    logging.info("Started file organization process.")
    
    source_dir = get_source_directory()
    if source_dir is None:
        return
    
    print(f"Source directory: {source_dir}")
    logging.info(f"Source directory: {source_dir}")
    
    files_moved = organize_files_in_directory(source_dir)
    
    # Report results
    if files_moved > 0:
        print(f"Moved {files_moved} files to their respective folders.")
        logging.info(f"Moved {files_moved} files to their respective folders.")
    else:
        print("No files were moved.")
        logging.info("No files were moved.")


if __name__ == "__main__":
    organize_files()






