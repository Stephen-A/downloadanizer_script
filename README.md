# File Organizer

![image](https://github.com/user-attachments/assets/4483257a-db7a-41d0-b9fb-016c5ec5e8ad)![image](https://github.com/user-attachments/assets/db80762b-826b-4a3a-a809-0f20429cfef6)![image](https://github.com/user-attachments/assets/5fd26e64-9f89-4191-8985-4e342d55c0a2)

A Python-based GUI application to organize files in a folder by categorizing them into subfolders based on their file types. Built with tkinter for the GUI and shutil for file operations.
---
## Features
+ File Categorization: Automatically sorts files into folders like Images, Documents, Audio, Video, Archives, and more.

+ Customizable Categories: Easily extend or modify the file extension mappings.

+ Preview Changes: Preview how files will be organized before executing the move.

+ Progress Tracking: Real-time progress bar and status updates during file organization.

+ Logging: Detailed logs for debugging and tracking file operations.

+ Cross-Platform: Works on Windows, macOS, and Linux.
---
## Screenshots
Screenshot 1
Main Interface of the File Organizer

Screenshot 2
Preview of File Organization
---
## Installation
### Prerequisites
+ Python 3.x
+ tkinter (usually comes pre-installed with Python)

## Steps
1. Clone the repository:

```bash
git clone https://github.com/your-username/file-organizer.git
2. Navigate to the project directory:
```
```bash
cd file-organizer
3. Run the script:
```
```bash
python file_organizer.py
```
## Usage
1. Launch the application.

2. Select the folder you want to organize using the Browse button.

3. Click Preview Changes to see how files will be organized.

4. Click Organize Files to execute the organization process.

5. Check the logs for detailed information about the operations.

6. Customization
You can customize the file extension mappings in the extension_map dictionary in the script. For example:

python
Copy
self.extension_map = {
    '.jpg': 'Images',
    '.pdf': 'Documents',
    # Add more mappings as needed
}
Contributing
Contributions are welcome! If you'd like to contribute:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeatureName).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeatureName).

Open a pull request.

License
