from pathlib import Path
import os

folder = Path.home() / "Downloads"
folder_bin = Path.home() / "Kosz"

extension = [".exe", ".txt", ".py", ".jpg", ".jpeg", ".png", ".pdf", ".mp4", ".mp3", ".zip", '.html', ".htm"]

ext_to_folder = {
    ".exe": "Exe Files",
    ".txt": "Txt Files",
    ".py": "Python Files",
    ".jpg": "Images",
    ".png": "Images",
    ".jpeg": "Images",
    ".pdf": "Pdf Files",
    ".mp3": "Music",
    ".mp4": "Videos",
    ".zip": "Zip Dirs",
    ".html": "Websites",
    ".htm": "Websites"
}

files_by_ext = {ext: [] for ext in extension}

for file in folder.iterdir():
    if file.is_file:
        ext = file.suffix.lower()

        if ext in extension:
            files_by_ext[ext].append(file)

# We create folders and move files to the appropriate folders in Downloads
for ext, files in files_by_ext.items():
    # Pliki do kosza
    if ext in [".otf", ".ttf"]:
        target_folder = folder_bin
    
    else:
        folder_name = ext_to_folder.get(ext, "Inne")
        target_folder = folder / folder_name

    target_folder.mkdir(exist_ok=True)

    for file in files:
        file.rename(target_folder / file.name)

print(files_by_ext)