from windows_screenshot import find_window_id, capture_window_as_img
from image_diff import calculate_image_difference
from PIL import Image
from pathlib import Path

import time

dir = Path('data')

if not dir.exists(): 
    dir.mkdir()


previous_img = Image.new('RGB', (100, 100), (255, 255, 255))



window_handle = find_window_id("RetroArch")
counter = 0
while window_handle:

    filepath = dir.joinpath(f'ss_{counter}.jpg')
    print(f"{window_handle} found")
    img = capture_window_as_img(window_handle)

    percent_diff = calculate_image_difference(img, previous_img)
    print(f"Images differ by {percent_diff:.2f}%")

    if percent_diff > 10:
        print("Images are more than 10% different. Saving the image.")
        
        img.save(filepath)
        counter += 1

        previous_img = img
    
    else:
        print("Different is less than 10%. No need to save again.")


    time.sleep(1)

