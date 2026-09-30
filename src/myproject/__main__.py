"""`python -m myproject`, and the entry point of the one-file executables."""
import sys

from myproject.cli import main       # absolute: PyInstaller runs this file as a script

if __name__ == "__main__":
    sys.exit(main())
