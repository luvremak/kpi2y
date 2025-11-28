from typing import Callable, List, Optional


class ShapeManager:

    def __init__(self, max_shapes: int):
        self._shapes = []
        self._selected_index: Optional[int] = None
        self._shape_change_listeners: List[Callable[[], None]] = []
        self._selection_listeners: List[Callable[[int], None]] = []
        self.MAX_SHAPES = max_shapes

    @property
    def shapes(self):
        return self._shapes

    @property
    def selected_index(self):
        return self._selected_index

    def add_shape(self, shape) -> bool:
        if len(self._shapes) >= self.MAX_SHAPES:
            return False
        self._shapes.append(shape)
        self._notify_shape_change()
        return True

    def delete_shape(self, index: int):
        if 0 <= index < len(self._shapes):
            del self._shapes[index]
            if self._selected_index is not None:
                if self._selected_index == index:
                    self._selected_index = None
                elif self._selected_index > index:
                    self._selected_index -= 1
            self._notify_shape_change()

    def clear_all(self):
        self._shapes.clear()
        self._selected_index = None
        self._notify_shape_change()

    def set_selected(self, index: int):
        if 0 <= index < len(self._shapes):
            self._selected_index = index
        else:
            self._selected_index = None
        self._notify_selection_change(self._selected_index if self._selected_index is not None else -1)

    def add_shape_change_listener(self, callback: Callable[[], None]):
        if callback not in self._shape_change_listeners:
            self._shape_change_listeners.append(callback)

    def remove_shape_change_listener(self, callback: Callable[[], None]):
        if callback in self._shape_change_listeners:
            self._shape_change_listeners.remove(callback)

    def add_selection_listener(self, callback: Callable[[int], None]):
        if callback not in self._selection_listeners:
            self._selection_listeners.append(callback)

    def remove_selection_listener(self, callback: Callable[[int], None]):
        if callback in self._selection_listeners:
            self._selection_listeners.remove(callback)

    def _notify_shape_change(self):
        for cb in list(self._shape_change_listeners):
            try:
                cb()
            except Exception:
                pass

    def _notify_selection_change(self, index: int):
        for cb in list(self._selection_listeners):
            try:
                cb(index)
            except Exception:
                pass
