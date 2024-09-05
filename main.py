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
        CMYK_value = hex_to_rgb(color_code)
        LAB_value = rgb_to_hsl(*CMYK_value)
        CMYK_label.config(text=f"RGB: {CMYK_value}")
        LAB_label.config(text=f"HSL: {LAB_value}")

# Создание окна
root = tk.Tk()
root.minsize(500, 500)
root.maxsize(1000, 600)
root.title("Color Converter")

# Настройка сетки для центрирования
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)

# Кнопка для выбора цвета
color_button = tk.Button(root, text="Choose Color", command=choose_color)
color_button.grid(row=0, column=0, columnspan=3, padx=5, pady=100)

# Метка для CMYK
CMYK_label = tk.Label(root, text="CMYK:")
CMYK_label.grid(row=1, column=0, pady=5, sticky='e')

# Ввод текста для CMYK
CMYK_entry = tk.Entry(root)
CMYK_entry.insert(0, "0, 0, 0")
CMYK_entry.grid(row=1, column=1, pady=5, padx=(0, 5), sticky='w')

# Ползунок для CMYK
scale_button_CMYK = ttk.Scale(root)
scale_button_CMYK.grid(row=1, column=2, padx=50, pady=5, sticky='w')

# Метка для LAB
LAB_label = tk.Label(root, text="LAB:")
LAB_label.grid(row=2, column=0, pady=5, sticky='e')

# Ввод текста для LAB
LAB_entry = tk.Entry(root)
LAB_entry.insert(0, "0, 0, 0")
LAB_entry.grid(row=2, column=1, pady=5, padx=(0, 5), sticky='w')

# Ползунок для LAB
scale_button_LAB = ttk.Scale(root)
scale_button_LAB.grid(row=2, column=2, padx=50, pady=5, sticky='w')

# Метка для HSV
HSV_label = tk.Label(root, text="HSV:")
HSV_label.grid(row=3, column=0, pady=5, sticky='e')

# Ввод текста для HSV
HSV_entry = tk.Entry(root)
HSV_entry.insert(0, "0, 0, 0")
HSV_entry.grid(row=3, column=1, pady=5, padx=(0, 5), sticky='w')

# Ползунок для HSV
scale_button_HSV = ttk.Scale(root)
scale_button_HSV.grid(row=3, column=2, padx=50, pady=5, sticky='w')

root.mainloop()
