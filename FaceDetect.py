import face_recognition
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw


def drawImageFace(img, rects):
    img = Image.fromarray(img)
    imgdrw = ImageDraw.Draw(img)
    for i in range(0, len(rects)):
        imgdrw.rectangle(rects[i], outline=(255, 0, 0), width=5)
    return img


def resizeRect(rects):
    for index in range(0, len(rects)):
        top, right, bottom, left = rects[index]
        top = int(top - top*0.7)
        left = int(left - left*0.2)
        right = int(right + right*0.2)
        bottom = int(bottom + bottom*0.05)
        rects[index] = (top, right, bottom, left)
    return rects


def getFaceRect(imgPath):
    img = face_recognition.load_image_file(imgPath)
    face_locations = face_recognition.face_locations(img)
    return img, face_locations
