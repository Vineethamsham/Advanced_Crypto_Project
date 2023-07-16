from django.shortcuts import render,redirect
from .models import*
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.db import connection
import cv2
import numpy as np
from datetime import datetime
from Crypto.Cipher import DES3
import binascii

#Required Libraries importing
from Crypto.Cipher import DES
from Crypto.Hash import SHA256
import turtle
import requests
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
import pytz
from datetime import datetime

Key_length=100005
salt="$ez*&214097GDAKACNASC;LSOSSBAdjskasnmosuf!@#$^()_adsa"

def home(request):
	return render(request,"home.html",{})

def Info(request):
	return render(request,"Info.html",{})

'''def messageToBinary(message):
    if isinstance(message, str):
        return ''.join([format(ord(i), "08b") for i in message])
    elif isinstance(message, (bytes, np.ndarray)):
        return [format(i, "08b") for i in message]
    elif isinstance(message, int) or isinstance(message, np.uint8):
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported")
    
def hideData(image, key):
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("Maximum bytes to encode:", n_bytes)

    if len(secret_message) > n_bytes:
        raise ValueError("Error encountered: insufficient bytes, need a bigger image or less data!")

    secret_message += "#####" # you can use any string as the delimiter

    data_index = 0
    binary_secret_msg = messageToBinary(secret_message)

    data_len = len(binary_secret_msg)
    for values in image:
        for pixel in values:
            r, g, b = messageToBinary(pixel)

            if data_index < data_len:
                pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1

            if data_index >= data_len:
                break

    return image

def showData(image):
    binary_data = ""
    for values in image:
        for pixel in values:
            r, g, b = messageToBinary(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]

    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "#####":
            break

    return decoded_data[:-5]'''

def encrypt_data(data, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    padded_data = pad_data(data)
    encrypted_data = cipher.encrypt(padded_data)
    encrypted_data_hex = binascii.hexlify(encrypted_data).decode()
    return encrypted_data_hex

def decrypt_data(data, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    encrypted_data = binascii.unhexlify(data.encode())
    decrypted_data = cipher.decrypt(encrypted_data)
    decrypted_data = unpad_data(decrypted_data).decode()
    return decrypted_data

def pad_data(data):
    block_size = DES3.block_size
    pad_len = block_size - (len(data) % block_size)
    padding = bytes([pad_len] * pad_len)
    padded_data = data.encode() + padding
    return padded_data

def unpad_data(data):
    pad_len = data[-1]
    unpadded_data = data[:-pad_len]
    return unpadded_data

def generate_unique_image_name():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    encrypt_image_name = f"image_{timestamp}.png"
    return encrypt_image_name

def decode(request,id):
   return render(request, 'decode.html', {'id':id})




def User_Login(request):
	if request.method == "POST":
		C_name = request.POST['aname']
		C_password = request.POST['apass']
		if userDetails.objects.filter(Username=C_name,Password=C_password).exists():
			users = userDetails.objects.all().filter(Username=C_name,Password=C_password)
			messages.info(request,C_name +' logged in')
			request.session['UserId'] = users[0].id
			#request.session['next_id'] = next_id
			request.session['type_id'] = 'User'
			request.session['UserType'] = C_name
			request.session['login'] = "Yes"
			return redirect('/')
		else:
			messages.info(request, 'Please Register')
			return redirect("/User_Registration")
	else:
		return render(request,'User_Login.html',{})

def User_Registration(request):
	if request.method == "POST":
		
		Name= request.POST['name']
		Age= request.POST['age']
		Phone= request.POST['phone']
		Email= request.POST['email']
		Address= request.POST['address']
		Username= request.POST['Username']
		Password= request.POST['Password']
		if userDetails.objects.all().filter(Username=Username).exists():
			messages.info(request,"Username Taken")
			return redirect('/User_Registration')
		else:
			obj = userDetails(
			Name=Name
			,Age=Age
			,Phone=Phone
			,Email=Email
			,Address=Address
			,Username=Username
			,Password=Password)
			obj.save()
			messages.info(request,Name+" Registered")
			return redirect('/User_Login')
	else:
		return render(request,"User_Registration.html",{})


def Logout(request):
	Session.objects.all().delete()
	return redirect("/")


def view_file(request):
    current_user = request.session['UserType']
    print(current_user)
    secret_files = filedetails.objects.filter(User_name=current_user)
    print(secret_files)
    return render(request, "view_file.html", {'secret_files': secret_files})



def send_file(request):
    if request.method == 'POST':
        try:
            last_id = filedetails.objects.latest('id').id
            next_id = last_id + 1
            print('next id:', next_id)
        except filedetails.DoesNotExist:
            next_id = 1

        #secret_msg=request.POST['secret_msg']
        image = request.FILES['image']
        key_enc = request.POST['key']
        username = request.POST['user']
        request.session['next_id'] = next_id
        print(next_id)
        # Define the target timezone
        target_timezone = pytz.timezone('US/Eastern')
        current_time = datetime.now(target_timezone)

        # Format the time as a string
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        # Save the file details in the database
        filedetails.objects.create(image=image, key=key_enc, User_name=username,
                                   sender_name=request.session['UserType'], created_at=formatted_time)
        image_name = filedetails.objects.all().filter(id = next_id)
        print(image_name[0].image)
        image_name1 = image_name[0].image
        print(image_name1)
        image_path='C:/workspace/stegnography/stegnography/media/' + str(image_name1)
        print(image_path)
        #Opening the image file
        try:
            with open(image_path, 'rb') as imagefile:
                image=imagefile.read()
                
            #Padding    
            while len(image)%8!=0:
                image+=b" "
        except:
            print("Error loading the file, make sure file is in same directory, spelled correctly and non-corrupted")
            exit()
        #hashing original image in SHA256   
        hash_of_original=SHA256.new(data=image)
        #Salting and hashing password
        key_enc=PBKDF2(key_enc,salt,48,Key_length)
        print(key_enc)
        #Encrypting using triple 3 key DES  
        print("Wait it is being encrypting.....\n") 
        try:
            
            cipher1=DES.new(key_enc[0:8],DES.MODE_CBC,key_enc[24:32])
            ciphertext1=cipher1.encrypt(image)
            cipher2=DES.new(key_enc[8:16],DES.MODE_CBC,key_enc[32:40])
            ciphertext2=cipher2.decrypt(ciphertext1)
            cipher3=DES.new(key_enc[16:24],DES.MODE_CBC,key_enc[40:48])
            ciphertext3=cipher3.encrypt(ciphertext2)
            
            print("\n------ENCRYPTION SUCCESSFUL-------")
        except:
            print(" Encryption failed...Possible causes:Library not installed properly/low device memory/Incorrect padding or conversions")
            exit()
        
        #Adding hash at end of encrypted bytes
        ciphertext3+=hash_of_original.digest()

        
        #Saving the file encrypted
        try:
            encrypted_image_name = generate_unique_image_name()
            dpath = 'media/encrypt_image/' + encrypted_image_name
            print(dpath)
            #dpath="encrypted_"+path
            with open(dpath, 'wb') as image_file:
                    image_file.write(ciphertext3)
            print("Encrypted Image Saved successfully as filename "+dpath)

            
        except:
            temp_path=input("Saving file failed!. Enter alternate name without format to save the encrypted file. If it is still failing then check system memory")
            try:
                dpath=temp_path+path
                dpath="encrypted_"+path
                with open(dpath, 'wb') as image_file:
                        image_file.write(ciphertext3)
                print("Encrypted Image Saved successfully as filename in the same directory "+dpath)
                exit()
            except:
                print(" Failed....Exiting...")
                exit()


        file_name = filedetails.objects.all().filter(id = next_id)
        '''encoded_image = hideData(resized_image,key)
        print(encoded_image)'''
        #
        
        #cv2.imwrite(encrypted_image_path, encoded_image)
        file_name = filedetails.objects.all().filter(id = next_id).update(encrypt_image = dpath)
        '''image = cv2.imread(encrypted_image_path)
                                print("The steganographed image is as shown below:")
                                resized_image = cv2.resize(image, (500, 500))
                                cv2.imshow("Steganographed Image", resized_image)
                                cv2.waitKey(0)
                                cv2.destroyAllWindows()'''
        '''text = showData(resized_image)
        print(text)'''

        user_name = request.session['UserType']
        users = userDetails.objects.all().exclude(Username = user_name)
        print(users)
        message = "File sent sucessfully to" + ' '+ str(username)
        messages.error(request, message)
        return render(request, 'send_file.html', {'users': users})
    else:
        user_name = request.session['UserType']
        users = userDetails.objects.all().exclude(Username = user_name)
        print(users)
        return render(request, 'send_file.html', {'users': users})







def image_decode(request):
   if request.method == 'POST':
        file_id = request.POST.get('file_id')
        print(file_id)
        key = request.POST.get('key')
        print(key)
        if filedetails.objects.filter(id=file_id,key=key).exists():
            msg = filedetails.objects.all().filter(id=file_id,key=key)
            print(msg)
            file_name = msg[0].encrypt_image
            path = "C:/workspace/stegnography/stegnography/" +str(file_name)
            print(path)
            #img = file_name.path

            try:
                with open(path,'rb') as encrypted_file:
                    encrypted_data_with_hash=encrypted_file.read()
                    
            except:
                print(" Unable to read source cipher data. Make sure the file is in same directory...Exiting...")
                exit()
            
            
            #Key Authentication
            key_dec=key
            #extracting hash and cipher data without hash
            extracted_hash=encrypted_data_with_hash[-32:]
            encrypted_data=encrypted_data_with_hash[:-32]

            
            #salting and hashing password
            key_dec=PBKDF2(key_dec,salt,48,Key_length)
            

            #decrypting using triple 3 key DES
            print(" Decrypting...")
            try:
        
                cipher1=DES.new(key_dec[16:24],DES.MODE_CBC,key_dec[40:48])
                plaintext1=cipher1.decrypt(encrypted_data)
                cipher2=DES.new(key_dec[8:16],DES.MODE_CBC,key_dec[32:40])
                plaintext2=cipher2.encrypt(plaintext1)
                cipher3=DES.new(key_dec[0:8],DES.MODE_CBC,key_dec[24:32])
                plaintext3=cipher3.decrypt(plaintext2)
                
                
            except:
                print("Decryption failed...Possible causes:Library not installed properly/low device memory/Incorrect padding or conversions")
                
            #hashing decrypted plain text
            hash_of_decrypted=SHA256.new(data=plaintext3)

            
            #matching hashes
            if hash_of_decrypted.digest()==extracted_hash:
                print("Password Correct !!!")
                print(" ------DECRYPTION SUCCESSFUL------")
            else:
                print("Incorrect Password!!!!!")
                exit()
                
                
                
            #saving the decrypted file  
            try:
                encrypted_image_name = generate_unique_image_name()

                epath='C:/workspace/stegnography/stegnography/media/decrypt/' + "decrypted_" + encrypted_image_name
                print(epath)
                with open(epath, 'wb') as image_file:
                    image_file.write(plaintext3)
                print(" Image saved successully with name " + epath)
            except:
                temp_path=input("Saving file failed!. Enter alternate name without format to save the decrypted file. If it is still failing then check system memory")
                try:
                    epath=temp_path+dpath
                    with open(epath, 'wb') as image_file:
                        image_file.write(plaintext3)
                    print(" Image saved successully with name " + epath)
                    print(" Note: If the decrypted image is appearing to be corrupted then password may be wrong or it may be file format error")
                except:
                    print("Failed! Exiting...")
                    exit()
            #decryptor(file_name)
            '''encrypted_image_path = 'D:/stegnography using triple DES/stegnography/media/encrypt_image/' + str(file_name)
            print(encrypted_image_path)'''
            image = cv2.imread(str(file_name))
            print("The steganographed image is as shown below:")
            #epath = 'C:/workspace/stegnography/stegnography/' + str(epath)
            filedetails.objects.filter(id=file_id,key=key).update(secret_msg = epath)
            data = filedetails.objects.filter(id=file_id,key=key)
            #print(epath)
            
            return render(request, 'decode.html', {'data':data})
        else:
            # Key doesn't match, show an error message
            message = "Invalid key. Please try again."
            messages.error(request, message)
            return redirect('/view_file')
            
   else:
        return render(request, 'decode.html')