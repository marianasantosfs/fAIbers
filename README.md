
# Agricultural Sprinkler System Optimization Tool

## Overview

Efficient irrigation is a cornerstone of modern agriculture, directly impacting crop yield, resource conservation, and overall farm sustainability. However, the automation and optimization of agricultural irrigation systems remain significantly underexplored, leaving many farmers without adequate tools to maximize efficiency and minimize costs.

This project addresses this gap by providing a solution for planning and optimizing agricultural sprinkler systems. It calculates the optimal placement of sprinklers within a field based on user-defined parameters, such as field dimensions, obstacle coordinates, and desired irrigation precision. By tailoring the sprinkler configuration to the specific layout and needs of the field, the system ensures even water distribution and efficient resource usage.

The system also generates a comprehensive PDF report, offering:

- Recommendations on the types of sprinklers to use.  
- Precise locations for sprinkler installation.  
- Justifications for the chosen configuration.  
- An estimated cost for the entire sprinkler system.  

By automating complex calculations and consolidating insights into an actionable report, this tool simplifies the design process for farmers and agricultural planners. It empowers users to adopt irrigation systems that are both cost-effective and highly efficient, addressing a critical yet overlooked challenge in the agricultural sector.

---

## About the Project


This project was developed during a **hackathon** focused on creating innovative and impactful solutions by leveraging generative AI technology. We extend our heartfelt thanks to the **promoters of the event**, whose support was instrumental in bringing this project to fruition.

A special acknowledgment goes to **AWS (Amazon Web Services)** for providing the tools and resources that greatly enriched and enhanced the development process. Their robust infrastructure and cloud-based services were pivotal in ensuring the project's efficiency, scalability, and technical excellence.

---

## Features

- **Input Parameters**: Accepts field coordinates, obstacle and other objects coordinates, and intended irrigation precision.  
- **Optimal Placement Calculation**: Determines the best placement for sprinklers to ensure optimal water distribution across the field.  
- **PDF Report Generation**: Creates a professional report detailing the configuration and placement of the sprinkler system.  
- **Modular Design**: Includes separate modules for calculations, report generation, and execution, ensuring maintainability and scalability.  

---

## File Structure

1. **`mathematic_algorithm.py`**  
   Contains functions for calculating optimal sprinkler placement.  
   Key functionalities:  
   - Calculates field area.  
   - Determines optimal positions for sprinklers based on input parameters.  
   - Ensures no overlap between sprinkler coverage.  
   - Provides images of sprinkler positioning and coverage.  
   - Provides information of the the sytem.

2. **`report.py`**  
   The main entry point for the application.  
   Key functionalities:  
   - Collects input from the user.  
   - Executes the calculation of mathematic_algorithm.  
   - Requests and retrieves report information from the **LLaMA 3.1 70B Instruct model**.  
   - Outputs the final report in PDF format.  

---

## Installation

1. Clone or download the repository.  
2. Ensure Python 3.8 or higher is installed on your system.  
3. Install required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the Application**:  
   Execute the `main.py` script to start the program:  
   ```bash
   python main.py
   ```

2. **Provide Input Parameters**:  
   To configure and run the irrigation system, the following input parameters are required:

### - **Field Boundary Points**
   A list of tuples representing the boundary points of the field. Each tuple must contain two values: `(latitude, longitude)` in the EPSG:4326 coordinate system (WGS 84). The boundary points define the area to be irrigated.

   **Example:**
      ```python
      field_coordinates = [(40.32897891010581, -8.653877052022354), (40.32879283914316, -8.654454588726981), (40.32871683817989, -8.654719293049935), (40.328673596214294, -8.654879146959251), (40.328566146359954, -8.655171353054081), (40.328555374264695, -8.655347460383402), (40.32846503629598, -8.655627046067496), (40.32840434040056, -8.655762210033197), (40.32836340593132, -8.655858491213378),  (40.328280125383884, -8.655480772805728),
      (40.32830976762442, -8.655345608865737), (40.328380344335166, -8.654999366992056),
      (40.32850032457668, -8.654419828401345), (40.32860901237369, -8.653973602243287), (40.328704996258885, -8.653592180685843), (40.328875790774305, -8.653744008662159)]

### - **Obstacle Points**
   A list of dictionaries representing obstacles within the field. Each dictionary must contain the following keys:
    "format_type": A string that defines the shape of the obstacle. Only two values are accepted: "rectangle" or "circle".
    "coordinates": A tuple specifying the central point of the obstacle, formatted as (latitude, longitude).
    "radius": An integer specifying the radius of the obstacle (in meters). This value applies only for circular obstacles. For rectangular obstacles, set this value to None.
   
   **Example:**
      ```python
      obstacles = [
         {"format_type": "circle", "coordinates": (40.32850461030154, -8.654941160992928), "radius": 20},
         {"format_type": "rectangle", "coordinates":[(40.32864390701266, -8.654509663225632), (40.3287, -8.6552), (40.3292, -8.6552), (40.3292, -8.6547), (40.3287, -8.6547)], "radius": None}]

### - **Resolution**      
   Specify the level of precision required for the irrigation calculations. Higher precision will result in more detailed calculations and potentially longer processing times. Choose an appropriate level of precision based on the complexity of the field and the accuracy required for irrigation.

   Note: Increasing precision may extend the time required to process the data, so it is important to balance the desired accuracy with computational efficiency.
   
   **Example:**
         10

3. **View Output**:  
   The program generates a PDF report in the current directory, summarizing:  
   - Field details.  
   - Sprinkler placements.  
   - Efficiency metrics.  

---

## Example Output

After running the program, a sample output file, `irrigation_report.pdf`, is generated. This report includes:  
- Techonology explanation.
- A graphical representation of the field and sprinkler placements.  
- Key metrics, such as the total number of sprinklers required and coverage efficiency.  

---

# Future Enhancements

The system is continuously evolving, with several exciting features and integrations planned for future releases. Below are the key enhancements that are currently being explored:

## 1. **Meteorological Integration**
   - Integrate real-time weather data (such as precipitation, humidity, temperature, and wind speed) to optimize irrigation schedules and improve water usage efficiency.

## 2. **Advanced Valve Control**
   - Implement intelligent valve control to dynamically adjust water flow based on real-time field conditions and sensor inputs. This includes automatic adjustments for varying soil moisture levels and pressure fluctuations across the field.

## 3. **Sensor Integration**
   - Integrate a variety of sensors (e.g., soil moisture, temperature, pressure) to provide more granular control and monitoring. This will offer real-time feedback to optimize irrigation and detect potential issues proactively.

## 4. **Centralized Platform Development**
   - Develop a centralized platform that allows users to remotely monitor and control irrigation systems. The platform will feature a dashboard with live data, performance analytics, and automated alerts for maintenance or operational anomalies.

## 5. **Satellite Imagery for Obstacle Detection and Field Analysis**
   - Leverage satellite imagery to detect obstacles, identify changes in field conditions, and assess the overall field layout (e.g., detecting uneven terrain or large obstructions). This will enhance the system’s ability to adapt to field-specific challenges.

## 6. **Integration with GIS Tools for Complex Field Mapping**
   - Incorporate Geographic Information System (GIS) tools to support more complex field shapes and configurations, enabling precise mapping and management of irrigation systems, especially in non-rectangular fields or challenging terrains.

## 7. **Advanced Modeling for Terrain and Environmental Factors**
   - Implement advanced modeling techniques to account for factors such as uneven terrain, altitude variations, soil type, crop type, and water pressure dependencies. This will help optimize irrigation patterns and enhance resource efficiency.

## 8. **Cloud-Based Deployment for Real-Time Data Collection and Reporting**
   - Transition to a cloud-based deployment to facilitate real-time data collection and report sharing. Cloud integration will enable seamless data access, analytics, and collaboration among users and stakeholders, improving decision-making and reporting on irrigation performance.

These enhancements aim to create a more intelligent, efficient, and adaptable irrigation system that can better respond to dynamic environmental conditions, improve water usage efficiency, and maximize crop yield.

---