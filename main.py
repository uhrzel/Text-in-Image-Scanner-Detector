import cv2
import easyocr
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Initialize EasyOCR reader for English
reader = easyocr.Reader(['en'])

# Function to capture an image from the camera
def capture_image():
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('captured_photo.png', frame)
        text = extract_text_from_image('captured_photo.png')
        update_image_on_canvas('captured_photo.png', text)
    else:
        print("Error: Could not capture a photo.")

# Function to extract text from an image
def extract_text_from_image(image_path):
    results = reader.readtext(image_path)
    text = ''
    for result in results:
        text += result[1] + ' '
    return text

# Function to update the captured image and text on the canvas
def update_image_on_canvas(image_path, text):
    img = Image.open(image_path)
    img = img.resize((400, 300), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.image = photo

    text_label.config(text="Text extracted from the image:\n" + text)

# Function to continuously update the camera feed
def update_camera_feed():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(Image.fromarray(frame))
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo
    root.after(10, update_camera_feed)

# Create a GUI window
root = tk.Tk()
root.title("Camera Capture")

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera (usually your webcam)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Create a canvas to display the camera feed
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Create a capture button
capture_button = ttk.Button(root, text="Capture", command=capture_image)
capture_button.pack()

# Create a label for displaying extracted text
text_label = tk.Label(root, text="", wraplength=400)
text_label.pack()

# Start updating the camera feed
update_camera_feed()

# Start the main loop for the GUI
root.mainloop()

# Release the camera when the GUI window is closed
cap.release()
