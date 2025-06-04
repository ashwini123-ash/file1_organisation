# File Organizer - Automation Script

## Project Description

A Python automation script that automatically organizes files in a target directory based on file types. The script categorizes files into predefined folders (Documents, Images, Videos, Music) and handles uncategorized files by creating extension-specific folders.

## Features

- **Automatic File Classification**: Organizes files based on their extensions
- **Dynamic Folder Creation**: Creates category folders as needed
- **Duplicate File Handling**: Renames duplicate files to prevent overwrites
- **Comprehensive Logging**: Logs all operations for tracking and debugging
- **Error Handling**: Robust error handling with detailed error messages
- **Hidden File Protection**: Skips hidden files (files starting with '.')

## File Categories

- **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.odt`, `.rtf`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.svg`, `.webp`
- **Videos**: `.mp4`, `.avi`, `.mov`, `.wmv`, `.flv`, `.mkv`, `.webm`
- **Music**: `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.wma`
- **Others**: Files with unrecognized extensions are placed in folders named after their extension

## Requirements

- Python 3.6 or higher
- Standard library modules: `pathlib`, `shutil`, `logging`, `typing`

## Usage

1. Run the script:
   ```bash
   python file_organizer.py
   ```

2. Enter the source directory path when prompted

3. The script will:
   - Scan all files in the directory
   - Create category folders as needed
   - Move files to appropriate folders
   - Handle duplicates by renaming
   - Log all operations

## Example

```
Enter the source directory path: /Users/username/Downloads
Organizing files in: /Users/username/Downloads
Found file: 'document.pdf', extension: .pdf (Category: Documents)
Moved file: document.pdf to /Users/username/Downloads/Documents
Found file: 'image.jpg', extension: .jpg (Category: Images)
Moved file: image.jpg to /Users/username/Downloads/Images
Moved 2 files to their respective folders.
```

## Duplicate File Handling

When a file with the same name already exists in the destination folder, the script automatically renames the incoming file by appending a counter:
- `document.pdf` → `document_1.pdf`
- `image.jpg` → `image_1.jpg`

## Logging

All operations are logged to `file_organizer.log` with timestamps, including:
- File discoveries and categorizations
- File movements and renames
- Errors and warnings
- Directory creation operations

## Project Structure

```
file_organizer.py       # Main script
README.md              # Project documentation
file_organizer.log     # Log file (created after first run)
```

## Author

Created as part of INFOTACT SOLUTION automation project.

## License

This project is for educational purposes.
