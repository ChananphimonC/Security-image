from PIL import Image
import numpy as np
import cv2
import os

def get_bit_stream(message, index):
    return format(ord(message[index]), '08b')


def get_bits(bit_stream, ind):
    # print bit_stream
    if ind == 6:
        last = 0
    else:
        last = int(bit_stream[ind + 2])

    return int(bit_stream[ind]), int(bit_stream[ind + 1]), last


def change_bits(r, g, b, bits, flag=False):
    """

    :type bits: Integer array
    """
    if bits[0]:
        r = r | bits[0]
    else:
        # print "R before", r
        r &= 0b11111110
        # print "R after", r
    if bits[1]:
        g = g | bits[1]
    else:
        g &= 0b11111110

    if not flag:
        if bits[2]:
            b |= bits[2]
        else:
            b &= 0b11111110
    return r, g, b


def append_to_message(pic, img_index):
    r1, g1, b1 = pic[img_index], pic[img_index + 1], pic[img_index + 2]
    r2, g2, b2 = pic[img_index + 3], pic[img_index + 4], pic[img_index + 5]
    r3, g3, b3 = pic[img_index + 6], pic[img_index + 7], pic[img_index + 8]
    char = ""
    char += str(r1 & 0x00000001)
    char += str(g1 & 0x00000001)
    char += str(b1 & 0x00000001)
    char += str(r2 & 0x00000001)
    char += str(g2 & 0x00000001)
    char += str(b2 & 0x00000001)
    char += str(r3 & 0x00000001)
    char += str(g3 & 0x00000001)
    return char


def reshape(pic, w, h):
    pic = np.resize(pic, (int(pic.size / 3), 3))
    pic = pic.reshape((h, w, 3))
    img_copy = Image.fromarray(pic)
    return img_copy

def encrypt(image_path, message):
    # Load image using PIL
    img = Image.open(image_path)
    
    # Convert PIL image to a NumPy array (for OpenCV compatibility)
    img = np.array(img)

    # Check if the image is loaded properly
    if img is None or img.size == 0:
        raise ValueError("Error: Image not found or unable to load.")

    # Get image dimensions (height, width, channels)
    height, width, channels = img.shape
    print(f"Image dimensions: {height}x{width}, Channels: {channels}")

    # Flatten the image to a 1D array for easier pixel manipulation
    pic = img.flatten()

    # Check if the image can hold the message
    max_message_size = (len(pic) // 9) - 3  # Each 9 pixels store 1 character
    if len(message) > max_message_size:
        raise ValueError("Error: Message is too large for the given image.")

    # Convert message length to 24-bit binary
    message_length = len(message)
    bits_l = format(message_length, '024b')

    # Store message length in the last 3 pixels
    pic[-1] = int(bits_l[16:24], 2)
    pic[-2] = int(bits_l[8:16], 2)
    pic[-3] = int(bits_l[0:8], 2)

    msg_index = 0  # Initialize message index

    # Iterate over image pixels in chunks of 9
    for img_index in range(0, len(pic) - 9, 9):
        if msg_index >= len(message):
            break  # Stop when the full message is embedded

        # Get pixel values
        r1, g1, b1 = pic[img_index], pic[img_index + 1], pic[img_index + 2]
        r2, g2, b2 = pic[img_index + 3], pic[img_index + 4], pic[img_index + 5]
        r3, g3, b3 = pic[img_index + 6], pic[img_index + 7], pic[img_index + 8]

        # Convert message character to bit stream
        bit_stream = get_bit_stream(message, msg_index)
        counter = 0

        # Embed bits in three RGB pixel sets
        for ind in range(0, 8, 3):
            bits = get_bits(bit_stream, ind)

            if counter == 0:
                r1, g1, b1 = change_bits(r1, g1, b1, bits)
                pic[img_index], pic[img_index + 1], pic[img_index + 2] = r1, g1, b1
            elif counter == 1:
                r2, g2, b2 = change_bits(r2, g2, b2, bits)
                pic[img_index + 3], pic[img_index + 4], pic[img_index + 5] = r2, g2, b2
            elif counter == 2:
                r3, g3, b3 = change_bits(r3, g3, b3, bits, True)
                pic[img_index + 6], pic[img_index + 7], pic[img_index + 8] = r3, g3, b3
            else:
                print("Unexpected error in bit embedding!")
            counter += 1

        msg_index += 1  # Move to the next character

    # Reshape the image back to its original form
    img_copy = img.reshape((height, width, channels))

    # Convert the modified image back to a PIL Image
    img_copy_pil = Image.fromarray(img_copy.astype(np.uint8))

    # Save the modified image
    save_path = os.path.join("./static", "modified_image.png")
    img_copy_pil.save(save_path)

    print(f"Encrypted image saved at: {save_path}")

    return img_copy_pil

def decode(image):
    img = Image.open(image)
    msg_index = 0
    msg = ""
    pic = (np.array(img))
    # print pic
    pic = pic.flatten()
    length = get_msg_len(pic[-3:])
    print(length)
    for img_index in range(0, pic.size, 9):
        if msg_index == length:
            return msg
        char = append_to_message(pic, img_index)
        msg += str(chr(int(char, 2)))
        msg_index += 1


def get_msg_len(pix):
    s = ""
    for i in range(0, 3):
        s += format(pix[i], '08b')
    return int(s, 2)
