# 🔐 Image Encryption & Decryption System using Triple DES

This project implements a **secure image encryption and decryption system** using the **Triple DES (3DES)** algorithm, built with the Django framework. It enables users to securely transmit images using a web-based platform, protecting sensitive image data from unauthorized access or tampering.

---

## 🧩 Project Objective

To provide a robust, web-based cryptographic system that:
- Encrypts and decrypts images using **Triple DES** for enhanced security
- Ensures the **confidentiality, integrity, and availability** of sensitive visual information
- Facilitates secure image transmission over networks

---

## 🔒 What is Triple DES?

Triple DES (3DES or TDEA) is a symmetric encryption algorithm that applies the **DES cipher three times** to each data block using a unique 3-key structure:

- **Encryption**: `EK3(DK2(EK1(PlainText)))`
- **Decryption**: `DK1(EK2(DK3(CipherText)))`

This technique improves upon the original DES, offering a **168-bit key length** for greater resistance to brute-force attacks.

---

## 🌐 System Architecture

### 💻 Frontend:
- **HTML, CSS, JavaScript** – for user interface design

### 🖥 Backend:
- **Python (Django Framework)** – implements encryption logic
- **MySQL** – handles user data, file tracking, and secure key storage

### 🔄 Features:
- ✅ User registration and login with validation
- ✅ Upload, encrypt, and transmit image files using Triple DES
- ✅ Secure key-based decryption for recipients
- ✅ File tracking (sent/received), role-based access
- ✅ Bit-level image manipulation and steganographic LSB embedding

---

## 🛠 Technologies Used

| Category    | Tools & Frameworks               |
|-------------|----------------------------------|
| Language    | Python                           |
| Framework   | Django                           |
| Frontend    | HTML, CSS, JavaScript            |
| Database    | MySQL                            |
| Server      | XAMPP (Apache + MySQL)           |
| Encryption  | Triple DES (DES x3 with 3 keys)  |

---

## 🧪 System Workflow

1. **User Registration/Login** – Validate identity
2. **Image Upload** – Choose file + enter 3DES key
3. **Encryption Process** – Convert image to binary → apply 3DES with Key1, Key2, Key3
4. **Secure Transmission** – Send encrypted image to recipient
5. **Decryption Process** – Recipient enters key → decrypt image using reverse 3DES

---

## 🔐 Security Highlights

- **168-bit encryption** with Triple DES (K1-K2-K3 key sequence)
- **LSB data embedding** for secure image hiding
- Ensures **confidentiality, integrity, and privacy** even if images are intercepted
- Designed for **medical imaging, military files, and private media sharing**

---

## 📦 Modules

| Module         | Description |
|----------------|-------------|
| User           | Register/Login, session management |
| Send File      | Upload image + encrypt with 3DES |
| Receive File   | View received encrypted files |
| Decrypt File   | Enter key to decrypt and retrieve original image |

---

## 📊 Applications

- 📡 **Secure Image Transmission** (military, healthcare, legal)
- ☁️ **Encrypted Image Archiving** (cloud storage, databases)
- 🧬 **Medical Imaging** (sensitive patient diagnostics)
- 🔒 **Confidential Media Sharing** (social networks, intelligence)

---

## 🧠 Key Takeaways

- Triple DES still provides **strong encryption** for specific use cases
- Proper **key management and secure front-end/backend integration** are critical
- Cryptography can be implemented efficiently in **full-stack Django apps**

---

## 📁 How to Run the Project

1. Create a virtual environment:  
   `python -m venv venv && venv\Scripts\activate`

2. Start XAMPP → enable **Apache** and **MySQL**

3. Run the Django server:  
   `python manage.py runserver`

4. Visit `http://localhost:8000/` in your browser to register, upload, and encrypt images

---

## 👨‍💻 Authors

- Vineeth Amsham   

📎 [Project Report PDF](https://github.com/Vineethamsham/Advanced_Crypto_Project/blob/main/CS7530_W01_Advanced_Cryptography_Group_4_Project_Final_Report.pdf))

---

## 📚 References

1. [NIST - Triple DES Standard](https://csrc.nist.gov/publications/detail/fips/46/3/archive/1999-10-25)  
2. [Modified Triple DES for Image Encryption (ResearchGate)](https://www.researchgate.net/publication/239732171_Image_Encryption_Based_on_the_Modified_Triple-DES_Cryptosystem)

---

> 🧠 *“Security is not a product, but a process — and this project is a step toward safer digital image exchange.”*
