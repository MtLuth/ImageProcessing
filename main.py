from tkinter import Tk, Canvas

class MainDisplay:

    def __init__(self):
        self.width = 1200
        self.height = 800
        self.root = Tk()
        self.root.title("Image Processing")
        self.root.geometry(str(self.width) + "x" + str(self.height))

    def run(self):
        self.input_image = Canvas()
        self.root.mainloop()

if __name__ == '__main__':
    main = MainDisplay()
    main.run()