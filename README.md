# Proxy Card Grid PDF Generator

This script generates a PDF containing resized images arranged in a grid format. It uses the Waifu2x image upscaling tool to resize images and the ReportLab library to create the PDF.

## Requirements

Before running the script, ensure you have the following dependencies installed:

- Python 3.x
- Pillow
- ReportLab
- waifu2x-ncnn-py

You can install the necessary Python packages using pip:
```bash
pip install Pillow reportlab waifu2x-ncnn-py
```

## Usage
### Place Images:
Place the images you want to resize and include in the PDF in the same directory as the script.
Supported formats are .png, .jpg, and .jpeg.

### Run the Script:
Execute the script from your terminal or command prompt:

```bash
python CardGrid.py
```
# Output PDF:
Upon successful execution, a PDF named output.pdf will be generated in the same directory.
The images will be arranged in a grid format, with each image displayed three times.
