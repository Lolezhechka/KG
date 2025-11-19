import tkinter as tk
from tkinter import filedialog
import os
import struct
from PIL import Image

def lzw_compress(data: bytes):
    dictionary = {bytes([i]): i for i in range(256)}
    next_code = 256
    w = b""
    out = []

    for b in data:
        wb = w + bytes([b])
        if wb in dictionary:
            w = wb
        else:
            out.append(dictionary[w])
            if next_code < 4096:
                dictionary[wb] = next_code
                next_code += 1
            w = bytes([b])

    if w:
        out.append(dictionary[w])

    return out

def lzw_decompress(codes):
    dictionary = {i: bytes([i]) for i in range(256)}
    next_code = 256

    if not codes:
        return b""
    
    prev = codes[0]
    result = bytearray(dictionary[prev])
    w = dictionary[prev]

    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = w + w[:1]
        else:
            raise ValueError("invalid LZW code")

        result.extend(entry)
        if next_code < 4096:
            dictionary[next_code] = w + entry[:1]
            next_code += 1
        w = entry

    return bytes(result)

def save_lzw(path, width, height, codes):
    with open(path, "wb") as f:
        f.write(struct.pack("<I", width))
        f.write(struct.pack("<I", height))
        f.write(struct.pack("<I", len(codes)))
        for c in codes:
            f.write(struct.pack("<H", c))

def load_lzw(path):
    with open(path, "rb") as f:
        width = struct.unpack("<I", f.read(4))[0]
        height = struct.unpack("<I", f.read(4))[0]
        code_count = struct.unpack("<I", f.read(4))[0]
        codes = [struct.unpack("<H", f.read(2))[0] for _ in range(code_count)]
    return width, height, codes

def image_to_binary_data(image_path):
    try:
        img = Image.open(image_path)
        
        if img.mode != '1':
            img = img.convert('1')
        
        binary_data = img.tobytes()
        
        return binary_data, img.size
    
    except Exception as e:
        raise ValueError(f"Ошибка обработки изображения: {e}")

def binary_data_to_image(binary_data, width, height):
    try:
        img = Image.frombytes('1', (width, height), binary_data)
        return img
    
    except Exception as e:
        raise ValueError(f"Ошибка восстановления изображения: {e}")

class LZWApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LZW Black & White Image Compressor")
        self.root.geometry("500x400")

        self.raw_data = None
        self.codes = None
        self.original_size = None
        self.compressed_size = None
        self.image_width = None
        self.image_height = None

        tk.Button(root, text="1. Загрузить чёрно-белое изображение", command=self.load_image, 
                 font=("Arial", 10)).pack(pady=10)
        tk.Button(root, text="2. Сжать LZW", command=self.compress_file,
                 font=("Arial", 10)).pack(pady=5)
        tk.Button(root, text="3. Сохранить .lzw", command=self.save_compressed,
                 font=("Arial", 10)).pack(pady=5)
        tk.Button(root, text="4. Загрузить .lzw", command=self.load_compressed,
                 font=("Arial", 10)).pack(pady=5)
        tk.Button(root, text="5. Распаковать и сохранить", command=self.decompress,
                 font=("Arial", 10)).pack(pady=5)

        self.stats = tk.Label(root, text="Нет данных.", justify="left", 
                             font=("Arial", 11), fg="blue")
        self.stats.pack(pady=20)

        self.status = tk.Label(root, text="Готов к работе", justify="left", 
                              font=("Arial", 9), fg="green")
        self.status.pack(pady=5)

    def update_stats(self):
        text = ""
        if self.original_size is not None:
            text += f"Исходный размер: {self.original_size:,} байт\n"
        if self.compressed_size is not None and self.original_size is not None:
            eff = (1 - self.compressed_size / self.original_size) * 100
            text += f"После LZW: {self.compressed_size:,} байт\n"
            text += f"Эффективность: {eff:+.1f}%\n"
            
            if eff > 0:
                text += f"Экономия: {self.original_size - self.compressed_size:,} байт\n"
            
        if self.image_width and self.image_height:
            text += f"Изображение: {self.image_width}x{self.image_height} (чёрно-белое)\n"
        
        self.stats.config(text=text if text else "Нет данных.")

    def update_status(self, message):
        self.status.config(text=message)

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            raw_data, (width, height) = image_to_binary_data(path)
            self.raw_data = raw_data
            self.original_size = len(raw_data)
            self.image_width = width
            self.image_height = height
            self.codes = None
            self.compressed_size = None

            self.update_stats()
            self.update_status(f"✓ Загружено: {width}x{height} чёрно-белое изображение")

        except Exception as e:
            self.update_status(f"✗ Ошибка загрузки: {str(e)}")

    def compress_file(self):
        if self.raw_data is None:
            self.update_status("✗ Сначала загрузите изображение")
            return

        try:
            self.codes = lzw_compress(self.raw_data)

            tmp = ".__tmp__.lzw"
            save_lzw(tmp, self.image_width, self.image_height, self.codes)
            self.compressed_size = os.path.getsize(tmp)
            os.remove(tmp)

            self.update_stats()
            self.update_status("✓ LZW сжатие завершено")

        except Exception as e:
            self.update_status(f"✗ Ошибка сжатия: {str(e)}")

    def save_compressed(self):
        if self.codes is None:
            self.update_status("✗ Сначала выполните сжатие")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".lzw",
            filetypes=[("LZW files", "*.lzw"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            save_lzw(path, self.image_width, self.image_height, self.codes)
            self.compressed_size = os.path.getsize(path)
            self.update_stats()
            self.update_status(f"✓ Сохранено: {os.path.basename(path)}")
        except Exception as e:
            self.update_status(f"✗ Ошибка сохранения: {str(e)}")

    def load_compressed(self):
        path = filedialog.askopenfilename(filetypes=[("LZW files", "*.lzw")])
        if not path:
            return

        try:
            width, height, self.codes = load_lzw(path)
            self.compressed_size = os.path.getsize(path)
            self.image_width = width
            self.image_height = height
            self.original_size = None
            self.update_stats()
            self.update_status(f"✓ Загружено: {width}x{height} сжатое изображение")
        except Exception as e:
            self.update_status(f"✗ Ошибка загрузки: {str(e)}")

    def decompress(self):
        if self.codes is None:
            self.update_status("✗ Сначала загрузите сжатый файл (.lzw)")
            return

        try:
            decompressed_data = lzw_decompress(self.codes)

            restored_image = binary_data_to_image(decompressed_data, self.image_width, self.image_height)

            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if save_path:
                restored_image.save(save_path)
                self.update_status(f"✓ Сохранено: {os.path.basename(save_path)}")

        except Exception as e:
            self.update_status(f"✗ Ошибка распаковки: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LZWApp(root)
    root.mainloop()
