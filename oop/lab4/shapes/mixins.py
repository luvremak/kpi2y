class CircleEndsMixin:
    def draw_circle_ends(self, canvas):
        r = 5
        canvas.create_oval(self.x1 - r, self.y1 - r, self.x1 + r, self.y1 + r,
                           fill='black', outline='black', width=2)
        canvas.create_oval(self.x2 - r, self.y2 - r, self.x2 + r, self.y2 + r,
                           fill='black', outline='black', width=2)

    def draw_circle_ends_rubber(self, canvas):
        r = 5
        ids = []
        ids.append(canvas.create_oval(self.x1 - r, self.y1 - r, self.x1 + r, self.y1 + r,
                                      outline='gray', fill='', dash=(4, 4), width=1))
        ids.append(canvas.create_oval(self.x2 - r, self.y2 - r, self.x2 + r, self.y2 + r,
                                      outline='gray', fill='', dash=(4, 4), width=1))
        return ids


class CubeFrameMixin:
    def draw_cube_frame(self, canvas, outline_color='black', width=2, fill=''):

        ids = []
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        w, h = abs(x2 - x1), abs(y2 - y1)
        depth = max(1, min(w, h) // 4)

        left, right = min(x1, x2), max(x1, x2)
        top, bottom = min(y1, y2), max(y1, y2)

        ids.append(canvas.create_rectangle(left, top, right, bottom,
                                           outline=outline_color, width=width, fill=fill))

        ids.append(canvas.create_rectangle(left + depth, top - depth, right + depth, bottom - depth,
                                           outline=outline_color, width=width, fill=''))

        ids.append(canvas.create_line(left, top, left + depth, top - depth, fill=outline_color, width=width))
        ids.append(canvas.create_line(right, top, right + depth, top - depth, fill=outline_color, width=width))
        ids.append(canvas.create_line(left, bottom, left + depth, bottom - depth, fill=outline_color, width=width))
        ids.append(canvas.create_line(right, bottom, right + depth, bottom - depth, fill=outline_color, width=width))

        return ids
