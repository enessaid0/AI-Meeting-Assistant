import os
import whisper
import gradio as gr
import google.generativeai as genai

# 1. FFmpeg Yolunu Zorla Tanıtıyoruz mecburi (hata aldım çünkü)
os.environ["PATH"] += os.pathsep + r'C:\ffmpeg\bin'

# GPT API
# API anahtarını buraya yazıcağız
genai.configure(api_key="BURAYA API GİRİN")  # Kişisel apinizi girin

# 404 hatasını önlemek için en kararlı model ismini kullanıyoruz
model_gemini = genai.GenerativeModel('gemini-2.5-flash')  # veya başka model adı


# 3. Whisper Modelini Yükle
print("Yapay zeka modelleri hazırlanıyor...")
whisper_model = whisper.load_model("base")


def analiz_et(ses_yolu):
    try:
        if ses_yolu is None:
            return "Lütfen bir ses dosyası yükleyin.", "", ""

        # Sesi metne dönüştürmeliyiz
        print("Ses deşifre ediliyor...")
        sonuc = whisper_model.transcribe(ses_yolu, fp16=False)
        tam_metin = sonuc["text"]

        # Ben Gpt kullandım ondan analiz etmesini istiyoruz.
        print("Yapay zeka analiz yapıyor...")
        response = model_gemini.generate_content(
            f"Aşağıdaki toplantı metnini profesyonelce özetle ve yapılacak görevleri madde madde çıkar:\n\n{tam_metin}"
        )
        analiz_sonucu = response.text

        # Gönderdiğimiz ses kaydının çıktılarını bölümlere dağıtmamız lazım.
        ozet = analiz_sonucu.split("Görev")[0] if "Görev" in analiz_sonucu else analiz_sonucu
        gorevler = analiz_sonucu.split("Görev")[
            -1] if "Görev" in analiz_sonucu else "Metin içerisinde belirgin görev bulunamadı."

        return tam_metin, ozet, gorevler

    except Exception as e:
        return f"Teknik bir sorun oluştu: {str(e)}", "Hata", "Hata"


# 4. Arayüz Tasarımı
arayuz = gr.Interface(
    fn=analiz_et,
    inputs=gr.Audio(type="filepath", label="Ses Dosyasını Yükleyin"),
    outputs=[
        gr.Textbox(label="1. Deşifre Edilen Tam Metin", lines=10),
        gr.Textbox(label="2. Akıllı Özet ", lines=5),
        gr.Textbox(label="3. Yapılacaklar Listesi ", lines=5)
    ],
    title="🎙️ Gelişmiş AI Toplantı Asistanı",
    description="Ses kaydını yükleyin; Whisper deşifre etsin, yapay zeka analiz etsin.",
    theme="soft"
)

if __name__ == "__main__":
    arayuz.launch()