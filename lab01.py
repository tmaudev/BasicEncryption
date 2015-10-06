# Lab 1
# Tyler Mau
# September 25, 2015

from Crypto.Cipher import AES
import array

# XORs Two Strings
def xor_str(str1, str2):
   if len(str1) != len(str2):
      print "Error: Strings not same length"
      return -1

   data1 = array.array('B', str1)
   data2 = array.array('B', str2)

   for i in range(len(data1)):
      data1[i] ^= data2[i]

   return data1.tostring()

# Encodes File Using One-Time-Pad
def encode_otp(filename, output_filename, key = 0):
	# Open File for Reading
   my_file = open(filename, 'r')

	# Get String Data from File
   file_str = my_file.read()
   my_file.close()

	# Get Appropriate Length of Random Data for Key
   file_len = len(file_str)
   if key == 0:
      rand_file = open('/dev/urandom', 'rb')
      rand_data = rand_file.read(file_len)
      rand_file.close()
   else:
      rand_data = key

	# Encode File Data
   encoded_str = xor_str(file_str, rand_data)

	# Save Encoded Data to Output File
   file_out = open(output_filename, 'wb')
   file_out.write(encoded_str)
   file_out.close()

   return rand_data

# Decodes Encoded Data
def decode(filename, key):
   encoded_file = open(filename, 'rb')
   encoded_str = encoded_file.read()
   encoded_file.close()
   decoded_str = xor_str(encoded_str, key)
   return decoded_str

# Encodes BMP Image File
def encode_bmp(filename, output_filename, key = 0):
   my_img = open(filename, 'rb')
   header = my_img.read(54)
   my_img.close()

   if key == 0:
      key = encode_otp(filename, output_filename)
   else:
      encode_otp(filename, output_filename, key)

   encoded_img = open(output_filename, "r+b")
   encoded_img.seek(0)
   encoded_img.write(header)
   encoded_img.close()
   return key

# Decodes BMP Image File
def decode_bmp(filename, key):
   encoded_img = open(filename, 'rb')
   header = encoded_img.read(54)
   encoded_img.seek(0);
   encoded_str = encoded_img.read()
   encoded_img.close()

   decoded_str = xor_str(encoded_str, key)
   decoded_img = open("decoded_" + filename, 'wb')
   decoded_img.write(decoded_str)
   decoded_img.close()

   decoded_img = open("decoded_" + filename, "r+b")
   decoded_img.seek(0)
   decoded_img.write(header)
   decoded_img.close()
   return

def xor_images(img1, img2, output_file):
   encoded1 = open(img1, 'rb')
   header = encoded1.read(54)
   encoded1.seek(0)
   img1_str = encoded1.read()
   encoded1.close()

   encoded2 = open(img2, 'rb')
   img2_str = encoded2.read()
   encoded2.close()

   xor_img = xor_str(img1_str, img2_str)
   combined_img = open(output_file, 'wb')
   combined_img.write(xor_img)
   combined_img.close()

   combined_img = open(output_file, "r+b")
   combined_img.seek(0)
   combined_img.write(header)
   combined_img.close()

   return

def AES_128(data, key, iv = ''):
   cipher = AES.new(key, AES.MODE_ECB, iv)
   encoded_data = cipher.encrypt(data)
   return encoded_data

def ecb_encode(filename, output_filename):
   rand_file = open("/dev/urandom", 'r')
   key = rand_file.read(16)
   rand_file.close()

   output_file = open(output_filename, 'wb')

   data_file = open(filename, "rb")
   data = data_file.read(16)
   data_len = len(data)

   while data_len == 16:
      encoded_data = AES_128(data, key)
      output_file.write(encoded_data)
      data = data_file.read(16)
      data_len = len(data)

   pad_len = 16 - data_len

   if pad_len < 10:
      pad_str = ('0' + str(pad_len)) * pad_len
   else:
      pad_str = ('' + str(pad_len)) * pad_len

   final_data = data + pad_str.decode("hex")
   encoded_data = AES_128(final_data, key)
   output_file.write(encoded_data)
   output_file.close()

   return

def ecb_bmp(filename, output_filename):
   img = open(filename, 'rb')
   header = img.read(54)
   img.close()

   ecb_encode(filename, output_filename)
   encoded_img = open(output_filename, 'r+b')
   encoded_img.seek(0)
   encoded_img.write(header)
   encoded_img.close()

   return

def cbc_encode(filename, output_filename):
   rand_file = open("/dev/urandom", 'r')
   key = rand_file.read(16)
   rand_file.close()

   rand_file = open("/dev/urandom", 'r')
   iv = rand_file.read(16)
   rand_file.close()

   output_file = open(output_filename, 'wb')

   data_file = open(filename, "rb")
   data = data_file.read(16)
   data_len = len(data)

   while data_len == 16:
      input_data = xor_str(data, iv)
      encoded_data = AES_128(input_data, key, iv)
      iv = encoded_data
      output_file.write(encoded_data)
      data = data_file.read(16)
      data_len = len(data)

   pad_len = 16 - data_len

   if pad_len < 10:
      pad_str = ('0' + str(pad_len)) * pad_len
   else:
      pad_str = ('' + str(pad_len)) * pad_len

   final_data = data + pad_str.decode("hex")
   final_input = xor_str(final_data, iv)
   encoded_data = AES_128(final_data, key, iv)
   output_file.write(encoded_data)
   output_file.close()

   return

def cbc_bmp(filename, output_filename):
   img = open(filename, 'rb')
   header = img.read(54)
   img.close()

   cbc_encode(filename, output_filename)
   encoded_img = open(output_filename, 'r+b')
   encoded_img.seek(0)
   encoded_img.write(header)
   encoded_img.close()

   return

def string_test():
   # Get File for Encoding from User Input
   filename = raw_input("Enter File: ")
   output_filename = raw_input("Enter Output: ")
   print

   # Encode Data
   key = encode_otp(filename, output_filename)

   # Test Decode
   decoded_str = decode(output_filename, key)
   print "Decoded String"
   print decoded_str
   return

def image_test():
   img_key = encode_bmp("mustang.bmp", "mustang_encoded.bmp")
   decode_bmp("mustang_encoded.bmp", img_key)
   encode_bmp("cp-logo.bmp", "cp-logo_encoded.bmp", img_key)

   xor_images("mustang_encoded.bmp", "cp-logo_encoded.bmp", "combined.bmp")
   return

def ecb_test():
   ecb_bmp("mustang.bmp", "mustang_encoded_ecb.bmp")
   return

def cbc_test():
   cbc_bmp("mustang.bmp", "mustang_encoded_cbc.bmp")
   return

# --------------------------------- MAIN --------------------------------- 

# Menu
menu = """
   What would you like to do?
   s - Encrypt Text File with OTP
   b - Encrypt BMP Images and Combine
   e - Encrypt Image with ECB
   c - Encrypt Image with CBC
   r - Run All"
   q - Quit
>>> """

# User Prompt
user_input = raw_input(menu)

if user_input == "s":
   string_test()
elif user_input == "b":
   image_test()
elif user_input == "e":
   ecb_test()
elif user_input == "c":
   cbc_test()
elif user_input == "r":
   string_test()
   image_test()
   ecb_test()
   cbc_test()
elif user_input == "q":
   print "Goodbye!\n"
else:
   print "Invalid Choice"

