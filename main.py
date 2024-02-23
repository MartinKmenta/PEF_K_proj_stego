from typing import Tuple

import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
import sys
import io
import base64
import main
from tqdm import tqdm
    
images_path = 'images'
init_message = 'Hello, World! 🌍'

class App:
    def __init__(self, root):
        self.log_counter = 0
        
        self.root = root
        self.root.title('Steganography')
        self.root.geometry('800x700')
        self.root.resizable(True, True)
        
        self.img_path = tk.StringVar()
        self.output = tk.StringVar()
        
        self.img_path.set('path/to/image.png|bmp')
        
        self.label_img = tk.Label(self.root, text='Image')
        self.label_img.grid(row=0, column=0)
        self.input_img = tk.Entry(self.root, textvariable=self.img_path)
        self.input_img.grid(row=0, column=1, sticky='we')
        self.button_img = tk.Button(self.root, text='Browse', command=self.browse_image)
        self.button_img.grid(row=0, column=2)
        
        self.label_message = tk.Label(self.root, text='Message')
        self.label_message.grid(row=1, column=0)
        self.message = tk.Text(self.root, wrap="word", height=5, width=80)  # Multiline Text widget
        self.message.grid(row=1, column=1, rowspan=2)
        self.message.insert(1.0, init_message)
        
        self.button_encode = tk.Button(self.root, text='Encode', command=self.encode)
        self.button_encode.grid(row=1, column=2)
        self.button_encode = tk.Button(self.root, text='Decode', command=self.decode)
        self.button_encode.grid(row=2, column=2)
        
        self.label_output = tk.Label(self.root, text='Log')
        self.label_output.grid(row=3, column=0)
        self.text_output = tk.Text(self.root, height=10, width=80)
        self.text_output.grid(row=3, column=1, columnspan=1)
        
        self.image = ImageTk.PhotoImage(Image.new('RGB', (400, 400), (255, 255, 255)))
        self.label_image = tk.Label(self.root, image=self.image)
        self.label_image.grid(row=4, column=0, columnspan=3)
        
            
    def log(self, message: str) -> None:
        self.log_counter += 1
        print(f'{self.log_counter}: {message}')
        self.text_output.insert(1.0, f'{self.log_counter}: {message}\n')
    
    
    def browse_image(self):
        self.img_path.set(filedialog.askopenfilename(initialdir=images_path))
        image = None
        try:
            image = Image.open(self.img_path.get())
            image.thumbnail((400, 400))
            image = ImageTk.PhotoImage(image)
            
        except Exception as e:
            self.log('Image could not be opened' + '\n' + str(e))
            image = Image.new('RGB', (400, 400), (255, 255, 255))
        
        
        self.image = image
        self.label_image.config(image=self.image)
        
        
    def encode(self):
        image = None
        try:
            image = cv2.imread(self.img_path.get())
            
        except Exception as e:
            self.log('Image could not be opened' + '\n' + str(e))
            return
        
        message = self.message.get(1.0, tk.END)
        state, message = self.encode_image(image, message)
        if state:
            self.log('Message encoded successfully')
                
            filename = filedialog.asksaveasfilename(initialfile='encoded_image', 
                        defaultextension='.png', filetypes=[('PNG', '*.png'), ('BMP', '*.bmp')])
            if filename:
                try:
                    cv2.imwrite(filename, image)
                    self.log('Image saved successfully')
                    
                except Exception as e:
                    self.log('Image could NOT be saved' + '\n' + str(e))
            
            else:
                self.log('Image could NOT be saved, please provide valid path.')
                
        else:
            self.log(message)
            self.log('Message could NOT be encoded')
            
            
            
    def decode(self):
        image = None
        try:
            image = cv2.imread(self.img_path.get())
            
        except Exception as e:
            self.log('Image could NOT be opened' + '\n' + str(e))
            return
        
        state, message = self.decode_image(image)
        if state:
            self.log('Message decoded successfully')
            self.message.delete(1.0, tk.END)
            self.message.insert(1.0, message)
            
        else:
            self.log(message)
            self.log('Message could NOT be decoded')
        

    @staticmethod
    def encode_message_to_binary(message: str, encoding: str='utf-8') -> str:
        message_utf8 = ''
        message_utf8 = message.encode(encoding)
        message_binary = [ format(byte, '08b') for byte in message_utf8 ]
        binary_array = ''.join(message_binary)
        return binary_array


    @staticmethod
    def decode_binary_to_message(binary_array: str, encoding: str='utf-8') -> str:
        message_binary_splitted = [ binary_array[ i:i+8 ] for i in range(0, len(binary_array), 8) ]
        bytes_array = bytes([ int(binary, 2) for binary in message_binary_splitted ])
        bytes_array_splitted = bytes_array.split(b'\0')[0]
        message = bytes_array_splitted.decode(encoding)
        return message


    @staticmethod
    def encode_image(img:np.ndarray, message, encoding: str='utf-8') -> Tuple[ bool, str ]:
        encoded_message = ''
        try:
            encoded_message = App.encode_message_to_binary(message + '\0', encoding)
            
        except UnicodeEncodeError as e:
            return (False, str(e))
        
        index = 0
        progress = tqdm(total=len(encoded_message))
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                for k in range(0, 3):
                    if index < len(encoded_message):
                        img[i, j, k] = img[i, j, k] & 0b11111110 | int(encoded_message[index])
                        index += 1
                        progress.update(1)
                    else:
                        progress.close()
                        return (True, '')
        
        progress.close()
        return (False, 'Message could not be encoded, too large for the image.')
            
            
    @staticmethod
    def decode_image(img:np.ndarray, encoding: str='utf-8') -> Tuple[ bool, str ]:
        decoded_message = ''
        bytes_array = ''
        for i in tqdm(range(0, img.shape[0])):
            for j in range(0, img.shape[1]):
                for k in range(0, 3):
                    bytes_array += str(img[i, j, k] & 1)
        
        try:
            decoded_message = App.decode_binary_to_message(bytes_array, encoding)
            
        except UnicodeDecodeError as e:
            return (False, str(e))
        
        return (True, decoded_message)


def test_encoding_message():
    message = 'Hello, World! 🌍'
    encoded = App.encode_message_to_binary(message)
    decoded = App.decode_binary_to_message(encoded)
    assert message == decoded
    print('Test test_encoding_message passed!')


def test_encoding_message_to_image():
    message = 'Hello, World! 🌍'
    img = cv2.imread('images/dalle_duck.png')
    state1, _ = App.encode_image(img, message)
    assert state1
    state2, message2 = App.decode_image(img)
    assert state2
    assert message == message2
    print('Test test_encoding_message_to_image passed!')


if __name__ == '__main__':
    
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-m', '--message', type=str, default='', help='Message')
    parser.add_argument('-e', '--encode', type=str, default='', help='Encode message')
    parser.add_argument('-d', '--decode', type=str, default='', help='Decode message')
    parser.add_argument('-i', '--image', type=str, default='', help='Image path')
    parser.add_argument('-t', '--test', action='store_true', help='Run tests')
    parser.add_argument('-g', '--gui', action='store_true', help='Run GUI')
    args = parser.parse_args()
    
    if len(sys.argv) <= 1 or args.gui:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
        
    elif args.test:
        test_encoding_message()
        test_encoding_message_to_image()
        
    elif args.message:
        print(App.encode_message_to_binary(args.message))
    
    
    
    