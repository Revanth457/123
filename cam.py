import cv2

# List of possible camera devices to check
camera_devices = ['/dev/video-usb-cam0', '/dev/video-usb-cam1']

cap = None
working_camera = None

# Try each camera device in the list
for device in camera_devices:
    cap = cv2.VideoCapture(device)
    if cap.isOpened():
        working_camera = device  # Record which camera worked
        print(f"Success: USB camera {device} is accessible.")
        break
else:
    print("Error: Unable to access any USB camera.")
    exit()

# If camera is accessible, read a frame and display it
ret, frame = cap.read()
if ret:
    cv2.imshow(f"USB Camera ({working_camera}) Frame", frame)  # Display the camera feed
    cv2.waitKey(0)
else:
    print(f"Error: Failed to read a frame from {working_camera}.")

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
