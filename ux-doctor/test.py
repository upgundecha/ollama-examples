import requests
import json
import io
import base64

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

# A function to perform the analysis 
# using the Ollama API 
def perform_ui_ux_analysis(page_name, image):
    prompt = f"""
        As a UI/UX expert, you are presented with a screenshot of {page_name} page. 
        Your task is to meticulously evaluate and provide detailed feedback. 
        Focus on aspects such as the overall user interface and 
        user experience design, alignment, layout precision, color schemes, and textual content. 
        Include constructive suggestions and potential enhancements in your critique. 
        Additionally, identify and report any discernible errors, defects, additional features, 
        or areas for improvement observed in the screenshot.
    """
    
    # Define the API endpoint
    api_endpoint = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'text/plain'}

    # Define the data payload with prompt and image
    data_payload = {
        "model": "llava",
        "prompt": prompt,
        "stream": False,
        "images": [base64_encoded_string]
    }

    # Send the POST request to the Ollama API endpoint 
    # running the llava model
    response = requests.post(api_endpoint, headers=headers, 
                             data=json.dumps(data_payload))
    
    # Assuming the API returns a JSON response
    response_data = response.json()

    # Generate the report
    generate_report(response_data, f"{page_name}_report.pdf", base64_encoded_string)

# A function to generate the PDF report
def generate_report(json_data, filename, base64_image):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    # Decode the base64 image data
    image_data = base64.b64decode(base64_image)

    # Resize the image (width, height)
    image = Image(io.BytesIO(image_data), width=400, height=200)
    story.append(image)

    # Get a sample stylesheet
    styles = getSampleStyleSheet()

    # Convert the single dictionary JSON data to a list of Paragraphs
    table_data = []
    for key, value in json_data.items():
        key_para = Paragraph(str(key), styles['Normal'])
        value_para = Paragraph(str(value), styles['Normal'])
        table_data.append([key_para, value_para])

    # Define column widths
    col_widths = [200, 300]  # Adjust as necessary

    # Create the table
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    # Add the table to the story
    story.append(table)

    # Build the PDF
    doc.build(story)

page_url = 'https://cookbook.seleniumacademy.com/bmicalculator.html'

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver as per your configuration
webdriver_service = Service(ChromeDriverManager().install())

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, 
                          options=chrome_options)
try:
    # Get page
    driver.get(page_url)

    # Get screenshot as base64
    base64_encoded_string = driver.get_screenshot_as_base64()
    perform_ui_ux_analysis("BMI Calculator", base64_encoded_string)
 
finally:
    # Close browser
    driver.quit()
