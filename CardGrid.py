import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from waifu2x_ncnn_py import Waifu2x
import tempfile

def waifu2x_resize(input_image, scale=2):
    """Resize image using Waifu2x."""
    waifu2x = Waifu2x(gpuid=0, scale=scale, noise=3)  # Adjust noise level as needed
    with Image.open(input_image) as image:
        image = waifu2x.process_pil(image)
    return image

def generate_pdf(output_pdf):
    """Generate a PDF containing resized images arranged in a grid."""
    # Use the current working directory as the images directory
    images_dir = os.getcwd()
    
    # Settings for the PDF
    card_width, card_height = 2.5 * inch, 3.5 * inch  # 2.5 x 3.5 inches per card
    card_margin = 0.05 * inch  # Margin between cards
    margin_x, margin_y = 0.5 * inch, 0.05 * inch  # Reduced top margin
    page_width, page_height = letter  # 8.5 x 11 inches
    
    # List all image files in the directory
    image_files = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Ensure we have images
    if len(image_files) == 0:
        raise ValueError("No images found in the current directory.")
    
    temp_image_files = []
    
    # Resize images and save them to temporary files
    for img_file in image_files:
        # Resize the image using waifu2x
        output_image = waifu2x_resize(img_file, scale=2)  # Change scale as needed
        
        # Save the resized image to a temporary file once
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
            output_image.save(tmpfile, format="PNG")
            temp_image_files.append(tmpfile.name)  # Store the temp file name
        
        # Duplicate the reference three times in a list for usage in the PDF
        temp_image_files.extend([tmpfile.name] * 2)  # Add it twice more for a total of three references

    # Create a PDF canvas with explicit page size of 8.5 x 11 inches
    pdf_canvas = canvas.Canvas(output_pdf, pagesize=letter)
    
    # Determine how many images can fit in one page
    images_per_page = 9  # 3 rows * 3 columns
    total_images = len(temp_image_files)

    for index in range(total_images):
        if index % images_per_page == 0 and index > 0:
            # Create a new page for every 9 images
            pdf_canvas.showPage()  # Move to the next page

        row = (index % images_per_page) // 3  # 3 images per row
        col = (index % images_per_page) % 3   # 3 images per column

        # Positioning for each grid cell in the row with margin
        x = margin_x + col * (card_width + card_margin)
        y = page_height - margin_y - (row + 1) * (card_height + card_margin)

        # Draw the image from the temporary file
        pdf_canvas.drawInlineImage(temp_image_files[index], x, y, width=card_width - card_margin, height=card_height - card_margin)

    # Save the PDF file
    pdf_canvas.save()

    # Clean up temporary image files
    for temp_file in temp_image_files:
        os.remove(temp_file)  # Remove the temporary file after use

# Define the output PDF file name
output_pdf = 'output.pdf'

# Generate the PDF
generate_pdf(output_pdf)
print("PDF generated successfully!")
