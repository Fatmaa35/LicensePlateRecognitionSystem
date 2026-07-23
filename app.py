from ultralytics import YOLO
import cv2
import easyocr
import time
import re

# ==============================
# MODEL
# ==============================
model = YOLO("runs/detect/train2/weights/best.pt")

# OCR
reader = easyocr.Reader(['en'], gpu=False)

# Video
cap = cv2.VideoCapture("_video.mp4")

if not cap.isOpened():
    print("Video açılamadı!")
    exit()

# Log dosyası
log_file = open("plates.txt", "a", encoding="utf-8")

# Aynı plakayı tekrar tekrar kaydetmemek için
last_seen = {}

# OCR her karede çalışmasın
frame_count = 0


def clean_plate(text):
    """
    OCR sonucunu temizler.
    """
    text = text.upper()
    text = re.sub(r'[^A-Z0-9]', '', text)
    return text


cv2.namedWindow("Plaka Tanıma Sistemi", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Plaka Tanıma Sistemi", 640, 480)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    results = model(frame, conf=0.25)[0]

    output = results.plot()

    for box in results.boxes:

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(frame.shape[1], x2)
        y2 = min(frame.shape[0], y2)

        width = x2 - x1
        height = y2 - y1

        # Çok küçük plakaları okuma
        if width < 60 or height < 20:
            continue

        plate_crop = frame[y1:y2, x1:x2]

        if plate_crop.size == 0:
            continue

        # OCR'ı her 3 karede bir çalıştır
        if frame_count % 3 != 0:
            continue

        # Görüntü iyileştirme
        gray = cv2.cvtColor(plate_crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        ocr_results = reader.readtext(gray)

        for _, text, conf in ocr_results:

            if conf < 0.55:
                continue

            plate = clean_plate(text)

            if len(plate) < 6 or len(plate) > 10:
                continue

            current_time = time.time()

            # Aynı plakayı 30 saniye boyunca tekrar yazma
            if plate in last_seen:
                if current_time - last_seen[plate] < 30:
                    continue

            last_seen[plate] = current_time

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            log_file.write(f"{timestamp} - {plate}\n")
            log_file.flush() # önceliklendirme fonksiyonu

            print(f"[+] Plaka Okundu : {plate}")

            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.putText(
                output,
                plate,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

    cv2.imshow("Plaka Tanıma Sistemi", output)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
log_file.close()
cv2.destroyAllWindows()