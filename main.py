import os
import datetime
import whisper
import gradio as gr
import google.generativeai as genai

# FFmpeg Yolunu Zorla Tanıtıyoruz (PATH hatasını önlemek için)
os.environ["PATH"] += os.pathsep + r'C:\ffmpeg\bin'


# API
genai.configure(api_key="")


model_gemini = genai.GenerativeModel('gemini-2.5-flash')

#  Whisper Modeli
print("Yapay zeka modelleri hazırlanıyor...")
whisper_model = whisper.load_model("base")

# CSS KODLARI
custom_css = """
.gradio-container { background-color: #0b0f19 !important; }
#title_area { text-align: center; color: #ffffff; }
.input-text, .output-text, .gradio-input, .gradio-output {
    border-radius: 12px !important;
    border: 1px solid #2d3748 !important;
    background-color: #1a202c !important;
    color: white !important;
    }
.signature {
    position: fixed;
    bottom: 20px;
    left: 20px;
    padding: 10px 20px;
    background: linear-gradient(90deg, #4f46e5 0%, #3b82f6 100%);
    color: white;
    border-radius: 10px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);  
    z-index: 1000;
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


        print("Ses deşifre ediliyor...")
        sonuc = whisper_model.transcribe(ses_yolu, fp16=False)
        tam_metin = sonuc["text"]

        # Gemini Analiz
        print("Yapay zeka analiz yapıyor...")
        prompt = f"Aşağıdaki metni özetle ve varsa yapılacak somut görevleri 'GÖREVLER:' başlığı altında listele:\n\n{tam_metin}"
        response = model_gemini.generate_content(prompt)
        analiz_sonucu = response.text

        # KUTULARA DAĞITMA MANTIĞI
        if "GÖREVLER" in analiz_sonucu.upper():
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


        # "a" modu sayesinde her analiz dosyanın sonuna eklenir.
        with open("analiz_sonucu.txt", "a", encoding="utf-8") as dosya:
            dosya.write("\n" + "="*60 + "\n")
            dosya.write("YENİ ANALİZ KAYDI\n")
            dosya.write(f"--- TAM METİN ---\n{tam_metin}\n\n")
            dosya.write(f"--- AKILLI ÖZET ---\n{ozet}\n\n")
            dosya.write(f"--- YAPILACAKLAR LİSTESİ ---\n{gorevler}\n")
            dosya.write("="*60 + "\n")

        print("Analiz başarıyla 'analiz_sonucu.txt' dosyasına eklendi.")

        return tam_metin, ozet, gorevler

    except Exception as e:
        return f"Teknik bir sorun oluştu: {str(e)}", "Hata", "Hata"
# Arayüz Tasarımı
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
    gr.HTML('<div class="signature">Enes Sait Okur</div>')

if __name__ == "__main__":
    arayuz.launch()