import os
import urllib.request
import subprocess

# Get package details from user input
name = input("Enter package name: ")
description = input("Enter package description: ")
author = os.getlogin()  # Use system username as author name
author_email = input("Enter author email: ")
packages = input("Enter package names (comma-separated): ").split(",")

# Set package version
version = "1.0.0"

# Create package directory and subdirectories
os.mkdir(name)
os.chdir(name)
os.mkdir("src")

# Create __init__.py file in src directory
with open("src/__init__.py", "w", encoding="utf_8") as f:
    f.write("")

# Create README file
with open("README.md", "w", encoding="utf_8") as f:
    f.write(f"# {name}\n\n{description}")

# Download .gitignore file from GitHub repository
url = "https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore"
with urllib.request.urlopen(url) as response:
    with open(".gitignore", "w", encoding="utf_8") as f:
        f.write(response.read().decode())

# Create requirements.txt file
with open("requirements.txt", "w", encoding="utf_8") as f:
    for package in packages:
        f.write(package.strip())
        f.write("\n")
    f.write("-e .")

# Create setup.py file
with open("setup.py", "w", encoding="utf_8") as f:
    f.write(f"""from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace('\\n',"") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name='{name}',
    version='{version}',
    description='{description}',
    author='{author}',
    author_email='{author_email}',
    packages=find_packages('src'),
    package_dir={{'': 'src'}},
    install_requires=get_requirements('requirements.txt')
)
""")

# Git init
os.system("git init")
os.system("git add .")
os.system(f'git commit -m "Initilize the {name}"')
os.system("git branch -M main")

# Create virtual environment and activate it
subprocess.run(["python3", "-m", "venv", ".venv"])
if os.name == "nt":
    activate_script = os.path.join(".venv", "Scripts", "activate.bat")
else:
    activate_script = os.path.join(".venv", "bin", "activate")
subprocess.run(["source", activate_script], shell=True)

# Install all package from requirements.txt
subprocess.run(["pip", "install", "-r", "requirements.txt"])

# Open Code with the package
open_code = input("Do you want to open the code (Y/N): ")
if open_code.upper().startswith("Y"):
    code_path = subprocess.check_output("which code", shell=True).strip().decode('utf-8')
    subprocess.run([code_path, name], shell=True)
    print("VS code is opening....")

# Done
print("Package created successfully!")
