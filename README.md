# Araç Plaka Tanıma Sistemi (License Plate Recognition System)

Bu proje, YOLOv8 nesne tespit modeli ve EasyOCR optik karakter tanıma (OCR) kütüphanesini kullanarak videolardaki araç plakalarını otomatik olarak tespit eden ve okuyan bir Python uygulamasıdır.

## 🚀 Özellikler

- **YOLOv8 ile Plaka Tespiti**: Özel olarak eğitilmiş YOLOv8 modeli (`runs/detect/train2/weights/best.pt`) sayesinde video karelerindeki plakalar yüksek doğrulukla tespit edilir.
- **Görüntü İyileştirme (Image Processing)**: OCR doğruluğunu artırmak amacıyla, tespit edilen plaka bölgeleri kırpılır, gri tona dönüştürülür ve Histogram Eşitleme (Histogram Equalization) uygulanır.
- **EasyOCR ile Karakter Okuma**: İyileştirilmiş plaka görseli EasyOCR kullanılarak metne dönüştürülür.
- **Plaka Filtreleme**:
  - Güven skoru 0.55'in altındaki okumalar elenir.
  - Karakter uzunluğu 6 ile 10 arasında olmayan okumalar filtre dışı bırakılır.
  - Okunan metin temizlenerek yalnızca harf ve rakamlardan oluşması sağlanır.
- **Akıllı Loglama**: Okunan plakalar zaman damgasıyla birlikte `plates.txt` dosyasına kaydedilir. Aynı plakanın 30 saniye içerisinde tekrar tekrar log dosyasına yazılması engellenir.
- **Canlı Görselleştirme**: Tespit edilen plaka bölgesi yeşil bir çerçeveye alınarak üzerine okunan plaka canlı olarak yazdırılır.

---

## 🛠️ Kurulum

Projenin çalışabilmesi için gerekli kütüphanelerin yüklenmesi gerekmektedir. Python 3.8+ sürümü önerilir.

1. **Gereksinimleri Yükleme**:
   Gerekli kütüphaneleri yüklemek için aşağıdaki komutu kullanabilirsiniz:
   ```bash
   pip install -r yükle.txt
   ```
   *(Eğer `yükle.txt` yerine standart `requirements.txt` kullanmak isterseniz, paket listesi `yükle.txt` dosyası içerisindedir.)*

2. **Video Dosyası**:
   Uygulama varsayılan olarak dizindeki `_video.mp4` isimli videoyu işlemektedir. Kendi videonuzu test etmek için videonuzun adını `_video.mp4` yapabilir veya `app.py` içerisindeki ilgili satırı güncelleyebilirsiniz.

---

## 💻 Kullanım

Projeyi başlatmak için terminal veya komut satırından aşağıdaki komutu çalıştırmanız yeterlidir:

```bash
python app.py
```

### Tuş Kontrolleri:
- Canlı pencereyi kapatmak ve uygulamadan çıkmak için klavyeden **`q`** tuşuna basabilirsiniz.

---

## 📂 Dosya Yapısı

- `app.py`: Plaka tespiti, görüntü işleme, OCR ve loglama işlemlerini yürüten ana uygulama dosyası.
- `data.yaml`: YOLOv8 model eğitimi için veri seti yollarını ve sınıf isimlerini barındıran yapılandırma dosyası.
- `yükle.txt`: Projenin bağımlılıklarını içeren paket listesi.
- `plates.txt`: Tespit edilen plakaların zaman damgasıyla birlikte kaydedildiği log dosyası.
- `runs/`: YOLOv8 modelinin eğitim çıktılarını ve eğitilmiş ağırlıklarını (`best.pt`) barındıran dizin.
- `_video.mp4`: Test/girdi olarak kullanılan örnek video dosyası.

---

## 📝 Lisans

Bu proje eğitim ve geliştirme amaçlı hazırlanmıştır. Katkıda bulunmaktan veya kendi projelerinizde kullanmaktan çekinmeyin!
