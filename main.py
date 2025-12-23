import os
import whisper
import gradio as gr
import google.generativeai as genai

# 1. FFmpeg Yolunu Zorla Tanıtıyoruz (PATH hatasını önlemek için)
os.environ["PATH"] += os.pathsep + r'C:\ffmpeg\bin'

# 2. Yapay Zeka Yapılandırması
# API anahtarın burada tanımlı
genai.configure(api_key="AIzaSyBxLCsRVMa_ZN7QbdssXn9_64Ckaz3d-lU")

# Model adı 1.5-flash olarak güncellendi çünkü 2.5 diye bir model henüz yok (404 hatasını önler)
model_gemini = genai.GenerativeModel('gemini-2.5-flash')

# 3. Whisper Modelini Yükle
print("Yapay zeka modelleri hazırlanıyor...")
whisper_model = whisper.load_model("base")

# --- ÖZEL TASARIM (CSS) KODLARI ---
custom_css = """
.gradio-container { background-color: #0b0f19 !important; }
#title_area { text-align: center; color: #ffffff; }
.input-text, .output-text, .gradio-input, .gradio-output {
    border-radius: 12px !important;
    border: 1px solid #2d3748 !important;
    background-color: #1a202c !important;
    color: white !important;
}
button.primary {
    background: linear-gradient(90deg, #4f46e5 0%, #3b82f6 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}
"""

def analiz_et(ses_yolu):
    try:
        if ses_yolu is None:
            return "Lütfen bir ses dosyası yükleyin.", "", ""

        # Ses deşifre ediliyor
        print("Ses deşifre ediliyor...")
        sonuc = whisper_model.transcribe(ses_yolu, fp16=False)
        tam_metin = sonuc["text"]

        # Gemini Analiz İsteği
        print("Yapay zeka analiz yapıyor...")
        # Gemini'a net bir başlık kullanmasını söylüyoruz
        prompt = f"Aşağıdaki metni özetle ve varsa yapılacak somut görevleri 'GÖREVLER:' başlığı altında listele:\n\n{tam_metin}"
        response = model_gemini.generate_content(prompt)
        analiz_sonucu = response.text

        # --- BURASI KRİTİK: KUTULARA DAĞITMA MANTIĞI ---
        # Gemini genelde **GÖREVLER:** veya GÖREVLER: şeklinde başlık atar.
        if "GÖREVLER" in analiz_sonucu.upper():
            # Büyük harf duyarsız bölme işlemi yapıyoruz
            if "**GÖREVLER:**" in analiz_sonucu:
                parcalar = analiz_sonucu.split("**GÖREVLER:**")
            elif "GÖREVLER:" in analiz_sonucu:
                parcalar = analiz_sonucu.split("GÖREVLER:")
            else:
                parcalar = [analiz_sonucu]

            if len(parcalar) > 1:
                ozet = parcalar[0].strip()
                gorevler = parcalar[1].strip()
            else:
                ozet = analiz_sonucu
                gorevler = "Görevler ayıklanamadı."
        else:
            ozet = analiz_sonucu
            gorevler = "Metin içerisinde belirgin görev bulunamadı."

        return tam_metin, ozet, gorevler

    except Exception as e:
        # Hata kontrolü
        return f"Teknik bir sorun oluştu: {str(e)}", "Hata", "Hata"

# 4. Arayüz Tasarımı (Custom CSS + Blocks yapısı)
with gr.Blocks(css=custom_css, theme="soft") as arayuz:
    gr.Markdown("# 🎙️ Gelişmiş AI Toplantı Asistanı", elem_id="title_area")

    with gr.Row():
        with gr.Column():
            ses_input = gr.Audio(type="filepath", label="Ses Dosyasını Yükleyin")
            submit_btn = gr.Button("Analiz Et", variant="primary")

        with gr.Column():
            output_metin = gr.Textbox(label="1. Deşifre Edilen Tam Metin", lines=8)
            output_ozet = gr.Textbox(label="2. Akıllı Özet", lines=5)
            output_gorev = gr.Textbox(label="3. Yapılacaklar Listesi", lines=5)

    submit_btn.click(
        fn=analiz_et,
        inputs=ses_input,
        outputs=[output_metin, output_ozet, output_gorev]
    )

if __name__ == "__main__":
    arayuz.launch()