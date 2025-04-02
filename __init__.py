# sd-aspect-ratio-helper/__init__.py

import gradio as gr
from modules import script_callbacks

ASPECT_RATIOS = {
    "4:3": 4 / 3,
    "3:2": 3 / 2,
    "16:9": 16 / 9,
    "1:1": 1,
    "2:3": 2 / 3,
    "3:4": 3 / 4,
    "Personnalisé": None
}

def render_aspect_ratio_ui():
    with gr.Column():
        ratio_dropdown = gr.Dropdown(
            choices=list(ASPECT_RATIOS.keys()),
            label="Aspect Ratio",
            value="4:3",
            elem_id="aspect_ratio_select"
        )
        lock_checkbox = gr.Checkbox(label="Verrouiller le ratio", value=True, elem_id="lock_aspect_ratio")
        use_height_as_base = gr.Checkbox(label="Calculer à partir de la hauteur", value=False, elem_id="use_height_as_base")

        with gr.Row():
            width_input = gr.Number(label="Largeur (px)", value=512, elem_id="width_input")
            height_input = gr.Number(label="Hauteur (px)", value=384, elem_id="height_input")

        round_to_64 = gr.Checkbox(label="Arrondir à un multiple de 64", value=True, elem_id="round_to_64")

    return [ratio_dropdown, lock_checkbox, use_height_as_base, width_input, height_input, round_to_64]

def add_to_txt2img(component, **kwargs):
    return render_aspect_ratio_ui()

def add_to_img2img(component, **kwargs):
    return render_aspect_ratio_ui()

script_callbacks.on_after_component("txt2img_dimensions", add_to_txt2img)
script_callbacks.on_after_component("img2img_dimensions", add_to_img2img)
