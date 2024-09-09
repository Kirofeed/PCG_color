import math
import tkinter as tk
from tkinter import *
from tkinter import colorchooser
from tkinter import ttk

def hex_to_rgb(hexik):
    hexik = hexik.lstrip('#')
    return tuple(int(hexik[i:i+2], 16) for i in (0, 2, 4))





def rgb_to_cmyk(r, g, b):
    r_new = r/255
    g_new = g/255
    b_new = b/255
    k = 1 - max(r_new, g_new, b_new)
    if not k == 1:
        c = (1 - r_new - k) / (1 - k)
        m = (1 - g_new - k) / (1 - k)
        y = (1 - b_new - k) / (1 - k)
    else:
        c = 0
        m = 0
        y = 0
    c *= 100
    m *= 100
    y *= 100
    k *= 100
    return c, m, y, k

def cmyk_to_rgb(c, m, y, k):
    c_new = c / 100
    m_new = m / 100
    y_new = y / 100
    k_new = k / 100
    r = 255 * (1 - c_new) * (1 - k_new)
    g = 255 * (1 - m_new) * (1 - k_new)
    b = 255 * (1 - y_new) * (1 - k_new)
    return r, g, b

def rgb_to_xyz(r, g, b):
    r_prime, g_prime, b_prime = r / 255.0, g / 255.0, b / 255.0

    # Gamma correction
    r_prime = (r_prime / 12.92) if r_prime <= 0.04045 else ((r_prime + 0.055) / 1.055) ** 2.4
    g_prime = (g_prime / 12.92) if g_prime <= 0.04045 else ((g_prime + 0.055) / 1.055) ** 2.4
    b_prime = (b_prime / 12.92) if b_prime <= 0.04045 else ((b_prime + 0.055) / 1.055) ** 2.4

    # Convert to XYZ
    x = r_prime * 0.4124 + g_prime * 0.3576 + b_prime * 0.1805
    y = r_prime * 0.2126 + g_prime * 0.7152 + b_prime * 0.0722
    z = r_prime * 0.0193 + g_prime * 0.1192 + b_prime * 0.9505

    return x * 100, y * 100, z * 100

def xyz_to_lab(x, y, z):
    # Normalize for D65 white point
    x = x / 95.047
    y = y / 100.000
    z = z / 108.883

    # Function for LAB conversion
    def f(t):
        return math.pow(t, 1/3) if t > 0.008856 else (7.787 * t + 16 / 116)

    l = 116 * f(y) - 16
    a = 500 * (f(x) - f(y))
    b = 200 * (f(y) - f(z))

    return l, a, b

def rgb_to_lab(r, g, b):
    xyz = rgb_to_xyz(r, g, b)
    return xyz_to_lab(*xyz)

def lab_to_xyz(l, a, b):
    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200

    x = 95.047 * (math.pow(x, 3) if math.pow(x, 3) > 0.008856 else (x - 16 / 116) / 7.787)
    y = 100.000 * (math.pow(y, 3) if math.pow(y, 3) > 0.008856 else (y - 16 / 116) / 7.787)
    z = 108.883 * (math.pow(z, 3) if math.pow(z, 3) > 0.008856 else (z - 16 / 116) / 7.787)

    return x, y, z

def xyz_to_rgb(x, y, z):
    x /= 100
    y /= 100
    z /= 100

    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570

    r = 12.92 * r if r <= 0.0031308 else 1.055 * (math.pow(r, 1 / 2.4)) - 0.055
    g = 12.92 * g if g <= 0.0031308 else 1.055 * (math.pow(g, 1 / 2.4)) - 0.055
    b = 12.92 * b if b <= 0.0031308 else 1.055 * (math.pow(b, 1 / 2.4)) - 0.055

    r = min(max(0, r), 1)
    g = min(max(0, g), 1)
    b = min(max(0, b), 1)

    return int(r * 255), int(g * 255), int(b * 255)

def lab_to_rgb(l, a, b):
    xyz = lab_to_xyz(l, a, b)
    return xyz_to_rgb(*xyz)


def rgb_to_hsv(r, g, b):
    # Нормализуем значения RGB к диапазону [0, 1]
    r_prime, g_prime, b_prime = r / 255.0, g / 255.0, b / 255.0

    # Найдем минимальное и максимальное значения и их разность
    c_max = max(r_prime, g_prime, b_prime)
    c_min = min(r_prime, g_prime, b_prime)
    delta = c_max - c_min

    h = 0
    # Вычисляем значение H (Hue)
    if delta == 0:
        h = 0
    elif c_max == r_prime:
        h = 60 * (((g_prime - b_prime) / delta) % 6)
    elif c_max == g_prime:
        h = 60 * (((b_prime - r_prime) / delta) + 2)
    elif c_max == b_prime:
        h = 60 * (((r_prime - g_prime) / delta) + 4)

    # Вычисляем значение S (Saturation)
    s = 0 if c_max == 0 else (delta / c_max)

    # Вычисляем значение V (Value)
    v = c_max

    # Преобразуем H в диапазон [0, 360], а S и V — в [0, 100]
    h = int(h)
    s = int(s * 100)
    v = int(v * 100)

    return h, s, v


def hsv_to_rgb(h, s, v):
    s /= 100
    v /= 100

    c = v * s  # chroma
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r_prime, g_prime, b_prime = c, x, 0
    elif 60 <= h < 120:
        r_prime, g_prime, b_prime = x, c, 0
    elif 120 <= h < 180:
        r_prime, g_prime, b_prime = 0, c, x
    elif 180 <= h < 240:
        r_prime, g_prime, b_prime = 0, x, c
    elif 240 <= h < 300:
        r_prime, g_prime, b_prime = x, 0, c
    else:  # 300 <= h < 360
        r_prime, g_prime, b_prime = c, 0, x

    r = (r_prime + m) * 255
    g = (g_prime + m) * 255
    b = (b_prime + m) * 255

    return int(r), int(g), int(b)

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[1]
    if color_code:
        r, g, b = hex_to_rgb(color_code)

        cmyk = rgb_to_cmyk(r, g, b)
        lab = rgb_to_lab(r, g, b)
        hsv = rgb_to_hsv(r, g, b)

        CMYK_values[0].set(cmyk[0])
        CMYK_values[1].set(cmyk[1])
        CMYK_values[2].set(cmyk[2])
        CMYK_values[3].set(cmyk[3])
        LAB_values[0].set(lab[0])
        LAB_values[1].set(lab[1])
        LAB_values[2].set(lab[2])
        HSV_values[0].set(hsv[0])
        HSV_values[1].set(hsv[1])
        HSV_values[2].set(hsv[2])

        update_colors()
        update_color_rectangles()
        print(f'RGB: {r}, {g}, {b}')

def update_color_rectangles():
    # Обновляем цвета квадратов для CMYK, LAB, HSV
    cmyk_color = cmyk_to_rgb(CMYK_values[0].get(), CMYK_values[1].get(), CMYK_values[2].get(), CMYK_values[3].get())
    lab_color = lab_to_rgb(LAB_values[0].get(), LAB_values[1].get(), LAB_values[2].get())
    hsv_color = hsv_to_rgb(HSV_values[0].get(), HSV_values[1].get(), HSV_values[2].get())

    # Обновляем цвета квадратов в формате RGB
    cmyk_canvas.config(bg=f'#{int(cmyk_color[0]):02x}{int(cmyk_color[1]):02x}{int(cmyk_color[2]):02x}')
    lab_canvas.config(bg=f'#{int(lab_color[0]):02x}{int(lab_color[1]):02x}{int(lab_color[2]):02x}')
    hsv_canvas.config(bg=f'#{int(hsv_color[0]):02x}{int(hsv_color[1]):02x}{int(hsv_color[2]):02x}')


# Создание функции реагирования
def update_colors():
    # Обновляем поля ввода с округлением до 2 знаков
    CMYK_entry.delete(0, tk.END)
    CMYK_entry.insert(0, f'{round(CMYK_values[0].get(), 1)}, {round(CMYK_values[1].get(), 1)}, {round(CMYK_values[2].get(), 1)}, {round(CMYK_values[3].get(), 1)}')

    LAB_entry.delete(0, tk.END)
    LAB_entry.insert(0, f'{round(LAB_values[0].get(), 1)}, {round(LAB_values[1].get(), 1)}, {round(LAB_values[2].get(), 1)}')

    HSV_entry.delete(0, tk.END)
    HSV_entry.insert(0, f'{round(HSV_values[0].get(), 1)}, {round(HSV_values[1].get(), 1)}, {round(HSV_values[2].get(), 1)}')


def update_from_hsv(*args):
    h = HSV_values[0].get()
    s = HSV_values[1].get()
    v = HSV_values[2].get()

    r, g, b = hsv_to_rgb(h, s, v)
    cmyk = rgb_to_cmyk(r, g, b)
    lab = rgb_to_lab(r, g, b)

    CMYK_values[0].set(cmyk[0])
    CMYK_values[1].set(cmyk[1])
    CMYK_values[2].set(cmyk[2])
    CMYK_values[3].set(cmyk[3])
    LAB_values[0].set(lab[0])
    LAB_values[1].set(lab[1])
    LAB_values[2].set(lab[2])

    update_colors()
    update_color_rectangles()

def update_from_cmyk(*args):
    c = CMYK_values[0].get()
    m = CMYK_values[1].get()
    y = CMYK_values[2].get()
    k = CMYK_values[3].get()

    r, g, b = cmyk_to_rgb(c, m, y, k)
    hsv = rgb_to_hsv(r, g, b)
    lab = rgb_to_lab(r, g, b)

    LAB_values[0].set(lab[0])
    LAB_values[1].set(lab[1])
    LAB_values[2].set(lab[2])
    HSV_values[0].set(hsv[0])
    HSV_values[1].set(hsv[1])
    HSV_values[2].set(hsv[2])

    update_colors()
    update_color_rectangles()

def update_from_lab(*args):
    l = LAB_values[0].get()
    a = LAB_values[1].get()
    b = LAB_values[2].get()

    r, g, b = lab_to_rgb(l, a, b)
    cmyk = rgb_to_cmyk(r, g, b)
    hsv = rgb_to_hsv(r, g, b)

    CMYK_values[0].set(cmyk[0])
    CMYK_values[1].set(cmyk[1])
    CMYK_values[2].set(cmyk[2])
    CMYK_values[3].set(cmyk[3])
    HSV_values[0].set(hsv[0])
    HSV_values[1].set(hsv[1])
    HSV_values[2].set(hsv[2])

    update_colors()
    update_color_rectangles()

# Создание окна
root = tk.Tk()
# root.minsize(500, 500)
# root.maxsize(1000, 600)
root.title("Color Converter")

CMYK_values = [DoubleVar(value=0), DoubleVar(value=0), DoubleVar(value=0), DoubleVar(value=0)]
LAB_values = [DoubleVar(value=100), DoubleVar(value=0), DoubleVar(value=0)]
HSV_values = [DoubleVar(value=0), DoubleVar(value=0), DoubleVar(value=100)]

# Создание фреймов
CMYK_frame = tk.Frame(root)
LAB_frame = tk.Frame(root)
HSV_frame = tk.Frame(root)

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
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

# Кнопка для выбора цвета
color_button = tk.Button(root, text="Choose Color", command=choose_color)
color_button.grid(row=0, column=0, columnspan=1, padx=5, pady=20)

# Поле цветов
# Квадраты для отображения цветов
cmyk_canvas = tk.Canvas(root, width=100, height=100, bg='white')
lab_canvas = tk.Canvas(root, width=100, height=100, bg='white')
hsv_canvas = tk.Canvas(root, width=100, height=100, bg='white')

# Размещение квадратов
cmyk_canvas.grid(row=1, column=1, padx=10, pady=10)
lab_canvas.grid(row=2, column=1, padx=10, pady=10)
hsv_canvas.grid(row=3, column=1, padx=10, pady=10)


# Метка для CMYK
CMYK_label = tk.Label(CMYK_frame, text="CMYK:")
CMYK_label.grid(row=0, column=0, pady=(10, 5))

# Ввод текста для CMYK
CMYK_entry = tk.Entry(CMYK_frame)
CMYK_entry.insert(0, f'{CMYK_values[0].get()}, ' + f'{CMYK_values[1].get()}, ' +
                  f'{CMYK_values[2].get()}' + f'{CMYK_values[3].get()}')
CMYK_entry.grid(row=1, column=0, pady=5, padx=(3, 5))

# Ползунки для CMYK
cmyk_scales = []
for i in range(4):
    scale_button = ttk.Scale(CMYK_frame, from_=0, to=100, variable=CMYK_values[i], command=update_from_cmyk)
    scale_button.grid(row=i, column=1, padx=30, pady=5, sticky='w')
    cmyk_scales.append(scale_button)


# Метка для LAB
LAB_label = tk.Label(LAB_frame, text="LAB:")
LAB_label.grid(row=0, column=0, pady=(10, 5))

# Ввод текста для LAB
LAB_entry = tk.Entry(LAB_frame)
LAB_entry.insert(0, f'{LAB_values[0].get()}, ' + f'{LAB_values[1].get()}, ' + f'{LAB_values[2].get()}')
LAB_entry.grid(row=1, column=0, pady=5, padx=(3, 5))

# Ползунки для LAB
lab_scales = []
for i in range(3):
    if i == 0:
        scale_button = ttk.Scale(LAB_frame, from_=0, to=100, variable=LAB_values[i], command=update_from_lab)
    else:
        scale_button = ttk.Scale(LAB_frame, from_=-0, to=127, variable=LAB_values[i], command=update_from_lab)
    scale_button.grid(row=i, column=1, padx=30, pady=5, sticky='w')
    lab_scales.append(scale_button)

# Метка для HSV
HSV_label = tk.Label(HSV_frame, text="HSV:")
HSV_label.grid(row=0, column=0, pady=(10, 5))

# Ввод текста для HSV
HSV_entry = tk.Entry(HSV_frame)
HSV_entry.insert(0, f'{HSV_values[0].get()}, ' + f'{HSV_values[1].get()}, ' + f'{HSV_values[2].get()}')

HSV_entry.grid(row=1, column=0, pady=5, padx=(3, 5))

# Ползунки для HSV
hsv_scales = []
for i in range(3):
    if i == 0:
        scale_button = ttk.Scale(HSV_frame, from_=0, to=359, variable=HSV_values[i], command=update_from_hsv)
    else:
        scale_button = ttk.Scale(HSV_frame, from_=0, to=100, variable=HSV_values[i], command=update_from_hsv)
    scale_button.grid(row=i, column=1, padx=30, pady=5, sticky='w')
    hsv_scales.append(scale_button)

root.mainloop()
