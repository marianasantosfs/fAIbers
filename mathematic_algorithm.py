import logging
from shapely.geometry import Polygon, Point
from shapely.ops import transform
from pyproj import Transformer
import numpy as np
import matplotlib.pyplot as plt
import math

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

class IrrigationSystem:
    def __init__(self, crs_from="EPSG:4326", crs_to="EPSG:32629"):
        """
        Initializes the irrigation system with the provided coordinate reference systems.
        :param crs_from: CRS for input coordinates (default is WGS84)
        :param crs_to: CRS for output coordinates (default is UTM)
        """
        try:
            self.transformer = Transformer.from_crs(crs_from, crs_to, always_xy=True)
            logging.info(f"Coordinate transformer initialized from {crs_from} to {crs_to}.")
        except Exception as e:
            logging.error(f"Error transforming coordinates: {e}")
            raise

    def transform_coordinates(self, coordinates):
        """
        Transforms a list of coordinates from one CRS to another.
        :param coordinates: List of coordinates (x, y)
        :return: Transformed coordinates
        """
        try:
            transformed_coords = [transform(self.transformer.transform, Point(coord)) for coord in coordinates]
            logging.info(f"Transformed {len(coordinates)} coordinates.")
            return transformed_coords
        except Exception as e:
            logging.error(f"Error in transforming coordinates: {e}")
            raise

    def grade_adjustment(self, field_points_utm, resolution):
        """
        Adjusts the grid of sprinkler positions based on the field boundaries.
        :param field_points_utm: UTM transformed field boundary coordinates
        :param resolution: Grid resolution for sprinkler placement
        :return: List of valid points for sprinkler placement
        """
        try:
            center_x = (field_points_utm.bounds[0] + field_points_utm.bounds[2]) / 2
            center_y = (field_points_utm.bounds[1] + field_points_utm.bounds[3]) / 2

            grade = []
            for x in np.arange(center_x - (field_points_utm.bounds[2] - field_points_utm.bounds[0]) / 2,
                               center_x + (field_points_utm.bounds[2] - field_points_utm.bounds[0]) / 2, resolution):
                for y in np.arange(center_y - (field_points_utm.bounds[3] - field_points_utm.bounds[1]) / 2,
                                   center_y + (field_points_utm.bounds[3] - field_points_utm.bounds[1]) / 2, resolution):
                    point = Point(x, y)
                    if field_points_utm.contains(point):  # Check if the point is within the field boundaries
                        grade.append((x, y))
            return grade
        except Exception as e:
            logging.error(f"Error in grade adjustment: {e}")
            raise

    def sprinkler_sobreposition(self, point, radius, sprinklers_positions, field_utm, obstacles_utm):
        """
        Checks if a sprinkler placement overlaps with the field or any other sprinklers/obstacles.
        :param point: Point of sprinkler placement
        :param radius: Radius of the sprinkler
        :param sprinklers_positions: List of existing sprinkler positions
        :param field_utm: The field boundary in UTM coordinates
        :param obstacles_utm: List of obstacles in the field
        :return: True if there is a conflict, False otherwise
        """
        try:
            sprinkler_area = Point(point).buffer(radius)
            if not field_utm.contains(sprinkler_area):
                return True

            # Check for overlap with existing sprinklers
            for sprinkler in sprinklers_positions:
                if sprinkler_area.intersects(sprinkler["circle"]):
                    return True

            # Check for overlap with obstacles
            for obstacle in obstacles_utm:
                if sprinkler_area.intersects(obstacle["coordinates"]):
                    return True

            return False
        except Exception as e:
            logging.error(f"Error in sprinkler overposition check: {e}")
            raise

            
    def obstacles_transform(self, obstacles):
        """
        Transforms obstacles from one CRS to another.
        :param obstacles: List of obstacles in field (circle or rectangle)
        :return: List of transformed obstacles
        """
        obstacles_coordinates_transformed = []
        total_area = 0.0 
        try:
            for obstacle in obstacles:
                if obstacle["format_type"] == "circle":
                    transformed_center = transform(self.transformer.transform, Point(obstacle["coordinates"])).coords[0]
                    radius = obstacle["radius"]
                    obstacles_coordinates_transformed.append({"format_type": "circle", "coordinates": Point(transformed_center).buffer(radius), "radius": radius})
                    total_area += math.pi * (radius ** 2)

                elif obstacle["format_type"] == "rectangle":
                    if len(obstacle["coordinates"]) < 4:
                        logging.error(f"Rectangle obstacle must have at least 4 coordinates, got {len(obstacle['coordinates'])}.")
                        raise ValueError(f"Rectangle obstacle must have at least 4 coordinates.")
                    transformed_coords = [transform(self.transformer.transform, Point(c)).coords[0] for c in obstacle["coordinates"]]
                    transformed_polygon = Polygon(transformed_coords)
                    obstacles_coordinates_transformed.append({"format_type": "rectangle", "coordinates": transformed_polygon})
                    total_area += transformed_polygon.area

            return obstacles_coordinates_transformed, total_area
        except Exception as e:
            logging.error(f"Error in transforming obstacles: {e}")
            raise

    def sprinklers_distribution(self, field_coordinates, obstacles, resolution):
        """
        Distributes sprinklers across the field, checking for overlaps with obstacles and other sprinklers.
        :param field_coordinates: List of field boundary coordinates
        :param obstacles: List of dict with the obstacles in the field
        :param resolution: Grid resolution for sprinkler placement
        :return: List of dict with information of sprinkler positions, types and specification
        """
        if len(field_coordinates) < 4:
            logging.error("Field coordinates must have at least 4 points to form a valid polygon.")
            raise ValueError("Field coordinates must have at least 4 points.")
        try:
            sprinklers_positions = []
            total_sprinkler_area = 0
            field_points_utm = Polygon(self.transform_coordinates(field_coordinates))
            grade = self.grade_adjustment(field_points_utm, resolution)
            obstacles_utm, obstacles_total_area = self.obstacles_transform(obstacles) if obstacles else []

            for point in grade:
                for sprinkler_type, radius_list in {
                    "large_commercial": np.arange(10, 41, 5),
                    "impact": np.arange(5, 31, 2),
                    "rotor": np.arange(4, 19, 1),
                    "fixed_spray": np.arange(1, 5.6, 0.5),
                    "micro": np.arange(0.5, 3.1, 0.1)
                }.items():
                    radius_list = [round(radius, 1) for radius in radius_list]
                    radius_list = sorted(radius_list, reverse=True)  # Sort by the largest radius first
                    for radius in radius_list:
                        if not self.sprinkler_sobreposition(point, radius, sprinklers_positions, field_points_utm, obstacles_utm):
                            sprinkler_point = Point(point).buffer(radius)
                            sprinklers_positions.append({
                                "type": sprinkler_type,
                                "radius": radius,
                                "position": point,
                                "circle": sprinkler_point
                            })
                            total_sprinkler_area += math.pi * (radius ** 2)

            logging.info(f"Distributed {len(sprinklers_positions)} sprinklers.")
            return sprinklers_positions, field_points_utm, obstacles_utm, obstacles_total_area, total_sprinkler_area
        except Exception as e:
            logging.error(f"Error in sprinkler distribution: {e}")
            raise
            
    def plot_field(self, field_coordinates, sprinklers_positions, obstacles_utm, save_path):
        """
        Plots a map showing the field, sprinklers, and obstacles (circles or rectangles).
        
        :param field_utm: Shapely Polygon representing the field boundaries in UTM coordinates.
        :param sprinklers_positions: List of dicts containing sprinkler positions, types, and radii.
        :param obstacles: List of dicts containing obstacles, which can be either rectangles or circles.
        """
        try:
            fig, ax = plt.subplots(figsize=(10, 10))

            field_points_utm = Polygon(self.transform_coordinates(field_coordinates))
            x, y = field_points_utm.exterior.xy
            ax.fill(x, y, alpha=0.2, color="green", label="Field")
            added_labels = set()

            # Plotando os obstáculos
            for obstacle in obstacles_utm:
                label = None
                if obstacle["format_type"] == "rectangle":
                    label = "Obstacle (Retangle)"
                    ox, oy = obstacle["coordinates"].exterior.xy
                    ax.fill(ox, oy, alpha=0.4, color="red", label=label if label not in added_labels else None)
                elif obstacle["format_type"] == "circle":
                    label = "Obstacle (Circle)"
                    ox, oy = obstacle["coordinates"].exterior.xy
                    ax.fill(ox, oy, alpha=0.4, color="orange", label=label if label not in added_labels else None)
                if label:
                    added_labels.add(label)

            for sprinkler in sprinklers_positions:
                point = sprinkler["position"] 
                radius = sprinkler["radius"]
                circle = Point(point).buffer(radius)
                circle_x, circle_y = circle.exterior.xy
                ax.fill(circle_x, circle_y, color="blue", alpha=0.3, label="Sprinkler Coverage" if "Sprinkler Coverage" not in added_labels else None)
                ax.plot(point[0], point[1], 'ro', label="Sprinkler Position" if "Sprinkler Position" not in added_labels else None)
                added_labels.add("Sprinkler Coverage")
                added_labels.add("Sprinkler Position")

            ax.set_title("Irrigation System Map")
            ax.set_xlabel("Longitude (m)")
            ax.set_ylabel("Latitude (m)")
            ax.legend()

            plt.savefig(save_path)
            logging.info(f"Field plot saved as {save_path}")

        except Exception as e:
            logging.critical(f"Critical error: {e}")

    def plot_sprinkler_coverage_by_type(self, field_coordinates, sprinklers_positions):
        """
        Plots separate maps showing the sprinkler coverage for each type of sprinkler.
        
        :param field_coordinates: List of field boundary coordinates (latitude, longitude)
        :param sprinklers_positions: List of sprinklers with position, type, and radius
        """

        sprinkler_types = set(sprinkler["type"] for sprinkler in sprinklers_positions)
        added_labels = set()

        for sprinkler_type in sprinkler_types:
            save_path = f"{sprinkler_type}_coverage.png"
            fig, ax = plt.subplots(figsize=(10, 10))
            color_map = plt.cm.get_cmap("tab20")
            field_points_utm = Polygon(self.transform_coordinates(field_coordinates))
            x, y = field_points_utm.exterior.xy
            ax.fill(x, y, alpha=0.2, color="green", label="Field")

            type_sprinklers = [sprinkler for sprinkler in sprinklers_positions if sprinkler["type"] == sprinkler_type]

            for i, sprinkler in enumerate(type_sprinklers):
                point = sprinkler["position"]
                radius = sprinkler["radius"]
                
                circle = Point(point).buffer(radius)
                circle_x, circle_y = circle.exterior.xy
                label = f"Radius: {radius}m"
                if radius not in added_labels:
                    color = color_map(i / 20)
                    ax.fill(circle_x, circle_y, color=color, alpha=0.5, label=label) if label not in added_labels else None
                    added_labels.add(radius)
                else:
                    ax.fill(circle_x, circle_y, color=color, alpha=0.5)

            ax.set_title(f"Sprinkler Coverage: {sprinkler_type.capitalize()}")
            ax.set_xlabel("Longitude (m)")
            ax.set_ylabel("Latitude (m)")
            ax.legend(loc='best')
            plt.savefig(save_path)
