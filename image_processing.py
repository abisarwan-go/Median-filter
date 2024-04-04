from tkinter import filedialog, Tk, Button
from PIL import Image

class ImageProcessing:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.button_explore = Button(self.root, text= "Browse Files", command= self.browse_files)
        self.button_explore.pack()

    def browse_files(self):
        file_path = filedialog.askopenfilename(
        title= "Select a File",
        filetypes=(("image files", "*.png *.jpg *.jpeg *.bmp")
                   ,("all files", "*.*")
        ))
        self.read_image(file_path)

    def read_image(self, file_path):
        img = Image.open(file_path)
        self.format_file = img.format
        print('format file' + self.format_file)
        img = img.convert('L')
        pixels = img.load()
        width, height = img.size
        self.filter_median(pixels, width, height)

    def filter_median(self, pixels, width, height):
        image_rsl = [[0 for _ in range(height)] for _ in range(width)]
        print(f'width = {width}, height = {height}')
        for i in range(0, width):
            for j in range(0, height):
                arr = [0] * 9
                if i - 1 >= 0 and j - 1 >= 0:
                    arr[0] = pixels[i - 1, j - 1]
                if i - 1 >= 0 and j >= 0:
                    arr[1] = pixels[i - 1, j]
                if i - 1 >= 0 and j + 1 < height:
                    arr[2] = pixels[i - 1, j + 1]
                if i >= 0 and j - 1 >= 0:
                    arr[3] = pixels[i, j - 1]
                if i >= 0 and j >= 0:
                    arr[4] = pixels[i, j]
                if i >= 0 and j + 1 < height:
                    arr[5] = pixels[i, j + 1]
                if i + 1 < width and j - 1 >= 0:
                    arr[6] = pixels[i + 1, j - 1]
                if i + 1 < width and j >= 0:
                    arr[7] = pixels[i + 1, j]
                if i + 1 < width and j + 1 < height:
                    arr[8] = pixels[i + 1, j + 1]
                sorted_arr = sorted(arr)
                median = sorted_arr[4]
                image_rsl[i][j] = median
        self.create_image(image_rsl, width, height)
    
    def create_image(self, image_rsl, width, height):
        new_img = Image.new('L', (width, height))
        for i in range(width):
            for j in range(height):
                new_img.putpixel((i, j), image_rsl[i][j])
        new_img.show()
        try: 
            new_img.save('output_image.' + self.format_file)
        except Exception as e:
            print(f'Error saving image {e}')

if __name__ == "__main__":
    root = Tk()
    root.title('Image Processing')
    root.geometry("200x200")
    app = ImageProcessing(root)
    root.mainloop()
