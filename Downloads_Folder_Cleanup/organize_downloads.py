import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from pathlib import Path
import threading


class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer") #Add a title to application
        self.root.geometry("600x500") #Create GUI window size
    
    # Rest of the code remains the same
    extension_map = {
        # Images
        '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images',
        # Documents
        '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents',
        '.txt': 'Documents', '.rtf': 'Documents',
        # Audio
        '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio',
        # Video
        '.mp4': 'Video', '.avi': 'Video', '.mkv': 'Video',
        # Archives
        '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives',
        # Code
        '.py': 'Code', '.java': 'Code', '.cpp': 'Code', '.html': 'Code',
        '.css': 'Code', '.js': 'Code',
    }

    self.setup_gui()

    def setup_gui(self):
        # Path selection frame
        path_frame = ttk.LabelFrame(self.root, text="Select Folder", padding="10")
        path_frame.pack(fill="x", padx=10, pady=5)

        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_folder)
        browse_btn.pack(side="right")
        
        # Preview/Organize controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill="x", padx=10)

        preview_btn = ttk.Button(path_frame, text="Preview Changes", command=self.preview_changes)
        preview_btn.pack(side="left", padx=5)

        organize_btn = ttk.Button(path_frame, text="Organize Files", command=self.organize_files)
        organize_btn.pack(side="left", padx=5)

        # Preview area
        preview_frame = ttk.LabelFrame(self.root, text="Preview", padding="10")  
        preview_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Add scrollbar to preview area
        scroll = ttk.Scollbar(preview_frame)
        scroll.pack(side="right", fill="y")

        self.preview_text = tk.Text(preview_frame , wrap="word", yscrollcommand=scroll.set)
        self.preview_text.pack(fill="both", expand=True)
        scroll.config(command=self.preview_text.yview)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.root, variable=self.progress_var, mode='determinate')
        self.progress.pack(fill='x', padx=10, pady=5)

        # Status label
        self.status_var = tk.StringVar()
        status_label = ttk.Label(self.root, textvariable=self.status_var)
        status_label.pack(pady=5)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_var.set(folder_path)

    def get_planned_moves(self):
        downloads_path = self.path_var.get()
        if not downloads_path:
            messagebox.showerror("Error", "Please select a folder first!")
            return None
        
        downloads_dir = Path(downloads_path)
        if not downloads_dir.exists() or not downloads_dir.is_dir():
            messagebox.showerror("Error", "Invalid folder path!")
            return None

        # Process files
        planned_moves = {}
        total_files = 0

        for file in downloads_dir.iterdir():
            if file.is_file():  # Skip if it's a directory
                extension = file.suffix.lower()
                folder_name = self.extension_map.get(extension, 'Others')
                destination_folder = downloads_dir / folder_name

                new_filename = file.name
                if destination_folder.exists():
                    counter = 1
                    while (destination_folder / new_filename).exists():
                        base_name = file.stem
                        new_filename = f"{base_name}_{counter}{file.suffix}"
                        counter += 1

                    planned_moves.setdefault(folder_name, []).append((file.name, new_filename))
                    total_files += 1

        return planned_moves, total_files
    
    def preview_changes(self):
        self.preview_text.delete(1.0, tk.END)
        self.status_var.set("Generating preview...")

        result = self.get_planned_moves()
        if not result: 
            self.status_var.set("")
            return
        
        planned_moves, total_files = result

        preview_text = f"Found {total_files} files to organize:\n\n"
        for folder, files in planned_moves.items():
            preview_text += f"\n{folder} ({len(files)} files:\n)"
            for file, new_name in files:
                if file.name != new_name:
                    preview_text += f" - {file.name} -> {new_name}\n"
                else:
                    preview_text += f" - {file.name}\n"

        self.preview_text.insert(1.0, preview_text)
        self.status_var.set("Preview Generated")

    if preview_only:
        while True:
            response = input("\nWould you like to proceed with organizing the files? (yes/no): ").lower()
            if response in ['yes', 'no']:
                if response == 'yes':
                    print("\nExecuting file organization...")
                    organize_downloads(custom_path=custom_path, preview_only=False)
                else:
                    print("\nOperation cancelled. No files were moved.")
                break
            else:
                print("Please enter 'yes' or 'no'")

if __name__ == "__main__":
    # Example usage with custom path
    try:
        # You can replace this with your actual path. My downloads folder is on my B: drive.
        custom_downloads_path = "B:\Downloads"
        organize_downloads(custom_path=custom_downloads_path, preview_only=True)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}")