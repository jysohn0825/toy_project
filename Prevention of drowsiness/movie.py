from tkinter.filedialog import *
from tkinter.simpledialog import *
import cv2
import numpy as np
import joblib
from datetime import datetime
import pymysql

def clickStart() :
    global count, window, edtID, edtPW
    userId = edtID.get()
    userPw = edtPW.get()
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()  # 빈 트럭 준비
    sql = "SELECT d_id FROM drowsiness WHERE d_id = '" + userId + "' and d_pw = '" + str(userPw) + "';"
    cur.execute(sql)
    check = cur.fetchone()
    if check != None:
        conn.close()
        cur.close()
        count += 1
        s_factor = 1 # 화면 크기 비율(조절 가능)
        capture = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter(f"{userId}_{datetime.today().year}{datetime.today().month}{datetime.today().day}_{count}.avi", fourcc, 20.0, (int(capture.get(3)), int(capture.get(4))))

        frameCount = 0 # 처리할 프레임의 숫자 (자동증가)
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        left_eye_cascade = cv2.CascadeClassifier("haarcascade_lefteye_2splits.xml")
        right_eye_cascade = cv2.CascadeClassifier("haarcascade_righteye_2splits.xml")
        ##### OpenCV 용 영상처리 ###
        check = 0
        while True:
            ret, frame = capture.read()
            if not ret:  # 동영상을 읽기 실패
                break
            frameCount += 1

            if frameCount % 1  == 0 : # 숫자 조절 가능 (속도 문제)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                ## 눈 인식을 위한 얼굴 인식
                for(x,y,w,h) in faces:

                    cv2.rectangle(frame, (x, y), (x + w, y + h + 10), (255, 0, 0), 2)
                    face_gray = gray[y:y+int(h/2),x:x+w]

                    ## 눈 인식 haar cascaede
                    left_eyes = left_eye_cascade.detectMultiScale(face_gray,1.1,5)
                    right_eyes = right_eye_cascade.detectMultiScale(face_gray,1.1,5)

                    ## 교육 시켜 놓은 dump 로딩
                    clf = joblib.load("learn_eye.dmp")


                    for (ex,ey,ew,eh) in right_eyes:
                        if x + ex < x + w/2 :
                            tr = []
                            for i in range(0, 26):
                                for j in range(0, 34):
                                    tr.append(gray[y + ey + 15 + i, x + ex + 5 + j])
                            check_right_eye = clf.predict([tr])
                            if check_right_eye == 1:
                                cv2.rectangle(frame, (x + ex + 5, y + ey + 18), (x + ex + 39, y + ey + 44), (0, 0, 255), 1)
                            else:
                                cv2.rectangle(frame, (x + ex + 5, y + ey + 18), (x + ex + 39, y + ey + 44), (0, 255, 0), 1)
                    for (ex,ey,ew,eh) in left_eyes:
                        tl = []
                        if x + ex > x+w/2 :
                            for i in range(0, 26):
                                for j in range(0, 34):
                                    tl.append(gray[y + ey + 20 + i, x + ex + 5 + j])
                            check_left_eye = clf.predict([tl])
                            if check_left_eye == 1:
                                cv2.rectangle(frame, (x + ex + 5, y + ey + 18), (x + ex + 39, y + ey + 44), (0, 0, 255), 1)
                                check += 1
                            else:
                                cv2.rectangle(frame, (x + ex + 5, y + ey + 18), (x + ex + 39, y + ey + 44), (0, 255, 0), 1)
                                check = 0

                    if check > 5:
                        d_time = str(datetime.now())
                        conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
                        cur = conn.cursor()
                        sql = "INSERT INTO d_time VALUES ('" + userId + "','" + d_time + "');"
                        cur.execute(sql)
                        conn.commit()
                        cur.close()
                        conn.close()

                frame = cv2.resize(frame, None, fx=s_factor, fy=s_factor, interpolation=cv2.INTER_AREA)
                cv2.imshow('Video', frame)
                out.write(frame)

            key = cv2.waitKey(1)
            if key == 27:
                break

        capture.release()
        cv2.destroyAllWindows()


def clickSign():
    global window
    subwindow = Toplevel(window)
    subwindow.geometry('150x140')
    labelID = Label(subwindow, text="ID")
    labelID.grid(row=0, column=0, padx=10, pady=5)
    signID = Entry(subwindow, width=10)
    signID.grid(row=0, column=1)

    labelPW = Label(subwindow, text="PW")
    labelPW.grid(row=1, column=0, padx=10, pady=5)
    signPW = Entry(subwindow, width=10)
    signPW.grid(row=1, column=1)

    labelPhone = Label(subwindow, text="Phone")
    labelPhone.grid(row=2, column=0, padx=10, pady=5)
    edtPhone = Entry(subwindow, width=10)
    edtPhone.grid(row=2, column=1)

    def insertInfo():
        userID = signID.get()
        userPW = signPW.get()
        userPhone = edtPhone.get()
        conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cur = conn.cursor()  # 빈 트럭 준비
        sql = "SELECT * FROM user_table WHERE u_id =" + userID + ";"
        try:
            cur.execute(sql)
        except:
            sql = "INSERT INTO drowsiness VALUES('" + userID + "','" + userPW + "','" + userPhone + "');"
            cur.execute(sql)
            conn.commit()
        else:
            messagebox.showinfo('실패', 'ID 중복')
        cur.close()
        conn.close()
        messagebox.showinfo('성공', '회원가입 성공')
        subwindow.destroy()

    btnSign = Button(subwindow, text='회원가입', command=insertInfo, pady=5)
    btnSign.grid(row=4, column=1)

    subwindow.mainloop()

## 전역 변수부
count = 0
conn, cur = None, None
IP = ****
USER = ****
PASSWORD = ****
DB = 'drowsiness_db'
window = None
edtID, edtPW = None, None


## 메인 코드부
if __name__ == '__main__' :
    window = Tk()
    window.geometry('250x80')
    window.resizable(False, False)

    labelID = Label(window, text="ID")
    edtID = Entry(window, width=15)
    labelID.grid(row=0, column=0, padx=10, pady=5)
    edtID.grid(row=0, column=1, padx=10, pady=5)
    btnLogin = Button(window, text='로그인', command=clickStart)
    btnLogin.grid(row=0, column=3, padx=10, pady=5)

    labelPW = Label(window, text="PW")
    edtPW = Entry(window, width=15)
    labelPW.grid(row=1, column=0, padx=10, pady=5)
    edtPW.grid(row=1, column=1, padx=10, pady=5)
    btnSign = Button(window, text='회원가입', command=clickSign)
    btnSign.grid(row=1, column=3, padx=10, pady=5)
    window.mainloop()

