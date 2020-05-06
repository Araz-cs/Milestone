import json
import os
from pathlib import Path

path = Path('C:/Users/Araz/Desktop/121/Asg#3/DEV')
for subdir, dirs, files in os.walk(path):
    for filename in files:
        filepath = subdir + os.sep + filename

        if filepath.endswith(".json"):
            print (filepath)