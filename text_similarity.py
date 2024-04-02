# This is a part of building a dataset of screenshots, creating this file just for convinent for now. 

from thefuzz import fuzz
from PIL import Image
from pathlib import Path

import easyocr
import json
import io

def find_closest_entry(current_text):
    print(f"find_closest_entry- current_text: {current_text}")
    if "Contentless Cores Explore"   in current_text:
        print(f"skipping menu")
        return None

    
    # Initialize variables to track the highest similarity and corresponding entry number
    max_similarity_ratio = 0.33  # Start with your threshold
    closest_entry_number = None
    
    for number, entry in dialogues.items():
        dialogue = entry['dialogue']
        similarity_ratio = fuzz.ratio(current_text, dialogue) / 100.0  # Convert to a scale of 0 to 1
        #print(f"dialogue: {dialogue} -- similarity_ratio: {similarity_ratio} -- number {number}")
        
        # Update if this entry has a higher similarity ratio than current max and is above threshold
        if similarity_ratio > max_similarity_ratio:
            max_similarity_ratio = similarity_ratio
            closest_entry_number = number

    return closest_entry_number  # Return the entry number with the highest similarity ratio over 0.33

def ocr_easyocr(image):
    # Convert the PIL Image to bytes
    byte_buffer = io.BytesIO()

    image.save(byte_buffer, format='JPEG')  # You can change format if needed
    image_bytes = byte_buffer.getvalue()


    result =  reader.readtext(image_bytes,detail = 0) #change detail if you want the locations
    filtered_array = [entry for entry in result if 'RetroArch' not in entry]
    str = ' '.join(filtered_array)
    return str


reader = easyocr.Reader(['en'])

dialog_file_path = Path('dialogues_en_v2.json')

with dialog_file_path.open('r') as file:
    data = json.load(file)

dialogues = {index: item for index, item in enumerate(data)}

# for number, entry in dialogues.items():
#     print(f"{number}: Name: {entry['name']}, Dialogue: {entry['dialogue']}")


img_fld = Path('data')

with open('ss.csv', 'w') as f:
    for img_path in img_fld.iterdir():

        with Image.open(img_path) as img:
            text = ocr_easyocr(img)
            closest_entry = find_closest_entry(text)
            if closest_entry:
                closest_dialogue = f"{dialogues[closest_entry]['name']}:{dialogues[closest_entry]['dialogue']}"
            else:
                closest_dialogue = ""
            print(closest_dialogue)

            data = (img_path.name,closest_dialogue, text )

            f.write(','.join(data) + '\n')
    