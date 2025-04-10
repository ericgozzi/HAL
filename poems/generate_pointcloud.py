# r: compas

from compas.geometry import Point, Line, Curve
from compas_rhino.conversions import box_to_rhino, point_to_rhino, point_to_compas



def remove_duplicate_points(point_cloud):
    # A canvas of stars, waiting to shine bright
    new_point_cloud = []
    # For each star in the sky, let it find its place,
    # But only if it’s unique, not a duplicate trace
    [new_point_cloud.append(x) for x in point_cloud if x not in new_point_cloud]
    # Return the constellation, where only true stars remain in sight
    return new_point_cloud




def check_cell_distance(cell, point_cloud, dimension):
     # The heart of the cell, a center of light in the vast space
    cell_center_point = cell.draw_box().frame.point
    # For each point, like a wandering star in the night,
    # Measure the distance to the cell’s center, seeking a connection of light
    for point in point_cloud:
        if point.distance_to_point(cell_center_point) < dimension:
             # If the star is near, return the cell, a shared space they both embrace
            return cell




def get_interesting_cells(point_cloud, cells):   
    # A home for the intriguing, a place where something special resides
    interesting_cells = []
    # The dimensions, defining the size of the house on all axes
    dimension_x = cells[0].draw_box().xsize
    dimensinon_y = cells[0].draw_box().ysize
    dimensinon_z = cells[0].draw_box().zsize
    # Gather all dimensions and select the largest, like choosing the grandest house
    dimensions = [dimension_x, dimensinon_y, dimensinon_z]
    dimension = max(dimensions)   
    # For each cell, check if it can house something meaningful
    for cell in cells:
        # Check if this house can shelter a point from the cloud, close enough to notice
        checked_cell = check_cell_distance(cell, point_cloud, dimension)
        # If the house can indeed shelter something valuable, mark it as interesting
        if checked_cell != None:
            interesting_cells.append(checked_cell)
    # Return the list of houses where something meaningful can dwell
    return interesting_cells
