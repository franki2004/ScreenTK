from tkinter import Canvas, Toplevel, Tk
from os import makedirs, path
from keyboard import on_press_key
from PIL import ImageGrab

class ScreenTK:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()  

        self.selecting_area = False
        self.dim_window = None 

        on_press_key("print screen", self.on_print_screen)

    def on_print_screen(self, event):
        if not self.selecting_area:
            self.start_selection()

    def start_selection(self):
        self.selecting_area = True
        self.dim_screen()

    def dim_screen(self):
        self.dim_window = Toplevel(self.root)
        self.dim_window.attributes("-fullscreen", True)
        self.dim_window.attributes("-alpha", 0.3)  

        self.canvas = Canvas(self.dim_window, bd=0, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def on_mouse_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.draw_rectangle()

    def on_mouse_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.draw_rectangle()
        self.capture_region()

    def draw_rectangle(self):
        if hasattr(self, "rectangle"):
            self.canvas.delete(self.rectangle)

        x0, y0 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x1, y1 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)

        self.rectangle = self.canvas.create_rectangle(x0, y0, x1, y1, outline="white", dash=(2, 2), width=2)


    def capture_region(self):
        x0, y0 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x1, y1 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)

        if self.dim_window:
            self.dim_window.attributes("-alpha", 0.0)

        screenshot_name = self.generate_screenshot_name()

        screenshot = ImageGrab.grab(bbox=(x0, y0, x1, y1))
        screenshot.save(screenshot_name)

        self.dim_window.destroy()
        self.selecting_area = False

    def generate_screenshot_name(self):
        screenshot_dir = "screenshots"
        if not path.exists(screenshot_dir):
            makedirs(screenshot_dir)

        i = 1
        while True:
            screenshot_name = f"screenshot{i}.png"
            if not path.exists(path.join(screenshot_dir, screenshot_name)):
                return path.join(screenshot_dir, screenshot_name)
            i += 1

def main():
    app = ScreenTK()
    app.root.mainloop()

if __name__ == "__main__":
    main()
