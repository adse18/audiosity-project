from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Laden des BLIP-Modells und des Tokenizers
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_blip_caption(image_path):
    """Generiert eine Bildunterschrift für das gegebene Bild."""
    image = Image.open(image_path).convert("RGB") 
    inputs = blip_processor(images=image, return_tensors="pt")  

    output_ids = blip_model.generate(**inputs, max_length=16, num_beams=4)
    caption = blip_processor.decode(output_ids[0], skip_special_tokens=True)
    return caption