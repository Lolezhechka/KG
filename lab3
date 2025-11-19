import tkinter as tk
from tkinter import ttk
import time
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class AlgorithmVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Базовые растровые алгоритмы - Лабораторная работа 3")
        
        self.canvas_width = 600
        self.canvas_height = 600
        self.grid_size = 20
        self.grid_offset_x = self.canvas_width // 2
        self.grid_offset_y = self.canvas_height // 2
        
        self.points = []
        self.current_algorithm = "step_by_step"
        self.start_point = None
        self.end_point = None
        self.circle_center = None
        self.circle_radius = 0
        self.computations = []
        self.execution_time = 0
        
        self.setup_ui()
        self.draw_grid()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, 
                               height=self.canvas_height, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        control_frame = ttk.Frame(main_frame, width=300)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        control_frame.pack_propagate(False)
        
        algo_frame = ttk.LabelFrame(control_frame, text="Алгоритмы", padding=10)
        algo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        algorithms = [
            ("Пошаговый алгоритм", "step_by_step"),
            ("Алгоритм ЦДА", "dda"),
            ("Алгоритм Брезенхема (линия)", "bresenham_line"),
            ("Алгоритм Брезенхема (окружность)", "bresenham_circle")
        ]
        
        self.algo_var = tk.StringVar(value="step_by_step")
        for text, value in algorithms:
            rb = ttk.Radiobutton(algo_frame, text=text, variable=self.algo_var, 
                               value=value, command=self.on_algorithm_change)
            rb.pack(anchor=tk.W, pady=2)
        
        info_frame = ttk.LabelFrame(control_frame, text="Информация", padding=10)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.time_label = ttk.Label(info_frame, text="Время: 0.000000 сек")
        self.time_label.pack(anchor=tk.W)
        
        self.status_label = ttk.Label(info_frame, text="Статус: Выберите алгоритм и точки")
        self.status_label.pack(anchor=tk.W)
        
        comp_frame = ttk.LabelFrame(control_frame, text="Вычисления", padding=10)
        comp_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        comp_scroll = ttk.Scrollbar(comp_frame)
        comp_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.comp_text = tk.Text(comp_frame, height=20, width=35, 
                                yscrollcommand=comp_scroll.set, font=('Courier', 9))
        self.comp_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        comp_scroll.config(command=self.comp_text.yview)
        
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        clear_btn = ttk.Button(btn_frame, text="Очистить поле", command=self.clear_canvas)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = ttk.Button(btn_frame, text="Экспорт вычислений", command=self.export_computations)
        export_btn.pack(side=tk.RIGHT, padx=5)
    
    def draw_grid(self):
        self.canvas.delete("grid")
        
        for x in range(0, self.canvas_width, self.grid_size):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill='lightgray', tags="grid")
        for y in range(0, self.canvas_height, self.grid_size):
            self.canvas.create_line(0, y, self.canvas_width, y, fill='lightgray', tags="grid")
        
        self.canvas.create_line(0, self.grid_offset_y, self.canvas_width, self.grid_offset_y, 
                               fill='black', width=2, tags="grid")
        self.canvas.create_line(self.grid_offset_x, 0, self.grid_offset_x, self.canvas_height, 
                               fill='black', width=2, tags="grid")
        
        for i in range(-self.grid_offset_x // self.grid_size, self.grid_offset_x // self.grid_size + 1):
            x = self.grid_offset_x + i * self.grid_size
            if i != 0:
                self.canvas.create_text(x, self.grid_offset_y + 10, text=str(i), tags="grid")
        
        for i in range(-self.grid_offset_y // self.grid_size, self.grid_offset_y // self.grid_size + 1):
            y = self.grid_offset_y - i * self.grid_size
            if i != 0:
                self.canvas.create_text(self.grid_offset_x + 10, y, text=str(i), tags="grid")
    
    def draw_pixel(self, x, y, color='red'):
        screen_x = self.grid_offset_x + x * self.grid_size
        screen_y = self.grid_offset_y - y * self.grid_size
        self.canvas.create_rectangle(
            screen_x, screen_y, 
            screen_x + self.grid_size, 
            screen_y + self.grid_size, 
            fill=color, outline='', tags="pixel"
        )
    
    def on_algorithm_change(self):
        self.current_algorithm = self.algo_var.get()
        self.clear_canvas()
        self.update_status("Алгоритм изменен. " + self.get_algorithm_instructions())
    
    def get_algorithm_instructions(self):
        if self.current_algorithm == "bresenham_circle":
            return "Кликните центр окружности, затем точку на окружности"
        else:
            return "Кликните начальную и конечную точки линии"
    
    def update_status(self, message):
        self.status_label.config(text=f"Статус: {message}")
    
    def update_computations(self):
        self.comp_text.delete(1.0, tk.END)
        for comp in self.computations[-20:]:  
            self.comp_text.insert(tk.END, comp + '\n')
        self.comp_text.see(tk.END)
    
    def on_canvas_click(self, event):
        grid_x = (event.x - self.grid_offset_x) // self.grid_size
        grid_y = (self.grid_offset_y - event.y) // self.grid_size
        
        if self.current_algorithm == "bresenham_circle":
            self.handle_circle_click(grid_x, grid_y)
        else:
            self.handle_line_click(grid_x, grid_y)
    
    def handle_line_click(self, grid_x, grid_y):
        if self.start_point is None:
            self.start_point = Point(grid_x, grid_y)
            self.draw_pixel(grid_x, grid_y, 'green')
            self.update_status("Выбрана начальная точка. Кликните конечную точку")
        else:
            self.end_point = Point(grid_x, grid_y)
            self.draw_pixel(grid_x, grid_y, 'blue')
            
            start_time = time.time()
            
            if self.current_algorithm == "step_by_step":
                self.points, self.computations = self.step_by_step_line(
                    self.start_point.x, self.start_point.y, 
                    self.end_point.x, self.end_point.y)
            elif self.current_algorithm == "dda":
                self.points, self.computations = self.dda_line(
                    self.start_point.x, self.start_point.y, 
                    self.end_point.x, self.end_point.y)
            elif self.current_algorithm == "bresenham_line":
                self.points, self.computations = self.bresenham_line(
                    self.start_point.x, self.start_point.y, 
                    self.end_point.x, self.end_point.y)
            
            self.execution_time = time.time() - start_time
            
            for point in self.points:
                self.draw_pixel(point.x, point.y)
            
            self.time_label.config(text=f"Время: {self.execution_time:.6f} сек")
            self.update_computations()
            self.update_status("Линия построена. Выберите новые точки")
            
            self.start_point = None
            self.end_point = None
    
    def handle_circle_click(self, grid_x, grid_y):
        if self.circle_center is None:
            self.circle_center = Point(grid_x, grid_y)
            self.draw_pixel(grid_x, grid_y, 'green')
            self.update_status("Выбран центр окружности. Кликните точку на окружности")
        else:
            dx = grid_x - self.circle_center.x
            dy = grid_y - self.circle_center.y
            self.circle_radius = int(math.sqrt(dx*dx + dy*dy))
            
            self.draw_pixel(grid_x, grid_y, 'blue')
            
            start_time = time.time()
            self.points, self.computations = self.bresenham_circle(
                self.circle_center.x, self.circle_center.y, self.circle_radius)
            self.execution_time = time.time() - start_time
            
            for point in self.points:
                self.draw_pixel(point.x, point.y)
            
            self.time_label.config(text=f"Время: {self.execution_time:.6f} сек")
            self.update_computations()
            self.update_status("Окружность построена. Выберите новые точки")
            
            self.circle_center = None
    
    def step_by_step_line(self, x1, y1, x2, y2):
        points = []
        computations = []
        
        computations.append(f"=== Пошаговый алгоритм ===")
        computations.append(f"Начальная точка: ({x1}, {y1})")
        computations.append(f"Конечная точка: ({x2}, {y2})")
        
        if x1 == x2:  
            computations.append("Вертикальная линия")
            for y in range(min(y1, y2), max(y1, y2) + 1):
                points.append(Point(x1, y))
                computations.append(f"Точка: ({x1}, {y})")
        else:
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            
            computations.append(f"Уравнение: y = {m:.2f}x + {b:.2f}")
            
            if abs(m) <= 1:
                computations.append("|m| <= 1, итерируем по x")
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    y = m * x + b
                    points.append(Point(x, round(y)))
                    computations.append(f"x={x}, y={m:.2f}*{x}+{b:.2f}={y:.2f} -> ({x}, {round(y)})")
            else:
                computations.append("|m| > 1, итерируем по y")
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    x = (y - b) / m
                    points.append(Point(round(x), y))
                    computations.append(f"y={y}, x=({y}-{b:.2f})/{m:.2f}={x:.2f} -> ({round(x)}, {y})")
        
        computations.append(f"Всего точек: {len(points)}")
        return points, computations
    
    def dda_line(self, x1, y1, x2, y2):
        points = []
        computations = []
        
        computations.append(f"=== Алгоритм ЦДА ===")
        computations.append(f"Начальная точка: ({x1}, {y1})")
        computations.append(f"Конечная точка: ({x2}, {y2})")
        
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        
        computations.append(f"dx = {dx}, dy = {dy}")
        computations.append(f"steps = {steps}")
        
        if steps == 0:
            points.append(Point(x1, y1))
            computations.append(f"Точка: ({x1}, {y1})")
            return points, computations
        
        x_inc = dx / steps
        y_inc = dy / steps
        
        computations.append(f"x_inc = {x_inc:.2f}, y_inc = {y_inc:.2f}")
        
        x = x1
        y = y1
        
        for i in range(steps + 1):
            points.append(Point(round(x), round(y)))
            computations.append(f"Шаг {i}: x={x:.2f}->{round(x)}, y={y:.2f}->{round(y)}")
            x += x_inc
            y += y_inc
        
        computations.append(f"Всего точек: {len(points)}")
        return points, computations
    
    def bresenham_line(self, x1, y1, x2, y2):
        points = []
        computations = []
        
        computations.append(f"=== Алгоритм Брезенхема (линия) ===")
        computations.append(f"Начальная точка: ({x1}, {y1})")
        computations.append(f"Конечная точка: ({x2}, {y2})")
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        computations.append(f"dx = {dx}, dy = {dy}")
        
        x, y = x1, y1
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        if dx > dy:
            err = dx / 2
            computations.append(f"Основное направление: X, err = {err:.2f}")
            while x != x2:
                points.append(Point(x, y))
                computations.append(f"Точка: ({x}, {y}), err = {err:.2f}")
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                    computations.append(f"err < 0, y += {sy}, err += dx = {err:.2f}")
                x += sx
        else:
            err = dy / 2
            computations.append(f"Основное направление: Y, err = {err:.2f}")
            while y != y2:
                points.append(Point(x, y))
                computations.append(f"Точка: ({x}, {y}), err = {err:.2f}")
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                    computations.append(f"err < 0, x += {sx}, err += dy = {err:.2f}")
                y += sy
        
        points.append(Point(x2, y2))
        computations.append(f"Точка: ({x2}, {y2})")
        computations.append(f"Всего точек: {len(points)}")
        
        return points, computations
    
    def bresenham_circle(self, xc, yc, r):
        points = []
        computations = []
        
        computations.append(f"=== Алгоритм Брезенхема (окружность) ===")
        computations.append(f"Центр: ({xc}, {yc}), Радиус: {r}")
        
        x = 0
        y = r
        d = 3 - 2 * r
        
        computations.append(f"Начальные значения: x=0, y={r}, d={d}")
        
        while y >= x:
            computations.append(f"x={x}, y={y}, d={d}")
            
            for dx, dy in [(x, y), (-x, y), (x, -y), (-x, -y),
                          (y, x), (-y, x), (y, -x), (-y, -x)]:
                points.append(Point(xc + dx, yc + dy))
            
            x += 1
            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
                computations.append(f"d > 0: y--, d = {d}")
            else:
                d = d + 4 * x + 6
                computations.append(f"d <= 0: d = {d}")
        
        computations.append(f"Всего точек: {len(points)}")
        return points, computations
    
    def clear_canvas(self):
        self.canvas.delete("pixel")
        self.points = []
        self.computations = []
        self.start_point = None
        self.end_point = None
        self.circle_center = None
        self.execution_time = 0
        self.time_label.config(text="Время: 0.000000 сек")
        self.comp_text.delete(1.0, tk.END)
        self.update_status("Поле очищено. " + self.get_algorithm_instructions())
    
    def export_computations(self):
        if self.computations:
            with open("computations.txt", "w", encoding="utf-8") as f:
                f.write("Вычисления алгоритма:\n")
                f.write("=" * 50 + "\n")
                for comp in self.computations:
                    f.write(comp + "\n")
                f.write(f"\nВремя выполнения: {self.execution_time:.6f} сек\n")
                f.write(f"Количество точек: {len(self.points)}\n")
            self.update_status("Вычисления экспортированы в computations.txt")

def main():
    root = tk.Tk()
    root.geometry("1000x700")
    app = AlgorithmVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
