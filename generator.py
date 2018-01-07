from image import ImageCaptcha
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
import os

number = ['0','1','2','3','4','5','6','7','8','9']
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def random_captcha_text(char_set=number+alphabet+ALPHABET, captcha_size=4):
	captcha_text = []
	for i in range(captcha_size):
		c = random.choice(char_set)
		captcha_text.append(c)
	return captcha_text

def gen_captcha_text_and_image():
	image = ImageCaptcha()

	captcha_text = random_captcha_text()
	captcha_text = ''.join(captcha_text)

	captcha = image.generate(captcha_text)

	captcha_image = Image.open(captcha)
	captcha_image = np.array(captcha_image)
	return captcha_text, captcha_image

def new_captcha():
	text, image = gen_captcha_text_and_image()
	f = plt.figure()
	plt.axis('off')
	plt.imshow(image)
	plt.savefig('./pics/'+text+'.png')

	newimage=Image.open('./pics/'+text+'.png')
	newimage=newimage.crop((70,140,570,340))
	return text, newimage

if __name__ == '__main__':
	new_captcha()