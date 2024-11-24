from pdf2image import convert_from_path
import os

# Convert first page to image
images = convert_from_path('The Cycle.jpg', first_page=1, last_page=1)
first_page = images[0]

# Create static directory if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')

# Save the image
first_page.save('static/book-cover.jpg', 'JPEG')
