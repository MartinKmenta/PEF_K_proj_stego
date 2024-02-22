import cv2
import os


images = [ f'images/{img_path}' for img_path in os.listdir('images') ]

for img_path in images:
    img = cv2.imread(img_path)
    print(img.shape, img_path)
    

png = cv2.imread('images/dalle_duck.png')
jpg = cv2.imread('images/dalle_duck.jpg')
bmp = cv2.imread('images/dalle_duck.bmp')


def encode_message_to_binary(message: str) -> str:
    message_utf8 = message.encode('utf-8')
    message_binary = [ format(byte, '08b') for byte in message_utf8 ]
    binary_array = ''.join(message_binary)
    return binary_array

def decode_binary_to_message(binary_array: str) -> str:
    message_binary_splitted = [ binary_array[ i:i+8 ] for i in range(0, len(binary_array), 8) ]
    bytes_array = bytes([ int(binary, 2) for binary in message_binary_splitted ])
    message = bytes_array.decode('utf-8')
    return message



message = 'Hello, World! 🌍'
print(message)
encoded = encode_message_to_binary(message)
print(encoded)
decoded = decode_binary_to_message(encoded)
print(decoded)



exit()

def encode_image(img, message):
    
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            for k in range(0, 3):
                img[i, j, k] = img[i, j, k] & 0b11111110



for img in [ png, jpg, bmp ]:
    encode_image(img, 'Hello, world! 🌍')
    
    cv2.imshow('image', img)
    cv2.waitKey(0)
