import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import qrcode

URL = 'https://miikey24s.github.io/tai-lieu-hoi-nghi/'
TEXT_TOP = 'TÀI LIỆU HỘI NGHỊ'
TEXT_BOTTOM = 'QUÉT MÃ QR'
FONT_PATH = 'C:/Windows/Fonts/arialbd.ttf'

print(f"Generating QR assets for URL: {URL}")

# Base QR Code generator with High Error Correction
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=40,
    border=4,
)
qr.add_data(URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color='black', back_color='white').convert('RGB')

# 1. Standalone high-res QR code (2000 x 2000 px)
qr_img.resize((2000, 2000), Image.Resampling.NEAREST).save('qr_code_only.png', dpi=(300, 300))
print("Saved qr_code_only.png")

# 2. Standard Poster (2000 x 2600 px @ 300 DPI)
W, H = 2000, 2600
img_standard = Image.new('RGB', (W, H), 'white')
draw = ImageDraw.Draw(img_standard)

font_top = ImageFont.truetype(FONT_PATH, 115)
font_bottom = ImageFont.truetype(FONT_PATH, 95)

bbox_top = draw.textbbox((0, 0), TEXT_TOP, font=font_top)
top_w = bbox_top[2] - bbox_top[0]

bbox_bottom = draw.textbbox((0, 0), TEXT_BOTTOM, font=font_bottom)
bottom_w = bbox_bottom[2] - bbox_bottom[0]

qr_size = 1450
qr_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.NEAREST)

x_top = (W - top_w) // 2
y_top = 340

x_qr = (W - qr_size) // 2
y_qr = 550

x_bottom = (W - bottom_w) // 2
y_bottom = 2140

draw.text((x_top, y_top), TEXT_TOP, fill='black', font=font_top)
img_standard.paste(qr_resized, (x_qr, y_qr))
draw.text((x_bottom, y_bottom), TEXT_BOTTOM, fill='black', font=font_bottom)

img_standard.save('tai_lieu_hoi_nghi_qr.png', dpi=(300, 300))
img_standard.save('tai_lieu_hoi_nghi_qr.pdf', 'PDF', resolution=300.0)
print("Saved tai_lieu_hoi_nghi_qr.png and tai_lieu_hoi_nghi_qr.pdf")

# 3. A4 Poster (2480 x 3508 px @ 300 DPI)
W_a4, H_a4 = 2480, 3508
img_a4 = Image.new('RGB', (W_a4, H_a4), 'white')
draw_a4 = ImageDraw.Draw(img_a4)

font_top_a4 = ImageFont.truetype(FONT_PATH, 140)
font_bottom_a4 = ImageFont.truetype(FONT_PATH, 115)

bbox_top_a4 = draw_a4.textbbox((0, 0), TEXT_TOP, font=font_top_a4)
top_w_a4 = bbox_top_a4[2] - bbox_top_a4[0]

bbox_bottom_a4 = draw_a4.textbbox((0, 0), TEXT_BOTTOM, font=font_bottom_a4)
bottom_w_a4 = bbox_bottom_a4[2] - bbox_bottom_a4[0]

qr_size_a4 = 1800
qr_resized_a4 = qr_img.resize((qr_size_a4, qr_size_a4), Image.Resampling.NEAREST)

x_top_a4 = (W_a4 - top_w_a4) // 2
y_top_a4 = 460

x_qr_a4 = (W_a4 - qr_size_a4) // 2
y_qr_a4 = 760

x_bottom_a4 = (W_a4 - bottom_w_a4) // 2
y_bottom_a4 = 2760

draw_a4.text((x_top_a4, y_top_a4), TEXT_TOP, fill='black', font=font_top_a4)
img_a4.paste(qr_resized_a4, (x_qr_a4, y_qr_a4))
draw_a4.text((x_bottom_a4, y_bottom_a4), TEXT_BOTTOM, fill='black', font=font_bottom_a4)

img_a4.save('tai_lieu_hoi_nghi_qr_A4.png', dpi=(300, 300))
img_a4.save('tai_lieu_hoi_nghi_qr_A4.pdf', 'PDF', resolution=300.0)
print("Saved tai_lieu_hoi_nghi_qr_A4.png and tai_lieu_hoi_nghi_qr_A4.pdf")

# 4. Pure Vector SVG for infinite scalability
matrix = qr.get_matrix()
modules_count = len(matrix)
svg_w = 800
svg_h = 1050
svg_qr_size = 560
svg_qr_offset_x = (svg_w - svg_qr_size) / 2
svg_qr_offset_y = 230
cell_size = svg_qr_size / modules_count

rects = []
for r, row in enumerate(matrix):
    for c, val in enumerate(row):
        if val:
            x = svg_qr_offset_x + c * cell_size
            y = svg_qr_offset_y + r * cell_size
            rects.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell_size:.2f}" height="{cell_size:.2f}" fill="#000000" />')

svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <rect width="100%" height="100%" fill="#ffffff" />
  <text x="{svg_w/2}" y="150" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="bold" text-anchor="middle" fill="#000000">{TEXT_TOP}</text>
  <g id="qr-code">
    {''.join(rects)}
  </g>
  <text x="{svg_w/2}" y="870" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" text-anchor="middle" fill="#000000">{TEXT_BOTTOM}</text>
</svg>
'''

with open('tai_lieu_hoi_nghi_qr.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)
print("Saved tai_lieu_hoi_nghi_qr.svg")

# 5. Standalone vector SVG
svg_only_size = 600
cell_only_size = svg_only_size / modules_count
rects_only = []
for r, row in enumerate(matrix):
    for c, val in enumerate(row):
        if val:
            x = c * cell_only_size
            y = r * cell_only_size
            rects_only.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell_only_size:.2f}" height="{cell_only_size:.2f}" fill="#000000" />')

svg_only_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_only_size} {svg_only_size}" width="{svg_only_size}" height="{svg_only_size}">
  <rect width="100%" height="100%" fill="#ffffff" />
  <g id="qr-code">
    {''.join(rects_only)}
  </g>
</svg>
'''

with open('qr_code_only.svg', 'w', encoding='utf-8') as f:
    f.write(svg_only_content)
print("Saved qr_code_only.svg")

# 6. Verification with OpenCV QR detector
print("\n--- VERIFICATION OF DECODED URLS ---")
detector = cv2.QRCodeDetector()

for fname in ['qr_code_only.png', 'tai_lieu_hoi_nghi_qr.png', 'tai_lieu_hoi_nghi_qr_A4.png']:
    img_cv = cv2.imread(fname)
    decoded_text, points, _ = detector.detectAndDecode(img_cv)
    print(f"File '{fname}': decoded='{decoded_text}'")
    assert decoded_text == URL, f"Verification failed for {fname}! Got {decoded_text}"

print("All QR codes successfully verified and decoded!")
