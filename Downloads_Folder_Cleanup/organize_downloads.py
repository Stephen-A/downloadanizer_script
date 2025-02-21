import os
import shutil
from pathlib import Path
import datetime

def organize_downloads(custom_path=None, preview_only=True):
    # Get the downloads folder path
    if custom_path:
        downloads_path = Path(custom_path)
    else:
        downloads_path = Path.home() / "Downloads"
    
    # Verify the path exists
    if not downloads_path.exists():
        raise FileNotFoundError(f"The path {downloads_path} does not exist!")
    
    if not downloads_path.is_dir():
        raise NotADirectoryError(f"The path {downloads_path} is not a directory!")
    
    # Convert to string for compatibility with os.path functions
    downloads_path = str(downloads_path)
    
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

    def get_folder_name(file):
        """Determine the folder name based on file extension"""
        extension = file.suffix.lower()
        return extension_map.get(extension, 'Others')

    def create_folder(folder_path):
        """Create folder if it doesn't exist"""
        if not os.path.exists(folder_path) and not preview_only:
            os.makedirs(folder_path)

    def get_destination_filename(file, folder_name):
        """Generate the destination filename, handling potential conflicts"""
        destination_folder = os.path.join(downloads_path, folder_name)
        filename = file.name
        base_name = file.stem
        extension = file.suffix
        counter = 1
        
        while os.path.exists(os.path.join(destination_folder, filename)):
            filename = f"{base_name}_{counter}{extension}"
            counter += 1
            
        return filename, os.path.join(destination_folder, filename)

    def move_file(file, folder_name):
        """Move file to appropriate folder"""
        source = str(file)
        destination_folder = os.path.join(downloads_path, folder_name)
        create_folder(destination_folder)
        
        filename, destination = get_destination_filename(file, folder_name)
        
        if not preview_only:
            shutil.move(source, destination)
        
        return filename

    # Process files
    planned_moves = {}
    downloads_dir = Path(downloads_path)

    print(f"{'Previewing' if preview_only else 'Organizing'} files in: {downloads_path}")
    
    for file in downloads_dir.iterdir():
        if file.is_file():  # Skip if it's a directory
            folder_name = get_folder_name(file)
            try:
                new_filename = move_file(file, folder_name)
                planned_moves.setdefault(folder_name, []).append((file.name, new_filename))
            except Exception as e:
                print(f"Error processing {file.name}: {str(e)}")

    # Print summary
    print("\nPlanned File Organization:")
    total_files = sum(len(files) for files in planned_moves.values())
    print(f"\nTotal files to be organized: {total_files}")
    
    for folder, files in planned_moves.items():
        print(f"\n{folder} ({len(files)} files):")
        for original, new in files:
            if original != new:
                print(f"  - {original} -> {new}")
            else:
                print(f"  - {original}")

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