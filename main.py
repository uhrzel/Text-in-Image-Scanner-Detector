import cv2
import easyocr
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Initialize EasyOCR reader for English
reader = easyocr.Reader(['en'])


# Function to extract text from an image
def extract_text_from_image(image_path):
    results = reader.readtext(image_path)
    text = ''
    for result in results:
        text += result[1] + ' '
    return text


# Function to continuously update the camera feed and capture an image
def update_camera_feed_and_capture():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Add a square display indicator
        frame = add_square_indicator(frame)

        photo = ImageTk.PhotoImage(Image.fromarray(frame))
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo

        # Automatically capture the image when something is detected in the frame
        text = extract_text_from_image_from_frame(frame)
        if text:
            cv2.imwrite('captured_photo.png', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            update_text_on_label(text, font_size=12)  # Change the font size here
    root.after(10, update_camera_feed_and_capture)


# Function to extract text from a frame
def extract_text_from_image_from_frame(frame):
    image = Image.fromarray(frame)
    image.save('current_frame.png')
    text = extract_text_from_image('current_frame.png')
    return text


# Function to update the text label with a specified font size
def update_text_on_label(text, font_size=12):
    text_label.config(text="Text extracted from the image:\n" + text, font=("Arial", font_size))


# Function to add a square display indicator
def add_square_indicator(frame):
    # Define square coordinates and size
    x1, y1, x2, y2 = 100, 100, 300, 300
    square_color = (0, 255, 0)  # Green color (BGR format)
    square_thickness = 2  # Thickness of the square border

    # Draw the square on the frame
    cv2.rectangle(frame, (x1, y1), (x2, y2), square_color, square_thickness)

    return frame


# Create a GUI window
root = tk.Tk()
root.title("Camera Capture")

# Create a label for the title
title_label = tk.Label(root, text="Text Identifier", font=("Arial", 20))
title_label.pack()

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera (usually your webcam)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Create a canvas to display the camera feed
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Create a label for displaying extracted text
text_label = tk.Label(root, text="", wraplength=400)
text_label.pack()

# Start updating the camera feed and automatically capturing images
update_camera_feed_and_capture()

# Start the main loop for the GUIs
root.mainloop()

# Release the camera when the GUI window is closed
cap.release()
