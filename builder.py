from os import mkdir, rmdir, path
from pathlib import Path
from shutil import copyfile, rmtree
import subprocess

if __name__ == "__main__":
    if path.exists("./dist"):
        rmtree("./dist")
    if path.exists("./build"):
        rmtree("./build")
    subprocess.run(["pyinstaller", "-F", "ProjectTracker.py"])
    mkdir("./dist/ui")
    ui_folder = Path("./ui")
    for file in ui_folder.iterdir():
        if file.suffix == ".ui":
            copyfile(f"{file}", f".\\dist\\{file}")