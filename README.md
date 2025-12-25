# Akıllı Toplantı ve Ders Asistanı 🎙️🤖

Bu proje, **İskenderun Teknik Üniversitesi (İSTE)**, Bilgisayar Mühendisliği Bölümü **Mühendislikte Bilgisayar Uygulamaları I** dersi bitirme ödevi kapsamında geliştirilmiştir.

## 📌 Proje Hakkında
Bu uygulama, ses kayıtlarını (toplantı, ders, notlar) yapay zeka kullanarak analiz eder. Süreç iki aşamalı çalışır:
1. **OpenAI Whisper:** Ses dosyasını yerel sistemde yüksek doğrulukla metne dönüştürür.
2. **Google Gemini 2.5 Flash:** Oluşan metni analiz ederek profesyonel bir özet ve yapılacaklar listesi oluşturur.

## 🛠️ Kullanılan Teknolojiler
- **Python 3.10.11**
- **Whisper (OpenAI):** Ses deşifresi
- **Gemini 2.5 Flash (Google):** LLM tabanlı analiz
- **Gradio:** Web arayüzü
- **FFmpeg:** Ses işleme motoru

## ⚙️ Kurulum ve Çalıştırma

### 1. FFmpeg Kurulumu
Windows üzerinde çalıştırabilmek için FFmpeg kütüphanesinin kurulu olması ve `PATH` (Yol) değişkenlerine eklenmiş olması gerekmektedir.

### 2. Kütüphanelerin Yüklenmesi
Terminal üzerinden aşağıdaki komutları çalıştırın:
```bash

pip install openai-whisper gradio google-generativeai
```
### 3. API ANAHTARI
main.py içerisindeki genai.configure(api_key="...") kısmına kendi Gemini API anahtarınızı girin.

### 4. Başlatma
```bash
 python main.py
```

### 🚀 Kullanım
Uygulama başladığında terminalde çıkan http://127.0.0.1:7860 linkine gidin.

Ses dosyanızı sürükleyip bırakın ve Submit butonuna basın.

Sol tarafta sesin tam dökümünü, sağ tarafta ise yapay zeka tarafından hazırlanan özeti göreceksiniz.

### 🚀 Karşılaşılan Zorluklar
Geliştirme sürecinde Windows ortamında FFmpeg yol hataları (WinError 2) ve Gemini kütüphanesinin sürüm uyuşmazlığından kaynaklanan 404 model erişim hataları ile karşılaşılmıştır. Bu sorunlar os.environ ve request_options konfigürasyonları ile aşılmıştır.
