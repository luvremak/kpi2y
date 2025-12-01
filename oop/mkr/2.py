import numpy as np
import matplotlib.pyplot as plt

def generate_fractal(constant, res_x=800, res_y=800, depth=256):
    x_vals = np.linspace(-2, 2, res_x)
    y_vals = np.linspace(-2, 2, res_y)
    grid_x, grid_y = np.meshgrid(x_vals, y_vals)
    
    complex_plane = grid_x + 1j * grid_y
    iteration_map = np.zeros(complex_plane.shape, dtype=int)

    for step in range(depth):
        active = np.abs(complex_plane) < 2
        complex_plane[active] = complex_plane[active] ** 2 + constant
        iteration_map[active] += 1
    
    return iteration_map


def visualize_fractal(data, constant, size=(5, 5)):
    plt.figure(figsize=size)
    plt.title(f"Julia Set for C = {constant.real} + {constant.imag}i")
    plt.imshow(data, cmap="inferno")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    param = complex(-0.8, 0.156)
    fractal = generate_fractal(param)
    visualize_fractal(fractal, param)
