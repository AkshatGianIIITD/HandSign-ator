# import cv2
# import ultralytics
# from ultralytics import YOLO

# # Load the YOLO model
# model = YOLO(r'C:\cv_project\animals_151_first_training\best.pt')

# # Open the webcam
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Run YOLO inference
#     results = model.predict(frame,conf=0.25)

#     # Convert results to an image with bounding boxes
#     for result in results:
#         annotated_frame = result.plot()  # This automatically adds bounding boxes and labels

#     # Display the frame
#     cv2.imshow("YOLO Detection", annotated_frame)

#     # Exit when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



"""For image"""
import cv2
import ultralytics
from ultralytics import YOLO

# Load the YOLO model
model = YOLO(r'best.pt')

# Load the image
image_path = r'34.jpg'  # Change to your test image path
image = cv2.imread(image_path)

# Run YOLO inference
results = model.predict(image, conf=0.25)

# Convert results to an image with bounding boxes
for result in results:
    annotated_image = result.plot()  # This automatically adds bounding boxes and labels

# Display the image
import matplotlib.pyplot as plt

plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
plt.title("YOLO Detection")
plt.axis("off")
plt.show()


