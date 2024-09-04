import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsl(r, g, b):
    r /= 255
    g /= 255
    b /= 255
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    h, s, l = 0, 0, (max_val + min_val) / 2

    if max_val == min_val:
        h = s = 0
    else:
        d = max_val - min_val
        s = d / (2 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)
        if max_val == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_val == g:
            h = (b - r) / d + 2
        elif max_val == b:
            h = (r - g) / d + 4
        h /= 6

    return int(h * 360), int(s * 100), int(l * 100)

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[1]
    if color_code:
        rgb_value = hex_to_rgb(color_code)
        hsl_value = rgb_to_hsl(*rgb_value)
        rgb_label.config(text=f"RGB: {rgb_value}")
        hsl_label.config(text=f"HSL: {hsl_value}")

# Создание окна
root = tk.Tk()
root.minsize(500, 500)
root.maxsize(1000, 600)
root.title("Color Converter")

# Кнопка для выбора цвета
color_button = tk.Button(root, text="Choose Color", command=choose_color)
color_button.columnconfigure(0, weight=1)
color_button.rowconfigure(0, weight=1)
color_button.grid(column=0, row=0)

# Метки для отображения результатов
rgb_label = tk.Label(root, text="RGB:")
rgb_label.grid(row=1, column=0, pady=5)
scale_button = ttk.Scale(root)
scale_button.grid(row=1, column=1, padx=50, pady=5)
hsl_label = tk.Label(root, text="HSL:")
hsl_label.grid(row=2, column=0, pady=5)

root.mainloop()
