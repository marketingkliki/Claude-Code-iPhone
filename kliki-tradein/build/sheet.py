import sys, glob, os
from PIL import Image, ImageDraw
d, out, H = sys.argv[1], sys.argv[2], int(sys.argv[3])
fs = sorted(glob.glob(d + '/s_*.png'), key=lambda f: float(os.path.basename(f)[2:-4]))
w = 270; h = int(H * w / 1080); cols = 7; k = w / 1080
rows = (len(fs) + cols - 1) // cols
S = Image.new('RGB', (cols * w, rows * h), 'black')
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((w, h)); dr = ImageDraw.Draw(im)
    dr.rectangle([60*k, 90*k, (1080-150)*k, (H-200)*k], outline=(255, 0, 80), width=1)
    dr.rectangle([0, 0, 56, 16], fill='black'); dr.text((3, 2), os.path.basename(f)[2:-4], fill='yellow')
    S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(out)
