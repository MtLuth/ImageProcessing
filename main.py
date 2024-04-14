import cv2
import tkinter as tk
from tkinter import Canvas, Frame, Label, Entry, filedialog, Button
from PIL import Image, ImageTk
import time

class MainDisplay:
    def __init__(self):
        self.width = 1500
        self.height = 900
        self.root = tk.Tk()
        self.root.title("Image Processing")
        self.root.geometry(str(self.width) + "x" + str(self.height))
        
        self.main_label = Label(self.root)
        self.main_label.pack(side='left')
        
        self.upper_frame = Frame(self.main_label, width=1000, height=400)
        self.upper_frame.pack(side='top')
        
        self.upper_left_frame = Frame(self.upper_frame, width=500, height=400)
        self.upper_left_frame.pack(side='left')
        
        self.upper_right_frame = Frame(self.upper_frame, width=500, height=400)
        self.upper_right_frame.pack(side='left')
        
        self.upper_input_image = Canvas(self.upper_left_frame, width=500, height=400, bg='white')
        self.upper_input_image.pack()
        
        self.root.bind('i', lambda event: self.capture_image())
        self.upper_camera_image = Canvas(self.upper_right_frame, width=500, height=400, bg='white')
        self.upper_camera_image.pack()
        
        self.lower_frame = Frame(self.main_label, width=1000, height=400)
        self.lower_frame.pack(side='top')
        
        self.lower_left_frame = Frame(self.lower_frame, width=500, height=400)
        self.lower_left_frame.pack(side='left')
        
        self.lower_right_frame = Frame(self.lower_frame, width=500, height=400)
        self.lower_right_frame.pack(side='left')
        
        self.lower_input_image = Canvas(self.lower_left_frame, width=500, height=400, bg='white')
        self.lower_input_image.pack()
        
        self.root.bind('o', lambda event: self.capture_image_lower())
        self.lower_camera_image = Canvas(self.lower_right_frame, width=500, height=400, bg='white')
        self.lower_camera_image.pack()
        
        self.clock_label = Label(self.root, text="", font=("Roboto", 50), fg="blue", bg="white", borderwidth=2,
                                 width=300, relief="groove")
        self.clock_label.pack(side='top', pady=(5, 0))
        self.update_clock()

        info_text = "Mã Thẻ: 123456\nBiển số xe: 29C-12345\nGiờ vào: 08:00\nGiờ ra: 17:00"
        self.info_label = Label(self.root, text=info_text, font=("Roboto", 20), fg="black", bg="white", borderwidth=2, 
                                width=300, relief="groove", justify='left',padx=10, pady=10)  
        self.info_label.pack(side='top', pady=(5, 0))  

        self.cap_0 = cv2.VideoCapture(0)
        self.cap_1 = cv2.VideoCapture(1)
        
        self.video_capture = None
        self.selected_video_path = None
        self.video_selected = False
        self.video_frame = None  # Biến để lưu trữ frame từ video
        self.open_video_button = tk.Button(self.root, text='Chọn Video', command=self.open_video, font=("Roboto", 16), fg="white", bg="green", borderwidth=2, relief="raised")
        self.open_video_button.pack(side='top', pady=(5, 0))
        
        self.update_camera()
        
    def open_video(self):
        self.selected_video_path = filedialog.askopenfilename()
        self.video_capture = cv2.VideoCapture(self.selected_video_path)
        self.video_selected = True
        self.update_video()
        
    def update_video(self):
        if self.video_selected and self.video_capture is not None and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                # Resize frame to fit the display area without distortion
                display_width = self.upper_input_image.winfo_width()
                display_height = self.upper_input_image.winfo_height()
                frame_aspect_ratio = frame.shape[1] / frame.shape[0]
                display_aspect_ratio = display_width / display_height

                if frame_aspect_ratio > display_aspect_ratio:
                    new_height = int(display_width / frame_aspect_ratio)
                    frame = cv2.resize(frame, (display_width, new_height))
                    top_border = (display_height - new_height) // 2
                    bottom_border = display_height - new_height - top_border
                    frame = cv2.copyMakeBorder(frame, top_border, bottom_border, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
                else:
                    new_width = int(display_height * frame_aspect_ratio)
                    frame = cv2.resize(frame, (new_width, display_height))
                    left_border = (display_width - new_width) // 2
                    right_border = display_width - new_width - left_border
                    frame = cv2.copyMakeBorder(frame, 0, 0, left_border, right_border, cv2.BORDER_CONSTANT, value=(0, 0, 0))

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.video_frame = Image.fromarray(img)  # Lưu trữ frame từ video
                img = ImageTk.PhotoImage(image=self.video_frame)

                self.upper_input_image.create_image(0, 0, anchor='nw', image=img)
                self.upper_input_image.image = img

        self.root.after(10, self.update_video)

        
    def capture_image(self):
        if not self.video_selected:
            ret, frame = self.cap_0.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(image=img)

                self.upper_camera_image.create_image(0, 0, anchor='nw', image=img)
                self.upper_camera_image.image = img
        else:
            if self.video_frame is not None:  # Kiểm tra xem đã có frame từ video hay không
                img = ImageTk.PhotoImage(image=self.video_frame)

                self.upper_camera_image.create_image(0, 0, anchor='nw', image=img)
                self.upper_camera_image.image = img
    
    def capture_image_lower(self):
        if not self.video_selected:
            ret, frame = self.cap_1.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(image=img)
            
                self.lower_camera_image.create_image(0, 0, anchor='nw', image=img)
                self.lower_camera_image.image = img
            
    def update_camera(self):
        if not self.video_selected:
            ret_0, frame_0 = self.cap_0.read()
            if ret_0:
                img_0 = cv2.cvtColor(frame_0, cv2.COLOR_BGR2RGB)
                img_0 = Image.fromarray(img_0)
                img_0 = ImageTk.PhotoImage(image=img_0)

                self.upper_input_image.create_image(0, 0, anchor='nw', image=img_0)
                self.upper_input_image.image = img_0

            ret_1, frame_1 = self.cap_1.read()
            if ret_1:
                img_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2RGB)
                img_1 = Image.fromarray(img_1)
                img_1 = ImageTk.PhotoImage(image=img_1)

                self.lower_input_image.create_image(0, 0, anchor='nw', image=img_1)
                self.lower_input_image.image = img_1
            
        self.root.after(10, self.update_camera)
            
    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    main = MainDisplay()
    main.run()