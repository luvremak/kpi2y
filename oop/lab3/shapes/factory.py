from .point import Point
from .line import Line
from .rectangle import Rectangle
from .ellipse import Ellipse
from .star import Star

class ShapeFactory:
    SHAPE_MAP = {
        'point': Point,
        'line': Line,
        'rectangle': Rectangle,
        'ellipse': Ellipse,
        'star': Star
    }

    @classmethod
    def create_shape(cls, shape_type, x, y):
        shape_class = cls.SHAPE_MAP.get(shape_type)
        if not shape_class:
            raise ValueError(f"Unknown shape type: {shape_type}")
        if shape_type == 'ellipse':
            return shape_class(x, y)
        else:
            return shape_class(x, y)
