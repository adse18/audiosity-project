#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess

def main():
    """Run administrative tasks."""

    # Execute the BAT file in a new console with changed directory
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audiosity_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # start image generator
    subprocess.Popen(['cmd', '/k', f'cd .\model_webui\ & .\webui.bat'])
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
