import cv2
import face_recognition

img = face_recognition.load_image_file("images/Nayeon.jpg")
r = 500/img.shape[1]
dim = (500, int(r*img.shape[0]))
img = cv2.resize(img,dim,interpolation=cv2.INTER_AREA)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

test = face_recognition.load_image_file("3.jpg")
r = 500/test.shape[1]
dim = (500, int(r*test.shape[0]))
test = cv2.resize(test,dim,interpolation=cv2.INTER_AREA)
test = cv2.cvtColor(test,cv2.COLOR_BGR2RGB)

faceLoc = face_recognition.face_locations(img)[0]
encode = face_recognition.face_encodings(img)[0]
cv2.rectangle(img, (faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]), (255,255,0),2)

faceLoctest = face_recognition.face_locations(test)[0]
encodetest = face_recognition.face_encodings(test)[0]
cv2.rectangle(test, (faceLoctest[3],faceLoctest[0]),(faceLoctest[1],faceLoctest[2]), (255,255,0),2)

result = face_recognition.compare_faces([encode], encodetest)
print(result)

cv2.imshow("img", img)
cv2.imshow("test", test)
cv2.waitKey(0)
cv2.destroyAllWindows()