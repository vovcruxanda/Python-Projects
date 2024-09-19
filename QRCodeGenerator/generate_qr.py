import qrcode as qr
import re

# Geting URL input from the user
link = input("Enter the link for the QR code: ")

# Generating the QR code
img = qr.make(link)

# Removing query parameters and fragments (anything after '?' or '#')
clean_link = re.split(r'[?#]', link)[0]

# Remove "https://", "http://", "www.", and common domain extensions
clean_link = re.sub(r'(https?://)?(www\.)?', '', clean_link)
clean_link = re.sub(r'\.(com|org|net|dev|edu|gov|io|co)', '', clean_link)

# Remove non-alphanumeric characters and replace with underscores for a valid file name
file_name = re.sub(r'[^a-zA-Z0-9]', '_', clean_link)

# Set the file path and name
file_path = f"D:/Learning&improving/Python Projects/QRCodeGenerator/{file_name}.png"

# Save the image with the generated name
img.save(file_path)

print(f"QR code generated and saved successfully as {file_name}.png!")
