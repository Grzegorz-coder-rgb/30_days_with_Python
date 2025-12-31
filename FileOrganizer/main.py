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

for plik in folder.iterdir():
    if plik.is_file:
        ext = plik.suffix.lower()

        if ext in extension:
            files_by_ext[ext].append(plik)

# Tworzymy foldery i przenosimy pliki do odpowiednich folderów w Downloads
for ext, pliki in files_by_ext.items():
    # Pliki do kosza
    if ext in [".otf", ".ttf"]:
        folder_docelowy = folder_bin
    
    else:
        folder_name = ext_to_folder.get(ext, "Inne")
        folder_docelowy = folder / folder_name

    folder_docelowy.mkdir(exist_ok=True)

    for plik in pliki:
        plik.rename(folder_docelowy / plik.name)

print(files_by_ext)