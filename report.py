import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import os
import logging
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, ListFlowable, ListItem
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from mathematic_algorithm import IrrigationSystem

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def configure_aws_credentials():
    os.environ['AWS_ACCESS_KEY_ID'] ="ASIAR7JTVSWO3ZJ3ISSB"
    os.environ['AWS_SECRET_ACCESS_KEY'] = "3BuRZjKBolYjBYETy+z2hZYXVkSTlexOZckZNzNy"
    os.environ['AWS_DEFAULT_REGION'] = "us-west-2"
    os.environ['AWS_SESSION_TOKEN']="IQoJb3JpZ2luX2VjEFMaCXVzLWVhc3QtMSJHMEUCIEYD9BFBSso0DkSygr213GzATRh1cRWlmemfmUA0PDQPAiEArts2o1VWSbWl2jeXGrnKAOhc1zPfNoxCR0/AULpwLuUqogII6///////////ARACGgwxMzU5MzY3MTAwNDUiDOmyj64YKpUr8Qk5hCr2AZfzCvwxwOFlrhkw2765wLfIKxd1qSYryXnOzzu8G+r+DJ0bWlfXkZ2eADh4npCmwhVb44MLKC9RDh4Ha0g96VNNTE5Jraya4Yc6JDTt4vBEyVSz3B6o5tAmc5M45tCNs0aDL3mUvFqpHvJ1YAF8bAnwGYT9JmOWGUjnZoRFssuKSuaX8xXqmqHS3qPmu3xHaLllD1sTxG9cg0EZJwNBg10ULa81UCpyTRaUYD+5WToBC8brrao6OsvZGnQrOcd63nAorDZbchoncKoHvp1TkB6R7x7tE77cY6Io7oj/aJRUftsloWPEmfYilmc27oMPAq8qYZgs7DDo+Yu6BjqdAeWLmD7s0xOy6fnTlYuERG4ywUa5bxWI5bSW4LMzgR8pa4hUzKSHg8F2R2GZ+piBy1VmHtLcXDwfFcEaMjKmaxq0y0JCH+I0H2nnl80V7CVvefjcknmelBCUUpxu09zMj3Jtz2C2OKWWwRHKY54wK8xoMYEmvZZ8QOqkT75WN2ABe/eE2H5k7MeV5pAG1MKd7OIQVMcmeLXduzynSJo="

def create_bedrock_client():
    try:
        client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_DEFAULT_REGION", "us-west-2"))
        logging.info("Successfully created Bedrock client.")
        return client
    except Exception as e:
        logging.error(f"Error creating Bedrock client: {e}")
        raise

def generate_user_message(farm_name, area, obstacles, total_sprinklers, area_covered, type_sprinklers, radius_types):
    return f"""I am working on a project that involves the installation\
                of an irrigation system for an agricultural field. 
                Please generate a  report for the irrigation system design, to present to the farmer (client of the product),
                stating the following information:

                Technology Explanation: 
                Make a text (cientific) introducing the water problem in the agriculture field with numbers and percentage of water lost.
                And add why is important to install intelligent systems in this. And why this sytem is importar, since in an intellegence way creates
                the plannification for the irrigation system of a specific field in minutes. Giving to the farmer an intellegent way to project the system
                in order to reduce overleap irrigation, reduce obstacles irrigation,  reduce irrigate points outside of the field and give the farmer the choice
                to choose the resolution that the system must have. Since better resolution gives higher budget.
                
                Sprinkler vailable Details:
                Make a text about how the technology can implement different types of sprinklers. This HAVE to have explain this information:
                -Sprinkler Types of the technology(bullet list):
                Large Commercial Sprinkler-> This sprinkler type has a minimum radius of 10 meters, a maximum radius of 40 meters, and increases in increments of 5 meters. 
                Impact Sprinkler-> The impact sprinkler has a minimum radius of 5 meters and a maximum radius of 30 meters, with a step size of 2 meters. 
                Rotor Sprinkler-> The rotor sprinkler has a minimum radius of 4 meters and a maximum radius of 18 meters, with a step size of 1 meter. 
                Fixed Spray Sprinkler-> This sprinkler type has a minimum radius of 1 meter, a maximum radius of 5 meters, and increases in increments of 0.5 meters. 
                Micro Sprinkler-> The micro sprinkler has a minimum radius of 0.5 meters and a maximum radius of 3 meters, with a step size of 0.1 meters. 

                Field Overview:

                -Hectare Area(m2): {area} 
                -Obstacles Area (m2): {obstacles}
                -Total number of sprinklers: {total_sprinklers} 
                -Sprinklers Area Covered (m2): {area_covered}
                -Number of type of sprinkler used: {type_sprinklers}  Give only the number of types of sprinklers
                -Type of sprinklers used: {type_sprinklers} Give the text - normal text- with the type of sprinklers with nothing more added
                -Number of different types of radius: {radius_types}
                -Type of radius used (m): {radius_types} Give the text - normal text- with the type of radius with nothing more added

               

                End the text with Budget Prediction Table and Water Use Prediction:
                Do the budget in detail, with the detail how much cost each sprinkler use, the total cost in a  table. 
                How much water each sprinkler use per hour, the total water used per type of sprinkler in one hour and the total water used in one hour 
                of the system this information add this to the budget table.
                Each table header cell must not have more than 10 characters. 
                The header content should be also written in regular text. DO NOT use BOLD in table
                When you use gallons use 

                The report should:
                Clearly describe the proposed layout, using simple and clear language suitable for someone in the agriculture field.
                Specify where the sprinklers should be installed and what type should be used.

                Output the report in a professional tone but simple for a farmer or agricultural worker to understand easily.

                I want it to start with information of the cover that will be like the following example:
                    FAIbers,
                    2024
                - Format the output cleanly and make it ready to be saved as a document file.
                - Ensure the response is styled and formatted for direct conversion into a Word or PDF file.
                - THE TEXT MUST BE WITH THE PROPER SPACES, BULLED LIST, NEGRIT SETENCES, WORDS, WITHOUT LOOKING TO RAW
                """   

def invoke_model(client, model_id, user_message):
    conversation = [{"role": "user", "content": [{"text": user_message}]}]

    try:
        response = client.converse(
            modelId= model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 2048, "stopSequences": ["\n\nHuman:"], "temperature": 0, "topP": 1}
        )
        return response["output"]["message"]["content"][0]["text"]
    
    except ClientError as e:
        logging.error(f"Error invoking model: {e}")
        raise
    except Exception as e:
        logging.error(f"General error: {e}")
        raise


def adjust_table_column_widths(table_data, max_width):
    """
    Adjust the column widths to ensure the table fits within the page width.
    :param table_data: Data of the table (list of rows).
    :param max_width: Maximum width for the table.
    :return: List of column widths adjusted proportionally.
    """
    col_count = len(table_data[0])
    col_max_lengths = [0] * col_count
    
    # Calculate the maximum length for each column
    for row in table_data:
        for col_idx, cell in enumerate(row):
            # Check the length of the content in the current cell
            col_max_lengths[col_idx] = max(col_max_lengths[col_idx], len(cell))
    
    # Now adjust the column widths proportionally based on content length
    total_length = sum(col_max_lengths)  # Sum of all maximum content lengths
    scale_factor = max_width / total_length if total_length > 0 else 1  # Scale to fit within max width
    
    # Adjust column widths proportionally
    col_widths = [(max_length+1) * scale_factor for max_length in col_max_lengths]
    return col_widths

def create_pdf_from_dynamic_text(filename, content):
    """
    Generate a formatted PDF dynamically based on provided content,
    including paragraphs, tables, and images (graphs).

    :param filename: Name of the output PDF file.
    :param content: Text from the AWS model, containing markup (e.g., **bold**, *italic*, etc.).
    """

    styles = getSampleStyleSheet()

    custom_styles = {
        "CustomTitle": ParagraphStyle(
            name="CustomTitle", fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=20
        ),
        "CustomHeading": ParagraphStyle(
            name="CustomHeading", fontSize=14, leading=18, spaceAfter=10, fontName="Helvetica-Bold"
        ),
        "CustomNormal": ParagraphStyle(
            name="CustomNormal", fontSize=11, leading=14, spaceAfter=5
        ),
        "CustomBullet": ParagraphStyle(
            name="CustomBullet", fontSize=11, leading=14, leftIndent=20, bulletIndent=10
        ),
                "CustomGraphTitle": ParagraphStyle(
            name="CustomGraphTitle", fontSize=12, leading=14, alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=10
        )
    }

    # Parse and format content
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # Split the input content into paragraphs and handle tables
    lines = content.splitlines()
    
    table_data = []
    table_started = False

    for line in lines:
        line = line.strip()  # Trim extra spaces
        if not line:
            continue  # Skip empty lines
        elif line.startswith("|") and "|" in line:  # Detect table rows
            # Handle table parsing
            if not table_started:
                # Start table processing by parsing headers
                table_data = [line.split("|")[1:-1]]  # Get headers
                table_started = True
            else:
                table_data.append(line.split("|")[1:-1])  # Add table rows
        else:
            # If it's not part of the table, treat it as a normal paragraph
            if line.startswith("**") and line.endswith("**"):  # Bold text (e.g., title or heading)
                elements.append(Paragraph(line.strip("**"), custom_styles["CustomHeading"]))
            elif line.startswith("*") and ":" in line:  # Key-value style
                elements.append(Paragraph(line.strip("*"), custom_styles["CustomNormal"]))
            elif line.startswith("*"):  # Bullet list
                elements.append(ListFlowable(
                    [ListItem(Paragraph(line.strip("* "), custom_styles["CustomBullet"]))],
                    bulletType="bullet"
                ))
            else:  # Regular text
                elements.append(Paragraph(line, custom_styles["CustomNormal"]))

            # Add spacing between paragraphs
            elements.append(Spacer(1, 10))

    # Add the table to the PDF if any table data exists
    if table_started:
        # Adjust column widths to fit within the page
        max_table_width = letter[0] - 100  # Max width of the table (account for margins)
        col_widths = adjust_table_column_widths(table_data, max_table_width)

        # Create the table
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center all cell content
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header row
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Add space below the header
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Normal font for other rows
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),  # Padding for content rows
        ]))
        elements.append(table)

        # Add spacing after the table
        elements.append(Spacer(1, 20))

    # Add images from the project directory to the PDF
    project_dir = os.getcwd()
    png_files = [f for f in os.listdir(project_dir) if f.endswith(".png")]
    if png_files:
        for file_name in png_files:
            image_path = os.path.join(project_dir, file_name)
            
            # Add some space before the image
            elements.append(Spacer(1, 12))

            try:
                img = Image(image_path, width=400, height=300) 
                elements.append(img)
                            # Add image title
                elements.append(Paragraph(f"Graph: {file_name.replace('_', ' ').replace('.png', '')}", 
                                        custom_styles["CustomGraphTitle"]))
                elements.append(Spacer(1, 6))  
            except Exception as e:
                logging.error(f"Error adding image {file_name}: {e}")
                continue

    # Generate the PDF
    doc.build(elements)

    # Remove the file after adding it to the PDF
    try:
        if png_files:
            for file_name in png_files:
                image_path = os.path.join(project_dir, file_name)
                os.remove(image_path)
                logging.info(f"Removed image: {image_path}")
    except Exception as e:
        logging.error(f"Error removing image {image_path}: {e}")
 
def run_project(field_coordinates, obstacles, resolution):
    configure_aws_credentials()
    client = create_bedrock_client()

    model_id = "meta.llama3-1-70b-instruct-v1:0"
    filename = "irrigation_report.pdf"

    irrigation_system = IrrigationSystem()

    sprinklers, field_points_utm, obstacles_utm, obstacles_total_area, total_sprinkler_area = irrigation_system.sprinklers_distribution(field_coordinates, obstacles, resolution)
    irrigation_system.plot_field(field_coordinates, sprinklers, obstacles_utm, "field_plot.png")
    irrigation_system.plot_sprinkler_coverage_by_type(field_coordinates, sprinklers)

    # Input parameters
    farm_name = "Farmer"
    area = field_points_utm.area
    obstacles = obstacles_total_area
    total_sprinkles = len(sprinklers)
    area_covered = total_sprinkler_area
    sprinkler_types = set(sprinkler["type"] for sprinkler in sprinklers)
    radius_types = set(sprinkler["radius"] for sprinkler in sprinklers)

    # Generate Report
    user_message = generate_user_message(farm_name, area, obstacles, total_sprinkles, area_covered, sprinkler_types, radius_types)
    report_text = invoke_model(client, model_id, user_message)
    create_pdf_from_dynamic_text(filename, report_text)

    logging.info("Report successfully generated.")


