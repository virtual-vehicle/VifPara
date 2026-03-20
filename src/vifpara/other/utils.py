from ..logging import logger
from . import Vector3
from typing import Tuple

def is_valid_extension(extension_name: str, valid_file_extensions: list) -> bool:
    """
    Checks if the given file extension is inside a valid extension list.
    """
    valid_file: bool = False
    for extension in valid_file_extensions:
        if extension_name == extension:
            valid_file = True
    if not valid_file:
        extension_string: str = " ".join(valid_file_extensions)
        logger.error(f"Unknown file extension provided <{extension_name}>. Please use one of the following: {extension_string}")
    return valid_file


def intersect_vector_bounding_box(vector_origin: Vector3, vector_direction: Vector3,
                                  box_corners: tuple) -> Tuple[Vector3, Vector3]:
    """
    Computes the intersections of an infinite vector (direction and origin) with the bounding box of a case.
    box corners must be a tuple in the following format: (x_min, x_max, y_min, y_max, z_min, z_max)
    """
    x_min, x_max, y_min, y_max, z_min, z_max = box_corners
    norm_direction = vector_direction.normalized()

    t_vals = []
    for c, d, min_b, max_b in zip(vector_origin.to_list(), norm_direction.to_list(), [x_min, y_min, z_min],
                                  [x_max, y_max, z_max]):
        if abs(d) < 1e-8:
            t_vals.append((float('-inf'), float('inf')))
        else:
            t1 = (min_b - c) / d
            t2 = (max_b - c) / d
            t_vals.append((min(t1, t2), max(t1, t2)))

    t_min = max(t[0] for t in t_vals)
    t_max = min(t[1] for t in t_vals)

    entry_point = vector_origin + norm_direction * t_min
    exit_point = vector_origin + norm_direction * t_max

    return entry_point, exit_point