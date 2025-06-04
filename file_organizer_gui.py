#!/usr/bin/env python3
"""
File Organizer GUI - A simple graphical interface for organizing files
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
import os
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
import logging

# Import the core functionality from the command-line version
from file_organizer import (
    FILE_CATEGORIES, 
    get_file_category, 
    get_destination_folder_name,
    create_destination_directory,
    get_unique_filename,
    should_skip_file,
    setup_logging
)


class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("800x600")
        
        # Variables
        self.selected_directory = tk.StringVar()
        self.organization_stats = {}
        self.files_to_organize = {}
        self.is_organizing = False
        
        # Setup logging
        setup_logging()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="File Organizer", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Directory selection section
        dir_frame = ttk.LabelFrame(main_frame, text="Select Directory to Organize")
        dir_frame.pack(fill='x', pady=(0, 15))
        
        dir_inner = ttk.Frame(dir_frame)
        dir_inner.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(dir_inner, text="Directory:").pack(side='left')
        
        self.dir_entry = ttk.Entry(dir_inner, textvariable=self.selected_directory, state='readonly')
        self.dir_entry.pack(side='left', fill='x', expand=True, padx=(10, 10))
        
        self.browse_button = ttk.Button(dir_inner, text="Browse", 
                                       command=self.browse_directory)
        self.browse_button.pack(side='left', padx=(5, 0))
        
        self.scan_button = ttk.Button(dir_inner, text="Scan Files", 
                                     command=self.scan_files, 
                                     state='disabled')
        self.scan_button.pack(side='left', padx=(10, 0))
        
        # Preview section
        preview_frame = ttk.LabelFrame(main_frame, text="Preview - Files to be Organized")
        preview_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Treeview for file preview
        tree_container = ttk.Frame(preview_frame)
        tree_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(tree_container, 
                                columns=('count', 'size'), 
                                show='tree headings', 
                                height=10)
        self.tree.heading('#0', text='Category / File')
        self.tree.heading('count', text='Count')
        self.tree.heading('size', text='Total Size')
        
        self.tree.column('#0', width=300)
        self.tree.column('count', width=80, anchor='center')
        self.tree.column('size', width=100, anchor='center')
        
        # Scrollbars for treeview
        tree_scroll_y = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        tree_scroll_x = ttk.Scrollbar(tree_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        tree_scroll_y.pack(side='right', fill='y')
        tree_scroll_x.pack(side='bottom', fill='x')
        
        # Control buttons section
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(0, 15))
        
        self.organize_button = ttk.Button(
            button_frame, 
            text="Organize Files", 
            command=self.start_organization,
            state='disabled'
        )
        self.organize_button.pack(side='left', padx=(0, 15))
        
        self.clear_button = ttk.Button(button_frame, 
                                      text="Clear", 
                                      command=self.clear_preview)
        self.clear_button.pack(side='left')
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress")
        progress_frame.pack(fill='x', pady=(0, 15))
        
        progress_inner = ttk.Frame(progress_frame)
        progress_inner.pack(fill='x', padx=10, pady=10)
        
        self.progress_var = tk.StringVar(value="Ready to organize files...")
        self.progress_label = ttk.Label(progress_inner, textvariable=self.progress_var)
        self.progress_label.pack(anchor='w')
        
        self.progress_bar = ttk.Progressbar(progress_inner, 
                                           length=400, 
                                           mode='determinate')
        self.progress_bar.pack(fill='x', pady=(5, 0))
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results")
        results_frame.pack(fill='x')
        
        results_inner = ttk.Frame(results_frame)
        results_inner.pack(fill='x', padx=10, pady=10)
        
        self.results_text = tk.Text(results_inner, 
                                   height=6, 
                                   wrap=tk.WORD, 
                                   state='disabled')
        results_scroll = ttk.Scrollbar(results_inner, orient='vertical', command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scroll.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        results_scroll.pack(side='right', fill='y')
        
    def browse_directory(self):
        """Open directory browser dialog."""
        directory = filedialog.askdirectory(
            title="Select Directory to Organize",
            initialdir=os.path.expanduser("~")
        )
        if directory:
            self.selected_directory.set(directory)
            self.scan_button.config(state='normal')
            self.clear_preview()
            
    def scan_files(self):
        """Scan the selected directory and preview files to be organized."""
        directory = self.selected_directory.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory first.")
            return
            
        try:
            self.progress_var.set("Scanning files...")
            self.progress_bar.config(mode='indeterminate')
            self.progress_bar.start()
            
            # Clear previous results
            self.tree.delete(*self.tree.get_children())
            self.files_to_organize.clear()
            
            # Scan files in a separate thread to keep UI responsive
            threading.Thread(target=self._scan_files_thread, args=(directory,), daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scan directory: {str(e)}")
            self.progress_bar.stop()
            self.progress_bar.config(mode='determinate')
            self.progress_var.set("Ready to organize files...")
            
    def _scan_files_thread(self, directory):
        """Scan files in a separate thread."""
        try:
            source_dir = Path(directory)
            file_groups = defaultdict(list)
            total_files = 0
            
            # Group files by category
            for file_path in source_dir.iterdir():
                if file_path.is_file() and not should_skip_file(file_path):
                    extension = file_path.suffix.lower()
                    category = get_file_category(extension)
                    if category == 'Others':
                        category = f"{extension[1:].upper()} Files" if extension else "Unknown"
                    
                    file_info = {
                        'path': file_path,
                        'name': file_path.name,
                        'size': file_path.stat().st_size,
                        'extension': extension,
                        'destination_folder': get_destination_folder_name(extension)
                    }
                    
                    file_groups[category].append(file_info)
                    total_files += 1
            
            self.files_to_organize = file_groups
            
            # Update UI in main thread
            self.root.after(0, self._update_preview, file_groups, total_files)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to scan files: {str(e)}"))
            self.root.after(0, self._reset_progress)
            
    def _update_preview(self, file_groups, total_files):
        """Update the preview tree with scanned files."""
        self.progress_bar.stop()
        self.progress_bar.config(mode='determinate')
        
        if not file_groups:
            self.progress_var.set("No files found to organize.")
            messagebox.showinfo("Info", "No files found that need organizing in the selected directory.")
            return
            
        # Populate tree
        for category, files in sorted(file_groups.items()):
            total_size = sum(f['size'] for f in files)
            size_str = self._format_size(total_size)
            
            # Insert category node
            category_node = self.tree.insert('', 'end', text=category, values=(len(files), size_str))
            
            # Add files under category (limit to first 50 for performance)
            for i, file_info in enumerate(files[:50]):
                file_size_str = self._format_size(file_info['size'])
                file_text = file_info['name']
                if i == 49 and len(files) > 50:
                    file_text = f"... and {len(files) - 50} more files"
                    
                self.tree.insert(category_node, 'end', text=file_text, values=('', file_size_str))
        
        self.progress_var.set(f"Found {total_files} files to organize in {len(file_groups)} categories.")
        self.organize_button.config(state='normal')
        
        # Expand all categories
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
            
    def _reset_progress(self):
        """Reset progress indicators."""
        self.progress_bar.stop()
        self.progress_bar.config(mode='determinate')
        self.progress_var.set("Ready to organize files...")
        
    def clear_preview(self):
        """Clear the preview and reset UI."""
        self.tree.delete(*self.tree.get_children())
        self.files_to_organize.clear()
        self.organize_button.config(state='disabled')
        self.progress_var.set("Ready to organize files...")
        self.progress_bar['value'] = 0
        
        # Clear results
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state='disabled')
        
    def start_organization(self):
        """Start the file organization process."""
        if self.is_organizing:
            return
            
        if not self.files_to_organize:
            messagebox.showerror("Error", "No files to organize. Please scan a directory first.")
            return
            
        # Confirm organization
        total_files = sum(len(files) for files in self.files_to_organize.values())
        if not messagebox.askyesno(
            "Confirm Organization", 
            f"This will organize {total_files} files. Continue?"
        ):
            return
            
        self.is_organizing = True
        self.organize_button.config(state='disabled')
        self.scan_button.config(state='disabled')
        self.browse_button.config(state='disabled')
        
        # Start organization in separate thread
        threading.Thread(target=self._organize_files_thread, daemon=True).start()
        
    def _organize_files_thread(self):
        """Organize files in a separate thread."""
        try:
            source_dir = Path(self.selected_directory.get())
            total_files = sum(len(files) for files in self.files_to_organize.values())
            processed_files = 0
            stats = defaultdict(int)
            errors = []
            
            for category, files in self.files_to_organize.items():
                for file_info in files:
                    try:
                        # Update progress
                        progress = (processed_files / total_files) * 100
                        self.root.after(0, lambda p=progress: self.progress_bar.config(value=p))
                        self.root.after(0, lambda f=file_info['name']: 
                                      self.progress_var.set(f"Organizing: {f}"))
                        
                        # Create destination directory
                        dest_folder = get_destination_folder_name(file_info['extension'])
                        dest_dir = create_destination_directory(source_dir, dest_folder)
                        
                        if dest_dir:
                            # Get unique filename
                            unique_name = get_unique_filename(dest_dir, file_info['name'])
                            dest_path = dest_dir / unique_name
                            
                            # Move file
                            file_info['path'].rename(dest_path)
                            stats[dest_folder] += 1
                            
                            # Log the move
                            logging.info(f"Moved {file_info['name']} to {dest_folder}/{unique_name}")
                        else:
                            errors.append(f"Failed to create directory for {file_info['name']}")
                            
                    except Exception as e:
                        error_msg = f"Error moving {file_info['name']}: {str(e)}"
                        errors.append(error_msg)
                        logging.error(error_msg)
                        
                    processed_files += 1
            
            # Update UI with results
            self.root.after(0, self._show_results, stats, errors, total_files)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Organization failed: {str(e)}"))
        finally:
            self.root.after(0, self._finish_organization)
            
    def _show_results(self, stats, errors, total_files):
        """Display organization results."""
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        
        # Summary
        successful = sum(stats.values())
        failed = len(errors)
        
        results = f"Organization Complete!\n"
        results += f"Total files processed: {total_files}\n"
        results += f"Successfully organized: {successful}\n"
        results += f"Failed: {failed}\n\n"
        
        # Folder breakdown
        if stats:
            results += "Files organized by folder:\n"
            for folder, count in sorted(stats.items()):
                results += f"  {folder}: {count} files\n"
        
        # Errors
        if errors:
            results += f"\nErrors ({len(errors)}):\n"
            for error in errors[:10]:  # Show first 10 errors
                results += f"  {error}\n"
            if len(errors) > 10:
                results += f"  ... and {len(errors) - 10} more errors\n"
        
        self.results_text.insert(1.0, results)
        self.results_text.config(state='disabled')
        
        # Show completion message
        if failed == 0:
            messagebox.showinfo("Success!", f"Successfully organized {successful} files!")
        else:
            messagebox.showwarning(
                "Completed with Errors", 
                f"Organized {successful} files successfully.\n{failed} files had errors."
            )
            
    def _finish_organization(self):
        """Reset UI after organization is complete."""
        self.is_organizing = False
        self.progress_var.set("Organization complete!")
        self.progress_bar['value'] = 100
        
        # Re-enable buttons
        self.organize_button.config(state='disabled')  # Disable until new scan
        self.scan_button.config(state='normal')
        self.browse_button.config(state='normal')
        
        # Clear preview since files have been moved
        self.tree.delete(*self.tree.get_children())
        self.files_to_organize.clear()
        
    @staticmethod
    def _format_size(size_bytes):
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
