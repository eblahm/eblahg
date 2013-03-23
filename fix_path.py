import os
import sys

app_root = os.path.abspath(os.path.dirname(__file__))

def fix():
    # credit:  Nick Johnson of Google
    sys.path.insert(0, app_root)
    sys.path.append(os.path.join(app_root, 'externals'))