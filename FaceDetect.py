import face_recognition
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
image = face_recognition.load_image_file("dataset\\下載 (1).jpg")
face_locations = face_recognition.face_locations(image)
print(face_locations)
img = Image.fromarray(image)
for rect in face_locations:
    imgdrw = ImageDraw.Draw(img)
    top, right, bottom, left = rect
    top = int(top - top*0.7)
    left = int(left - left*0.2)
    right = int(right + right*0.2)
    bottom = int(bottom + bottom*0.05)
    rect_shape = (left, top, right, bottom)
    imgdrw.rectangle(rect_shape, outline=(255, 0, 0), width=5)
    img.show()
    image = image[top:bottom, left:right]
    img = Image.fromarray(image)
    img.show()
