# Encryptr

# Idea

The idea is to send secret messages through images using our web and iOS apps. It is commonly known that images are the most shared resources in today’s world. More than 200 million people over the world use Instagram stories daily and Snapchat sees more than a million snaps created daily. With such a dominating effect of pictures in our lifestyles and everything being in the public domain, we thought of sending more information through this medium than just the image. The sender can selectively send the secret messages to whoever he decides, thus creating an end to end encryption system.

# Working (web app)

# Web App

The web app allows users to to upload a photo and a text message to encrypt in that photo. An interesting exploration of this concept was that only .PNG files work with our code and that is because .PNG files follow lossless compression techniques, thereby saving all of our encrypted data.
Once the user uploads the .PNG file, the file is sent to the flask server where the file is encrypted using our encryption algorithm.
Then there is a web-view in which the user is shown the original and the encrypted images (both looking the same to the naked eye).
The image can then be decrypted by our decryption algorithm, which runs completely independently of the encryption algorithm. Hence the message returned from the decryption algorithm is what it figures out from the decoding the image itself.

![Alt text](https://cloud.githubusercontent.com/assets/6327394/25769693/119e129c-31e6-11e7-9782-c5323c20c17c.png)
![Alt text](https://cloud.githubusercontent.com/assets/6327394/25769711/69f2af70-31e6-11e7-8572-917634dc2929.png)
![Alt text](https://cloud.githubusercontent.com/assets/6327394/25769713/80c75430-31e6-11e7-9120-be2360412529.png)
![Alt text](https://cloud.githubusercontent.com/assets/6327394/25769717/8dfba778-31e6-11e7-880c-3616acc7a1c4.png)


# Encryption Algorithm

We encrypt the secret message in the pixels of the image. Each image is made by multiple pixels, which comprises of R (red), G (green) and B(blue) components. Each of this can have a value between 0 and 255 and is stored in 8 bits. We use these bits to store our message. 
The first step is to convert the message into a bit stream, which we do by appending ASCII characters (in Bits) of the message characters. Each character of the input message is 8 bits and hence we need 8 least significant bits to encrypt the message. The algorithm then iterates over each pixel of the image and stores a character in three pixels (3 RGB sets, hence 9 Bit Packets with 9 least significant bits), with one bit of the character replacing the least significant bit of one of the RGB bits.
We also store the length of the message in the last pixel of the image. That’s 24 bits, and can store message lengths of upto 2 ^ 24 characters (if the image is big enough). The message length is converted into bits and it completely replaces the last pixel bits, with the length bits and leading 0’s. In the decryption algorithm, we first decode the length of the message from the last pixel, then we iterate for that length over the image, take “bit packets” and convert those bits into characters and hence retrieve the message. 
