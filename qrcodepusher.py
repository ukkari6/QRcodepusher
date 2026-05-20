import sys
import cv2
import time

args = sys.argv


me_mode = ""
other_mode = ""
#まずはモードを検索、sendかreceiveか
if '-s' in args:
  me_mode = "send"
  other_mode = "receive"
elif '-r' in args:
  me_mode = "receive"
  other_mode = "send"
else:
  print("Send か　Receive を指定してください")
  sys.exit()


filename = ""
#次はファイル名の検索
if  '-n' in args:
  try:
    filename = args[args.index('-n') + 1]
  except IndexError:
    filename = "filename"
    print("ファイル名が指定されていません。デフォルト値を使用します。")
else:
  filename = "filename"


print("モード:",end="")
print(me_mode)
print("ファイル名:",end="")
print(filename)


#相手側QRコードの検出
cap = cv2.VideoCapture(0)
qcd = cv2.QRCodeDetector()
#retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow('Webcam', frame)
        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(frame)

        key = cv2.waitKey(1) & 0xFF

        if retval:
          if "".join(decoded_info) == other_mode:
            print("相手のコンピュータを検出しました")
            print("エンターキーで送信を開始します")

            # エンターキーが押されたらループから抜ける
            if key == 13:
                break
        else:
          print("QRコード検出中....")


        # 'q'キーが押されたらループから抜ける
        if key == ord('q'):
            # キャプチャをリリースし、ウィンドウを閉じる
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()
            break
    else:
        break


#me_mode = "send"
#other_mode = "receive"

#メイン処理
if me_mode == "send":
  #送信処理
  #QRエンコーダーの作成
  encoder = cv2.QRCodeEncoder.create()
  #バイナリファイル読み込み
  with open(filename, 'rb') as f:
    data = f.read()
    data_list = ""
    while True:
      print("send")
      #data配列を16進数文字列化してdata_listに追加する
      for i in range(0, len(data), 2):
        for j in range(2):
          current_byte_index = i + j
          if current_byte_index < len(data):
            data_list += '{:02x}'.format(data[current_byte_index])

        img = encoder.encode(data_list)
        img_resized = cv2.resize(img, (300, 300), interpolation=cv2.INTER_NEAREST)
        # 保存または表示
        cv2.imshow("QR Code", img_resized)
        cv2.waitKey(500)
        print(data_list)
        data_list = ""

      #送信完了処理
      img = cv2.imread('completion_qr.png')
      cv2.imshow('Display Window', img)
      cv2.waitKey(1000)
      break


elif me_mode == "receive":
  #受信処理
  while(cap.isOpened()):
    print("receive")
    time.sleep(0.1)

      ret, frame = cap.read()
      if ret == True:
          cv2.imshow('Webcam', frame)
          retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(frame)

          key = cv2.waitKey(1) & 0xFF

          if retval:








else:
  print("エラー")
  cap.release()
  cv2.destroyAllWindows()
