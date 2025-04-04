# sd-aspect-ratio-helper/__init__.py

import gradio as gr
from modules import scripts, shared

ASPECT_RATIOS = {
    "1:1": 1.0,
    "4:3": 4 / 3,
    "3:2": 3 / 2,
    "16:9": 16 / 9,
    "5:4": 5 / 4,
    "7:5": 7 / 5,
    "2:3": 2 / 3,
    "3:4": 3 / 4,
    "9:16": 9 / 16,
    "4:5": 4 / 5,
    "6:7": 6 / 7,
    "8.5x11": 8.5 / 11,
    "11x14": 11 / 14,
    "A4 (210x297)": 210 / 297,
    "A3 (297x420)": 297 / 420,
    "Personnalisé": None
}

TRANSLATIONS = {
    "fr": {
        "title": "Ratio Helper",
        "ratio_label": "Ratio calculé :",
        "width": "Largeur (px)",
        "height": "Hauteur (px)",
        "info": "Valeur multiple de 64 recommandée",
        "apply": "Appliquer le ratio",
        "tooltip": "Choisissez un ratio standard ou 'Personnalisé'.",
        "warn": "⚠️ Attention : dimensions trop petites ({w}x{h})."
    },
    "en": {
        "title": "Ratio Helper",
        "ratio_label": "Calculated ratio:",
        "width": "Width (px)",
        "height": "Height (px)",
        "info": "Value should be multiple of 64",
        "apply": "Apply Ratio",
        "tooltip": "Choose a standard or custom ratio.",
        "warn": "⚠️ Warning: dimensions too small ({w}x{h})."
    },
    "de": {
        "title": "Seitenverhältnis-Helfer",
        "ratio_label": "Berechnetes Verhältnis:",
        "width": "Breite (px)",
        "height": "Höhe (px)",
        "info": "Wert sollte ein Vielfaches von 64 sein",
        "apply": "Seitenverhältnis anwenden",
        "tooltip": "Wählen Sie ein Standard- oder benutzerdefiniertes Verhältnis.",
        "warn": "⚠️ Warnung: Abmessungen zu klein ({w}x{h})."
    },
    "es": {
        "title": "Asistente de relación",
        "ratio_label": "Relación calculada:",
        "width": "Ancho (px)",
        "height": "Alto (px)",
        "info": "Valor múltiplo de 64 recomendado",
        "apply": "Aplicar relación",
        "tooltip": "Elija una relación estándar o personalizada.",
        "warn": "⚠️ Advertencia: dimensiones demasiado pequeñas ({w}x{h})."
    },
    "pt": {
        "title": "Assistente de proporção",
        "ratio_label": "Proporção calculada:",
        "width": "Largura (px)",
        "height": "Altura (px)",
        "info": "Valor múltiplo de 64 recomendado",
        "apply": "Aplicar proporção",
        "tooltip": "Escolha uma proporção padrão ou personalizada.",
        "warn": "⚠️ Atenção: dimensões muito pequenas ({w}x{h})."
    },
    "ar": {
        "title": "مساعد النسبة",
        "ratio_label": "النسبة المحسوبة:",
        "width": "العرض (بكسل)",
        "height": "الارتفاع (بكسل)",
        "info": "القيمة يجب أن تكون من مضاعفات 64",
        "apply": "تطبيق النسبة",
        "tooltip": "اختر نسبة قياسية أو مخصصة.",
        "warn": "⚠️ تنبيه: الأبعاد صغيرة جدًا ({w}x{h})."
    }
}

class Script(scripts.Script):
    def title(self):
        lang = shared.opts.data.get("localization", "en")[:2]
        return TRANSLATIONS.get(lang, TRANSLATIONS["en"])['title']

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        lang = shared.opts.data.get("localization", "en")[:2]
        t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])

        with gr.Accordion(t["title"], open=False):
            ratio = gr.Dropdown(label="Aspect Ratio", choices=list(ASPECT_RATIOS.keys()), value="4:3", info=t["tooltip"])
            with gr.Row():
                width = gr.Number(label=t["width"], value=512, info=t["info"])
                height = gr.Number(label=t["height"], value=384, info=t["info"])
            apply_button = gr.Button(t["apply"], elem_id="ratio_helper_button")
            preview = gr.Image(label="Aperçu du ratio", tool=None, height=160, width=240, visible=True)
            ratio_label = gr.Markdown(f"{t['ratio_label']} -", elem_id="ratio_helper_display")
            warning_label = gr.Markdown(visible=False)

        def compute_dimensions(ratio, width, height):
            from PIL import Image, ImageDraw
            import io

            def draw_preview(w, h):
                bg_color = "#f0f0ff" if w >= h else "#fff0f0"
                img = Image.new("RGB", (240, 160), color=bg_color)
                draw = ImageDraw.Draw(img)

                scale = min(220 / w, 140 / h)
                rw, rh = int(w * scale), int(h * scale)
                x = (240 - rw) // 2
                y = (160 - rh) // 2

                label = f"{w}×{h}"
                text_w, text_h = draw.textsize(label)
                draw.text(((240 - text_w) / 2, (160 - text_h) / 2), label, fill="black")

                icon = "H" if w >= h else "V"
                draw.text((210, 5), icon, fill="black")

                draw.rectangle([x, y, x + rw, y + rh], outline="black", width=2)

                return img  # ✅ retour d'un objet PIL.Image

            if ratio not in ASPECT_RATIOS or ASPECT_RATIOS[ratio] is None:
                empty_preview = Image.new("RGB", (240, 160), "white")
                return width, height, f"{t['ratio_label']} -", gr.update(visible=False), empty_preview

            factor = ASPECT_RATIOS[ratio]
            w_aligned = round(width / 64) * 64
            h_from_w = round((w_aligned / factor) / 64) * 64

            h_aligned = round(height / 64) * 64
            w_from_h = round((h_aligned * factor) / 64) * 64

            diff_w = abs(width - w_from_h)
            diff_h = abs(height - h_from_w)

            if diff_w > diff_h:
                final_w, final_h = w_aligned, h_from_w
            else:
                final_w, final_h = w_from_h, h_aligned

            ratio_calc = round(final_w / final_h, 2)

            if final_w < 256 or final_h < 256:
                warn = t['warn'].format(w=final_w, h=final_h)
                return final_w, final_h, f"{t['ratio_label']} {ratio_calc}:1", gr.update(value=warn, visible=True), draw_preview(final_w, final_h)

            return final_w, final_h, f"{t['ratio_label']} {ratio_calc}:1", gr.update(visible=False), draw_preview(final_w, final_h)

        apply_button.click(
            fn=compute_dimensions,
            inputs=[ratio, width, height],
            outputs=[width, height, ratio_label, warning_label, preview]
        )

        return [ratio, width, height, apply_button, ratio_label, warning_label, preview]
