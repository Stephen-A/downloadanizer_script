import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from pathlib import Path
import threading
import logging
from datetime import datetime


class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer") #Add a title to application
        self.root.geometry("600x500") #Create GUI window size
    
        #setup logging
        self.setup_logging()

        self.extension_map = {
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

    def setup_logging(self):
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Setup logging with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"file_organizer_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

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
        scroll = ttk.Scrollbar(preview_frame)
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

    def execute_moves(self, planned_moves, total_files):
        downloads_path = Path(self.path_var.get())
        files_processed = 0

        try:
            for folder, files in planned_moves.items():
                folder_path = downloads_path / folder
                
                # Create folder if it doesn't exist
                try:
                    folder_path.mkdir(exist_ok=True)
                    self.logger.info(f"Created or verified folder: {folder_path}")
                except Exception as e:
                    self.logger.error(f"Error creating folder {folder_path}: {str(e)}")
                    raise
                
                for file_path, new_name in files:
                    try:
                        # Log the attempt
                        self.logger.info(f"Attempting to move: {file_path} to {folder_path / new_name}")
                        
                        # Check if source file exists
                        if not file_path.name.exists():
                            self.logger.error(f"Source file not found: {file_path}")
                            messagebox.showwarning(
                                "File Not Found", 
                                f"Could not find file: {file_path}\nSkipping this file."
                            )
                            continue
                        
                        # Check if destination folder exists and is writable
                        if not folder_path.name.exists():
                            self.logger.error(f"Destination folder not found: {folder_path}")
                            raise FileNotFoundError(f"Destination folder not found: {folder_path}")
                        
                        # Create full destination path
                        destination = folder_path / new_name
                        
                        # Perform the move
                        shutil.move(str(file_path), str(destination))
                        self.logger.info(f"Successfully moved file to: {destination}")
                        
                        files_processed += 1
                        progress = (files_processed / total_files) * 100
                        self.progress_var.set(progress)
                        self.status_var.set(f"Processed {files_processed} of {total_files} files...")
                        
                    except Exception as e:
                        self.logger.error(f"Error moving file {file_path}: {str(e)}")
                        messagebox.showwarning(
                            "Error Moving File", 
                            f"Error moving {file_path}\nError: {str(e)}\nSkipping this file."
                        )
                        continue

            if files_processed > 0:
                self.status_var.set("Organization complete!")
                messagebox.showinfo("Success", f"Successfully organized {files_processed} files!")
            else:
                self.status_var.set("No files were organized")
                messagebox.showwarning("Warning", "No files were successfully organized")
            
        except Exception as e:
            self.logger.error(f"Critical error during organization: {str(e)}")
            self.status_var.set("Error during organization!")
            messagebox.showerror("Error", f"A critical error occurred: {str(e)}")    

    def set_manual_path(self):
        path = self.path_var.get()
        if path:
            path = Path(path)
            if self.verify_path(path):
                self.path_var.set(str(path))
                self.preview_changes()
            else:
                messagebox.showerror("Error", f"Cannot access path: {path}")

    def browse_folder(self):
        folder_path = filedialog.askdirectory(initialdir="B:/")  # Start in B: drive
        if folder_path:
            if self.verify_path(folder_path):
                self.path_var.set(folder_path)
                self.preview_changes()
            else:
                messagebox.showerror("Error", f"Cannot access path: {folder_path}" )

    def get_planned_moves(self):
        downloads_path = self.path_var.get()
        if not downloads_path:
            messagebox.showerror("Error", "Please select a folder first!")
            return None
        
        try:
            downloads_dir = Path(downloads_path)
            # Add debug information
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, f"Checking path: {downloads_dir}\n")
            self.preview_text.insert(tk.END, f"Path exists: {downloads_dir.exists()}\n")
            self.preview_text.insert(tk.END, f"Is directory: {downloads_dir.is_dir()}\n\n")

            if not downloads_dir.exists() or not downloads_dir.is_dir():
                messagebox.showerror("Error", f"Invalid folder path: {downloads_dir}")
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
        
        except Exception as e:
            self.preview_text.insert(tk.END, f"Error occurred: {str(e)}\n")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return None
        
    def preview_changes(self):
        self.preview_text.delete(1.0, tk.END)
        self.status_var.set("Generating preview...")
        
        result = self.get_planned_moves()
        if not result:
            self.status_var.set("No files found or error occurred")
            return

        planned_moves, total_files = result
        
        preview_text = f"Found {total_files} files to organize:\n\n"
        for folder, files in planned_moves.items():
            preview_text += f"\n{folder} ({len(files)} files):\n"
            for original, new_name in files:
                if original != new_name:
                    preview_text += f"  - {original} -> {new_name}\n"
                else:
                    preview_text += f"  - {original}\n"

        self.preview_text.insert(1.0, preview_text)
        self.status_var.set("Preview generated")

    def organize_files(self):
        result = self.get_planned_moves()
        if not result:
            return
        
        planned_moves, total_files = result

        if messagebox.askyesno("Confirm", "Are you sure you want to organize these files?"):
            self.progress_var.set(0)
            self.status_var.set("Organizing files...")

            thread = threading.Thread(target=self.execute_moves, args=(planned_moves, total_files))
            thread.start()

    def verify_path(self, path):
        """Verify that a path exists and is accessible"""
        try:
            path = Path(path)
            if not path.exists():
                self.logger.error(f"Path does not exist: {path}")
                return False
            # Try to list contents to verify permissions
            list(path.iterdir())
            return True
        except Exception as e:
            self.logger.error(f"Error verifying path {path}: {str(e)}")
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()