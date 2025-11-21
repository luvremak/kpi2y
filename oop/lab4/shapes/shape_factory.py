from .simple_shapes import PointShape, LineShape, RectShape, EllipseShape
from .complex_shapes import LineWithCircles, CubeFrame


class ShapeFactory:
    _map = {
        'point': PointShape,
        'line': LineShape,
        'rectangle': RectShape,
        'ellipse': EllipseShape,
        'line_circles': LineWithCircles,
        'cube': CubeFrame
    }

    @classmethod
    def create(cls, shape_type):
        shape_cls = cls._map.get(shape_type)
        if shape_cls is None:
            raise ValueError(f"Unknown shape type: {shape_type}")
        return shape_cls()
