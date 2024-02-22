import cv2
import os


images = [ f'images/{img_path}' for img_path in os.listdir('images') ]

for img_path in images:
    img = cv2.imread(img_path)
    print(img.shape, img_path)
    

png = cv2.imread('images/dalle_duck.png')
jpg = cv2.imread('images/dalle_duck.jpg')
bmp = cv2.imread('images/dalle_duck.bmp')


def encode_message_to_binary(message: str, encoding: str='utf-8') -> str:
    message_utf8 = message.encode(encoding)
    message_binary = [ format(byte, '08b') for byte in message_utf8 ]
    binary_array = ''.join(message_binary)
    return binary_array

def decode_binary_to_message(binary_array: str, encoding: str='utf-8') -> str:
    message_binary_splitted = [ binary_array[ i:i+8 ] for i in range(0, len(binary_array), 8) ]
    print('asdsadas', b'\0')
    print(binary_array[:160])
    bytes_array = bytes([ int(binary, 2) for binary in message_binary_splitted ])
    bytes_array = bytes_array.split(b'\0')[0]
    message = bytes_array.decode(encoding)
    return message


message = 'Hello, World! 🌍'
print(message)
encoded = encode_message_to_binary(message)
print(encoded)
decoded = decode_binary_to_message(encoded)
print(decoded)


def encode_image(img, message):
    encoded_message = encode_message_to_binary(message + '\0')
    index = 0
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            for k in range(0, 3):
                if index < len(encoded_message):
                    img[i, j, k] = img[i, j, k] & 0b11111110 | int(encoded_message[index])
                    index += 1
                else:
                    break

def decode_image(img):
    decoded_message = ''
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            for k in range(0, 3):
                decoded_message += str(img[i, j, k] & 1)
    
    # print(decoded_message)
    return decode_binary_to_message(decoded_message)


for img in [ png ]:
    encode_image(img, 'Hello, world! 🌍')
    
    decoded = decode_image(img)
    print('decoded', decoded)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    