# File Organizer - User Guide

## Getting Started

### Step 1: Prepare Your Environment

Ensure you have Python 3.6 or higher installed on your system. You can check your Python version by running:

```bash
python --version
```

### Step 2: Download the Script

Save the `file_organizer.py` file to your desired location.

### Step 3: Running the Script

1. Open your terminal or command prompt
2. Navigate to the directory containing `file_organizer.py`
3. Run the script:

```bash
python file_organizer.py
```

## Detailed Walkthrough

### Initial Setup

When you run the script, you'll see:

```
-----Basic File Organizer-----
Enter the source directory path: 
```

**Example Input**: `/Users/username/Downloads` or `C:\Users\username\Downloads`

### What Happens Next

The script will:

1. **Validate the directory** - Check if the path exists and is a valid directory
2. **Scan for files** - Look for all files (excluding hidden files)
3. **Categorize files** - Determine which category each file belongs to
4. **Create folders** - Make category folders if they don't exist
5. **Move files** - Transfer files to their appropriate folders
6. **Handle duplicates** - Rename files if duplicates are found

### Example Output

```
Organizing files in: /Users/username/Downloads
Found file: 'vacation_photo.jpg', extension: .jpg (Category: Images)
Moved file: vacation_photo.jpg to /Users/username/Downloads/Images
Found file: 'report.pdf', extension: .pdf (Category: Documents)
Moved file: report.pdf to /Users/username/Downloads/Documents
Found file: 'song.mp3', extension: .mp3 (Category: Music)
Moved file: song.mp3 to /Users/username/Downloads/Music
Found file: 'movie.mp4', extension: .mp4 (Category: Videos)
Moved file: movie.mp4 to /Users/username/Downloads/Videos
Found file: 'data.csv', extension: .csv (Uncategorized)
Moved file: data.csv to /Users/username/Downloads/csv
Moved 5 files to their respective folders.
```

### Folder Structure After Organization

Before:
```
Downloads/
├── vacation_photo.jpg
├── report.pdf
├── song.mp3
├── movie.mp4
└── data.csv
```

After:
```
Downloads/
├── Documents/
│   └── report.pdf
├── Images/
│   └── vacation_photo.jpg
├── Music/
│   └── song.mp3
├── Videos/
│   └── movie.mp4
├── csv/
│   └── data.csv
└── file_organizer.log
```

## Duplicate File Handling

### Scenario: Duplicate Files

If you run the organizer again with a file that has the same name as an already organized file:

**Before**:
```
Downloads/
├── Documents/
│   └── report.pdf
└── report.pdf (new file)
```

**After**:
```
Downloads/
├── Documents/
│   ├── report.pdf
│   └── report_1.pdf
```

**Console Output**:
```
Found file: 'report.pdf', extension: .pdf (Category: Documents)
Moved file: report.pdf to /Users/username/Downloads/Documents (renamed to report_1.pdf)
```

## Understanding File Categories

### Predefined Categories

| Category | Extensions |
|----------|------------|
| Documents | .pdf, .doc, .docx, .txt, .xls, .xlsx, .ppt, .pptx, .odt, .rtf |
| Images | .jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg, .webp |
| Videos | .mp4, .avi, .mov, .wmv, .flv, .mkv, .webm |
| Music | .mp3, .wav, .aac, .flac, .ogg, .wma |

### Uncategorized Files

Files with extensions not in the predefined categories will be placed in folders named after their extension:
- `.zip` files → `zip/` folder
- `.py` files → `py/` folder
- `.csv` files → `csv/` folder

## Logging and Troubleshooting

### Log File

All operations are recorded in `file_organizer.log`:

```
2025-05-26 10:30:15,123 - INFO - Started file organization process.
2025-05-26 10:30:15,124 - INFO - Source directory: /Users/username/Downloads
2025-05-26 10:30:15,125 - INFO - Organizing files in: /Users/username/Downloads
2025-05-26 10:30:15,126 - INFO - Found file: vacation_photo.jpg, extension: .jpg, category: Images
2025-05-26 10:30:15,127 - INFO - Moved file: vacation_photo.jpg to /Users/username/Downloads/Images
```

### Common Issues and Solutions

**Issue**: "The specified directory does not exist"
- **Solution**: Check the path you entered for typos
- **Solution**: Use absolute paths (full path from root)

**Issue**: "The specified path is not a directory"
- **Solution**: Make sure you're pointing to a folder, not a file

**Issue**: Permission errors
- **Solution**: Ensure you have read/write permissions for the directory
- **Solution**: Run with appropriate privileges if needed

## Safety Features

### What Files Are Skipped

- **Hidden files**: Files starting with `.` (like `.DS_Store`, `.gitignore`)
- **Directories**: Only files are moved, subdirectories are left untouched

### What's Protected

- **Original files**: Files are moved (not copied), so no duplicates in original location
- **File integrity**: No file content is modified
- **Existing structure**: Subdirectories remain in place

## Best Practices

1. **Backup Important Data**: Always backup important files before running organization scripts
2. **Test on Small Directories**: Try the script on a test directory first
3. **Review Logs**: Check the log file after running to verify all operations
4. **Regular Cleanup**: Use the organizer regularly to maintain clean directories

## Advanced Usage Tips

- **Batch Processing**: You can run the script multiple times on different directories
- **Custom Categories**: Modify the `FILE_CATEGORIES` dictionary in the script to add your own file types
- **Automation**: Set up scheduled tasks to run the organizer automatically

## Support

If you encounter any issues:
1. Check the log file for detailed error messages
2. Verify directory permissions
3. Ensure file paths are correct
4. Review this user guide for common solutions
