class CircleEndsMixin:
    def draw_circle_ends(self, canvas):
        r = 5
        canvas.create_oval(self.x1-r, self.y1-r, self.x1+r, self.y1+r,
                           fill='white', outline='black', width=2)
        canvas.create_oval(self.x2-r, self.y2-r, self.x2+r, self.y2+r,
                           fill='white', outline='black', width=2)

class CubeFrameMixin:
    def draw_cube_frame(self, canvas):
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        w, h = abs(x2 - x1), abs(y2 - y1)
        depth = min(w, h) // 3

        canvas.create_rectangle(x1, y1, x2, y2, outline='black', width=2)
        canvas.create_rectangle(x1+depth, y1-depth, x2+depth, y2-depth,
                                outline='black', width=2)

        for (dx1, dy1, dx2, dy2) in [
            (x1, y1, x1+depth, y1-depth),
            (x2, y1, x2+depth, y1-depth),
            (x1, y2, x1+depth, y2-depth),
            (x2, y2, x2+depth, y2-depth)
        ]:
            canvas.create_line(dx1, dy1, dx2, dy2, fill='black', width=2)
