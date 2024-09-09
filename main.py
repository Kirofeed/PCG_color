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
        cmyk_value = hex_to_rgb(color_code)
        LAB_value = rgb_to_hsl(*cmyk_value)
        CMYK_label.config(text=f"RGB: {cmyk_value}")
        # LAB_label.config(text=f"HSL: {LAB_value}")

# Создание функции реагирования
def process_colors(n):
    for ind in range(4):
        CMYK_values[ind] = (cmyk_scales[ind].get())
        print(CMYK_values[ind], end=' ')
    print()
    for ind in range(3):
        LAB_values[ind] = lab_scales[ind].get()
        print(LAB_values[ind], end=' ')
    print()
    for ind in range(3):
        HSV_values[ind] = hsv_scales[ind].get()
        print(HSV_values[ind], end=' ')
    CMYK_entry.delete(0, tk.END)
    CMYK_entry.insert(0, f'{round(CMYK_values[0], 2)}, ' + f'{round(CMYK_values[1], 2)}, ' +
                      f'{round(CMYK_values[2], 2)}, ' + f'{round(CMYK_values[3], 2)}')
    LAB_entry.delete(0, tk.END)
    LAB_entry.insert(0, f'{round(LAB_values[0], 2)}, ' + f'{round(LAB_values[1], 2)}, ' + f'{round(LAB_values[2], 2)}')
    HSV_entry.delete(0, tk.END)
    HSV_entry.insert(0, f'{round(HSV_values[0], 2)}, ' + f'{round(HSV_values[1], 2)}, ' + f'{round(HSV_values[2], 2)}')


# Создание окна
root = tk.Tk()
# root.minsize(500, 500)
# root.maxsize(1000, 600)
root.title("Color Converter")

CMYK_values = [0.0, 0.0, 0.0, 0.0]
LAB_values = [0.0, 0.0, 0.0]
HSV_values = [0.0, 0.0, 0.0]

# Создание фреймов
CMYK_frame = tk.Frame(root, bd=5, relief="solid", highlightbackground="red", highlightthickness=2)
LAB_frame = tk.Frame(root, bd=5, relief="solid", highlightbackground="red", highlightthickness=2)
HSV_frame = tk.Frame(root, bd=5, relief="solid", highlightbackground="red", highlightthickness=2)

CMYK_frame.columnconfigure(0, weight=1)
CMYK_frame.columnconfigure(1, weight=1)
CMYK_frame.rowconfigure(0, weight=1)
CMYK_frame.rowconfigure(1, weight=1)
CMYK_frame.rowconfigure(2, weight=1)
CMYK_frame.rowconfigure(3, weight=1)
CMYK_frame.grid(row=1, column=0)

LAB_frame.columnconfigure(0, weight=1)
LAB_frame.columnconfigure(1, weight=1)
LAB_frame.rowconfigure(0, weight=1)
LAB_frame.rowconfigure(1, weight=1)
LAB_frame.rowconfigure(2, weight=1)
LAB_frame.grid(row=2, column=0)

HSV_frame.columnconfigure(0, weight=1)
HSV_frame.columnconfigure(1, weight=1)
HSV_frame.rowconfigure(0, weight=1)
HSV_frame.rowconfigure(1, weight=1)
HSV_frame.rowconfigure(2, weight=1)
HSV_frame.grid(row=3, column=0)

# Настройка сетки для центрирования
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)

# Кнопка для выбора цвета
color_button = tk.Button(root, text="Choose Color", command=choose_color)
color_button.grid(row=0, column=0, columnspan=1, padx=5, pady=100)
# Метка для CMYK
CMYK_label = tk.Label(CMYK_frame, text="CMYK:")
CMYK_label.grid(row=0, column=0, pady=(10, 5))

# Ввод текста для CMYKf
CMYK_entry = tk.Entry(CMYK_frame)
CMYK_entry.insert(0, f'{CMYK_values[0]}, ' + f'{CMYK_values[1]}, ' +
                  f'{CMYK_values[2]}' + f'{CMYK_values[3]}')
CMYK_entry.grid(row=1, column=0, pady=5, padx=(3, 5))

# Ползунки для CMYK
cmyk_scales = []
for i in range(4):
    scale_button = ttk.Scale(CMYK_frame, from_=0, to=100, command=process_colors)
    scale_button.grid(row=i, column=1, padx=30, pady=5, sticky='w')
    cmyk_scales.append(scale_button)


# Метка для LAB
LAB_label = tk.Label(LAB_frame, text="LAB:")
LAB_label.grid(row=0, column=0, pady=(10, 5))

# Ввод текста для LAB
LAB_entry = tk.Entry(LAB_frame)
LAB_entry.insert(0, f'{LAB_values[0]}, ' + f'{LAB_values[1]}, ' + f'{LAB_values[2]}')
LAB_entry.grid(row=1, column=0, pady=5, padx=(3, 5))

# Ползунки для LAB
lab_scales = []
for i in range(3):
    if i == 0:
        scale_button = ttk.Scale(LAB_frame, from_=0, to=100, command=process_colors)
    else:
        scale_button = ttk.Scale(LAB_frame, from_=-0, to=127, command=process_colors)
    scale_button.grid(row=i, column=1, padx=30, pady=5, sticky='w')
    lab_scales.append(scale_button)

# Метка для HSV
HSV_label = tk.Label(HSV_frame, text="HSV:")
HSV_label.grid(row=0, column=0, pady=(10, 5))

# Ввод текста для LAB
HSV_entry = tk.Entry(HSV_frame)
HSV_entry.insert(0, f'{HSV_values[0]}, ' + f'{HSV_values[1]}, ' + f'{HSV_values[2]}')

HSV_entry.grid(row=1, column=0, pady=5, padx=(3, 5))

# Ползунки для HSV
hsv_scales = []
for i in range(3):
    if i == 0:
        scale_button = ttk.Scale(HSV_frame, from_=0, to=359, command=process_colors)
    else:
        scale_button = ttk.Scale(HSV_frame, from_=0, to=100, command=process_colors)
    scale_button.grid(row=i, column=1, padx=30, pady=5, sticky='w')
    hsv_scales.append(scale_button)

root.mainloop()
