import tkinter as tk
from tkinter import ttk, colorchooser
import colorsys

class ColorConverter:
    @staticmethod
    def rgb_to_cmyk(r, g, b):
        r, g, b = r/255.0, g/255.0, b/255.0
        k = 1 - max(r, g, b)
        if k == 1:
            return 0, 0, 0, 100
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
        return round(c*100), round(m*100), round(y*100), round(k*100)

    @staticmethod
    def cmyk_to_rgb(c, m, y, k):
        c, m, y, k = c/100.0, m/100.0, y/100.0, k/100.0
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        return round(r), round(g), round(b)

    @staticmethod
    def rgb_to_hsv(r, g, b):
        r, g, b = r/255.0, g/255.0, b/255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return round(h*360), round(s*100), round(v*100)

    @staticmethod
    def hsv_to_rgb(h, s, v):
        h, s, v = h/360.0, s/100.0, v/100.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return round(r*255), round(g*255), round(b*255)

class ColorModelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Цветовые модели: CMYK-RGB-HSV")
        self.root.geometry("800x600")
        
        self.current_rgb = (128, 128, 128)
        self.updating = False
        
        self.setup_ui()
        self.update_all_models()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Конвертер цветовых моделей: CMYK-RGB-HSV", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        color_display_frame = ttk.LabelFrame(main_frame, text="Текущий цвет", padding="10")
        color_display_frame.pack(fill=tk.X, pady=10)
        
        self.color_canvas = tk.Canvas(color_display_frame, height=60, bg=self.rgb_to_hex(self.current_rgb))
        self.color_canvas.pack(fill=tk.X, padx=20, pady=5)
        
        self.hex_label = ttk.Label(color_display_frame, text="#808080", font=('Arial', 12))
        self.hex_label.pack(pady=5)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.setup_rgb_tab(notebook)
        self.setup_cmyk_tab(notebook)
        self.setup_hsv_tab(notebook)
        self.setup_palette_tab(notebook)
    
    def setup_rgb_tab(self, notebook):
        rgb_frame = ttk.Frame(notebook, padding="10")
        notebook.add(rgb_frame, text="RGB")
        
        ttk.Label(rgb_frame, text="R:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.r_slider = ttk.Scale(rgb_frame, from_=0, to=255, orient=tk.HORIZONTAL, 
                                 command=self.on_rgb_slider_change)
        self.r_slider.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.r_entry = ttk.Entry(rgb_frame, width=5)
        self.r_entry.grid(row=0, column=2, padx=5, pady=5)
        self.r_entry.bind('<Return>', self.on_rgb_entry_change)
        
        ttk.Label(rgb_frame, text="G:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.g_slider = ttk.Scale(rgb_frame, from_=0, to=255, orient=tk.HORIZONTAL, 
                                 command=self.on_rgb_slider_change)
        self.g_slider.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        self.g_entry = ttk.Entry(rgb_frame, width=5)
        self.g_entry.grid(row=1, column=2, padx=5, pady=5)
        self.g_entry.bind('<Return>', self.on_rgb_entry_change)
        
        ttk.Label(rgb_frame, text="B:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.b_slider = ttk.Scale(rgb_frame, from_=0, to=255, orient=tk.HORIZONTAL, 
                                 command=self.on_rgb_slider_change)
        self.b_slider.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        self.b_entry = ttk.Entry(rgb_frame, width=5)
        self.b_entry.grid(row=2, column=2, padx=5, pady=5)
        self.b_entry.bind('<Return>', self.on_rgb_entry_change)
        
        rgb_frame.columnconfigure(1, weight=1)
    
    def setup_cmyk_tab(self, notebook):
        cmyk_frame = ttk.Frame(notebook, padding="10")
        notebook.add(cmyk_frame, text="CMYK")
        
        ttk.Label(cmyk_frame, text="C:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.c_slider = ttk.Scale(cmyk_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                 command=self.on_cmyk_slider_change)
        self.c_slider.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.c_entry = ttk.Entry(cmyk_frame, width=5)
        self.c_entry.grid(row=0, column=2, padx=5, pady=5)
        self.c_entry.bind('<Return>', self.on_cmyk_entry_change)
        
        ttk.Label(cmyk_frame, text="M:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.m_slider = ttk.Scale(cmyk_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                 command=self.on_cmyk_slider_change)
        self.m_slider.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        self.m_entry = ttk.Entry(cmyk_frame, width=5)
        self.m_entry.grid(row=1, column=2, padx=5, pady=5)
        self.m_entry.bind('<Return>', self.on_cmyk_entry_change)
        
        ttk.Label(cmyk_frame, text="Y:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.y_slider = ttk.Scale(cmyk_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                 command=self.on_cmyk_slider_change)
        self.y_slider.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        self.y_entry = ttk.Entry(cmyk_frame, width=5)
        self.y_entry.grid(row=2, column=2, padx=5, pady=5)
        self.y_entry.bind('<Return>', self.on_cmyk_entry_change)
        
        ttk.Label(cmyk_frame, text="K:", font=('Arial', 10)).grid(row=3, column=0, sticky='w', pady=5)
        self.k_slider = ttk.Scale(cmyk_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                 command=self.on_cmyk_slider_change)
        self.k_slider.grid(row=3, column=1, sticky='ew', padx=5, pady=5)
        self.k_entry = ttk.Entry(cmyk_frame, width=5)
        self.k_entry.grid(row=3, column=2, padx=5, pady=5)
        self.k_entry.bind('<Return>', self.on_cmyk_entry_change)
        
        cmyk_frame.columnconfigure(1, weight=1)
    
    def setup_hsv_tab(self, notebook):
        hsv_frame = ttk.Frame(notebook, padding="10")
        notebook.add(hsv_frame, text="HSV")
        
        ttk.Label(hsv_frame, text="H:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.h_slider = ttk.Scale(hsv_frame, from_=0, to=360, orient=tk.HORIZONTAL, 
                                 command=self.on_hsv_slider_change)
        self.h_slider.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.h_entry = ttk.Entry(hsv_frame, width=5)
        self.h_entry.grid(row=0, column=2, padx=5, pady=5)
        self.h_entry.bind('<Return>', self.on_hsv_entry_change)
        
        ttk.Label(hsv_frame, text="S:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.s_slider = ttk.Scale(hsv_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                 command=self.on_hsv_slider_change)
        self.s_slider.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        self.s_entry = ttk.Entry(hsv_frame, width=5)
        self.s_entry.grid(row=1, column=2, padx=5, pady=5)
        self.s_entry.bind('<Return>', self.on_hsv_entry_change)
        
        ttk.Label(hsv_frame, text="V:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.v_slider = ttk.Scale(hsv_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                 command=self.on_hsv_slider_change)
        self.v_slider.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        self.v_entry = ttk.Entry(hsv_frame, width=5)
        self.v_entry.grid(row=2, column=2, padx=5, pady=5)
        self.v_entry.bind('<Return>', self.on_hsv_entry_change)
        
        hsv_frame.columnconfigure(1, weight=1)
    
    def setup_palette_tab(self, notebook):
        palette_frame = ttk.Frame(notebook, padding="10")
        notebook.add(palette_frame, text="Палитра")
        
        ttk.Button(palette_frame, text="Выбрать цвет из палитры", 
                  command=self.choose_color_from_palette,
                  style='Accent.TButton').pack(pady=10)
        
    
    def choose_color_from_palette(self):
        color = colorchooser.askcolor(initialcolor=self.rgb_to_hex(self.current_rgb), 
                                    title="Выберите цвет")
        if color[0] is not None:
            r, g, b = [int(c) for c in color[0]]
            self.current_rgb = (r, g, b)
            self.update_all_models()
    
    def on_color_select(self, color_hex):
        color_hex = color_hex.lstrip('#')
        r = int(color_hex[0:2], 16)
        g = int(color_hex[2:4], 16)
        b = int(color_hex[4:6], 16)
        self.current_rgb = (r, g, b)
        self.update_all_models()
    
    def on_rgb_slider_change(self, event=None):
        if self.updating:
            return
        r = int(self.r_slider.get())
        g = int(self.g_slider.get())
        b = int(self.b_slider.get())
        self.current_rgb = (r, g, b)
        self.update_all_models()
    
    def on_rgb_entry_change(self, event=None):
        if self.updating:
            return
        try:
            r = int(self.r_entry.get())
            g = int(self.g_entry.get())
            b = int(self.b_entry.get())
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                self.current_rgb = (r, g, b)
                self.update_all_models()
        except ValueError:
            pass
    
    def on_cmyk_slider_change(self, event=None):
        if self.updating:
            return
        c = int(self.c_slider.get())
        m = int(self.m_slider.get())
        y = int(self.y_slider.get())
        k = int(self.k_slider.get())
        self.current_rgb = ColorConverter.cmyk_to_rgb(c, m, y, k)
        self.update_all_models()
    
    def on_cmyk_entry_change(self, event=None):
        if self.updating:
            return
        try:
            c = int(self.c_entry.get())
            m = int(self.m_entry.get())
            y = int(self.y_entry.get())
            k = int(self.k_entry.get())
            if all(0 <= x <= 100 for x in [c, m, y, k]):
                self.current_rgb = ColorConverter.cmyk_to_rgb(c, m, y, k)
                self.update_all_models()
        except ValueError:
            pass
    
    def on_hsv_slider_change(self, event=None):
        if self.updating:
            return
        h = int(self.h_slider.get())
        s = int(self.s_slider.get())
        v = int(self.v_slider.get())
        self.current_rgb = ColorConverter.hsv_to_rgb(h, s, v)
        self.update_all_models()
    
    def on_hsv_entry_change(self, event=None):
        if self.updating:
            return
        try:
            h = int(self.h_entry.get())
            s = int(self.s_entry.get())
            v = int(self.v_entry.get())
            if 0 <= h <= 360 and 0 <= s <= 100 and 0 <= v <= 100:
                self.current_rgb = ColorConverter.hsv_to_rgb(h, s, v)
                self.update_all_models()
        except ValueError:
            pass
    
    def update_all_models(self):
        self.updating = True
        
        r, g, b = self.current_rgb
        
        self.r_slider.set(r)
        self.g_slider.set(g)
        self.b_slider.set(b)
        self.r_entry.delete(0, tk.END)
        self.r_entry.insert(0, str(r))
        self.g_entry.delete(0, tk.END)
        self.g_entry.insert(0, str(g))
        self.b_entry.delete(0, tk.END)
        self.b_entry.insert(0, str(b))
        
        c, m, y, k = ColorConverter.rgb_to_cmyk(r, g, b)
        self.c_slider.set(c)
        self.m_slider.set(m)
        self.y_slider.set(y)
        self.k_slider.set(k)
        self.c_entry.delete(0, tk.END)
        self.c_entry.insert(0, str(c))
        self.m_entry.delete(0, tk.END)
        self.m_entry.insert(0, str(m))
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, str(y))
        self.k_entry.delete(0, tk.END)
        self.k_entry.insert(0, str(k))
        
        h, s, v = ColorConverter.rgb_to_hsv(r, g, b)
        self.h_slider.set(h)
        self.s_slider.set(s)
        self.v_slider.set(v)
        self.h_entry.delete(0, tk.END)
        self.h_entry.insert(0, str(h))
        self.s_entry.delete(0, tk.END)
        self.s_entry.insert(0, str(s))
        self.v_entry.delete(0, tk.END)
        self.v_entry.insert(0, str(v))
        
        hex_color = self.rgb_to_hex(self.current_rgb)
        self.color_canvas.configure(bg=hex_color)
        self.hex_label.configure(text=hex_color)
        
        self.updating = False
    
    def rgb_to_hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

def main():
    root = tk.Tk()
    app = ColorModelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
