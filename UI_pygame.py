import pygame
import sys
import time
import datetime
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import pygame.camera
from src.frame import Frame
from yolo_predictions import Lisence_predict
from src.form import Form
from src.card import CardParking
from src.window_select_card import Window_Select_Card

class Main:
    
    def __init__(self):
        pygame.init()
        pygame.camera.init()

        self.image_from_file = None

        self.width = 1280
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg_img = pygame.image.load('images/bg.jpg')

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.set_alpha(128)
        self.surface.fill((60, 91, 111))

        self.frame_height = 359
        self.frame_width = 430
        self.frame_color = (246, 245, 242)
        self.frame_alpha = 255

        self.cameras = pygame.camera.list_cameras()
        self.webcam = pygame.camera.Camera(self.cameras[0])
        self.webcam.start()
        self.img_webcam = self.webcam.get_image()
        self.img_webcam_width = self.frame_width-10
        self.img_webcam_height = self.frame_height-10

        self.frame1 = Frame(self.frame_width, self.frame_height, self.frame_color, self.frame_alpha)
        self.frame2 = Frame(self.frame_width, self.frame_height, self.frame_color, self.frame_alpha)
        self.frame3 = Frame(self.frame_width, self.frame_height, self.frame_color, self.frame_alpha)
        self.frame4 = Frame(self.frame_width, self.frame_height, self.frame_color, self.frame_alpha)

        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)

        self.image_check_in = None
        self.image_check_out = None

        self.form = Form()
        self.new_window = None

        pygame.display.set_caption("Image Proccessing - Group 14")

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                if (self.new_window != None and self.new_window.is_run == True):
                    x = pos_x - self.new_window.rect.x
                    y = pos_y - self.new_window.rect.y
                    self.new_window.check_click(x, y)
                    if (self.new_window.ticket_choosed != None and self.new_window.status == False):
                        self.check_in() 
                    elif (self.new_window.ticket_choosed != None):
                        self.check_out()
                    self.new_window.click_outside(pos_x, pos_y)
            if event.type == pygame.KEYDOWN:
                self.check_key_down(event)
            if event.type == self.timer_event:
                self.display_clock()
            if event.type == pygame.USEREVENT:
                if self.image_check_in != None or self.image_check_out != None:
                    self.image_check_in = None
                    self.image_check_out = None
                    self.frame2 = Frame(self.frame_width, self.frame_height, self.frame_color, self.frame_alpha)
                    self.frame3 = Frame(self.frame_width, self.frame_height, self.frame_color, self.frame_alpha)
            

    def check_key_down(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_i:
            self.new_window = Window_Select_Card(self, False)       
        
        if event.key == pygame.K_l:
            self.webcam.stop()
            self.cameras.clear()
            file_name = self.open_file_dialog()
            if (file_name != ""):
                self.image_from_file = pygame.image.load(file_name)
        if event.key == pygame.K_s:
            self.webcam.start()
            self.cameras.append(self.webcam)
        if event.key == pygame.K_o:
            self.new_window = Window_Select_Card(self, True)
        
    
    def draw(self):
        self.bg_img = pygame.transform.scale(self.bg_img, (self.width, self.height))
        self.screen.blit(self.bg_img, (0,0))
        self.screen.blit(self.surface, (0,0))
        self.frame1.draw(self.screen, 20, 20)
        self.frame2.draw(self.screen, 20+10+self.frame_width, 20)
        self.frame3.draw(self.screen, 20, 20+10+self.frame_height)
        self.frame4.draw(self.screen, 20+10+self.frame_width, 20+10+self.frame_height)

        self.display_clock()
        self.blit_form()

        if (self.new_window != None):
            if (self.new_window.is_run == True):
                self.new_window.blitme()
            
    def update_screen(self):
        self.draw()
        
        pygame.display.flip()
        if self.cameras:
            self.frame1.blit(self.img_webcam, self.img_webcam_width, self.img_webcam_height)
            self.img_webcam = self.webcam.get_image()
        elif self.image_from_file != None and self.image_from_file != "":
            self.frame1.blit(self.image_from_file, self.img_webcam_width, self.img_webcam_height)
        else:
            self.webcam.start()
            self.cameras.append(self.webcam)   
        if self.image_check_in != None:
            self.frame2.blit(self.image_check_in, self.img_webcam_width, self.img_webcam_height)
        if self.image_check_out != None:
            self.frame3.blit(self.image_check_out, self.img_webcam_width, self.img_webcam_height)

    def display_clock(self):
        current_time = time.strftime('%H:%M:%S')
        font = pygame.font.SysFont('timesnewroman', 40)
        clock_surface = font.render(current_time, True, (255, 255, 255))
        total_width_used = 20+self.frame_width*2+10
        distance_x = (self.width - total_width_used)//2
        self.clock_rect = clock_surface.get_rect()
        self.clock_rect.centerx = distance_x + total_width_used
        self.clock_rect.y = 20
        self.screen.blit(clock_surface, self.clock_rect)

    def blit_form(self):
        self.form_rect = self.form.rect
        self.form_rect.centerx = self.clock_rect.centerx
        self.form_rect.y = self.clock_rect.y + self.clock_rect.height + 10
        self.form.blitme(self.screen, self.form_rect)

    def open_file_dialog(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        root.destroy()
        return file_path
    
    def convert_to_cv2(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        img = cv2.flip(img, 1)
        return img
    
    def convert_cv2_to_surface(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.flip(img, 1)
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        img = pygame.surfarray.make_surface(img)
        return img

    def check_in(self):
        #Load lên giao diện ảnh chụp
        self.license_predict = Lisence_predict()
        if self.cameras:
            image_np = pygame.surfarray.array3d(self.img_webcam)
        elif self.image_from_file is not None:
            image_np = pygame.surfarray.array3d(self.image_from_file)
        
        image_np = self.convert_to_cv2(image_np)

        img_check_in = self.license_predict.yolo_prediction(image_np, self.license_predict.net)
        img_check_in = self.convert_cv2_to_surface(img_check_in)
        if self.license_predict.point >=80:
            if self.cameras:
                image_np = pygame.surfarray.array3d(self.img_webcam)
            elif self.image_from_file is not None:
                image_np = pygame.surfarray.array3d(self.image_from_file)
            
            image_np = self.convert_to_cv2(image_np)

            self.image_check_in = self.license_predict.yolo_prediction(image_np, self.license_predict.net)
            self.image_check_in = self.convert_cv2_to_surface(self.image_check_in)
            license = self.license_predict.license
            check_in_time = time.strftime('%H:%M:%S')
            series_number = self.new_window.ticket_choosed
            self.form = Form()
            self.form.lines[0] = "Mã thẻ: "+series_number
            if license != None:
                self.form.lines[1] = "Biển số: "+license
            self.form.lines[2] = "Giờ vào: "+check_in_time

            if (self.new_window.status):
                self.new_window.update_card_status(self.new_window.ticket_choosed, False)
            else:
                self.new_window.update_card_status(self.new_window.ticket_choosed, True)
            date = datetime.date.today()
            date = date.strftime("%Y-%m-%d")
            check_in_time = time.strftime("%H-%M")
            check_in_dir = "./ImageCheckIn/"
            pygame.image.save(self.image_check_in, check_in_dir+"-"+check_in_time+"-"+license+".png")
            pygame.time.set_timer(pygame.USEREVENT, 3000)
        else:
            self.show_warning()

    def check_out(self):
        self.license_predict = Lisence_predict()
        if self.cameras:
            image_np = pygame.surfarray.array3d(self.img_webcam)
        elif self.image_from_file is not None:
            image_np = pygame.surfarray.array3d(self.image_from_file)
        
        image_np = self.convert_to_cv2(image_np)

        image_check_out = self.license_predict.yolo_prediction(image_np, self.license_predict.net)
        image_check_out = self.convert_cv2_to_surface(image_check_out)
        if self.license_predict.point >= 80:
            self.image_check_out = image_check_out
            license = self.license_predict.license
            check_out_time = time.strftime('%H:%M:%S')
            series_number = self.new_window.ticket_choosed
            self.form = Form()
            self.form.lines[0] = "Mã thẻ: "+series_number
            self.form.lines[3] = "Giờ ra: "+check_out_time
            self.form.lines[1] = "Biển số: "+license 
            if (self.new_window.status):
                    self.new_window.update_card_status(self.new_window.ticket_choosed, False)
            else:
                self.new_window.update_card_status(self.new_window.ticket_choosed, True)
            date = datetime.date.today()
            date = date.strftime("%Y-%m-%d")
            check_out_time = time.strftime("%H-%M")
            check_out_dir = "./ImageCheckOut/"
            pygame.image.save(self.image_check_in, check_out_dir+"-"+check_out_time+"-"+license+".png")
            pygame.time.set_timer(pygame.USEREVENT, 3000)
        else:
            self.show_warning()


    def show_warning(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "Can't detect license plate!") 
        root.destroy


    def run_app(self):
        while True:
            self.check_event()
            self.update_screen()

if __name__ == "__main__":
    main = Main()
    main.run_app()