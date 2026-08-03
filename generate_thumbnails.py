#!/usr/bin/env python3
"""
generate_thumbnails.py

Simple script to generate optimized thumbnails for this repo.
Usage:
  - Install Pillow: pip install pillow
  - From the repo root run: python generate_thumbnails.py

This will create a `thumbs/` directory and write resized JPEG thumbnails (width 200px)
for all .jpg/.jpeg/.png files in the repository root (except files already in `thumbs/`).
"""

from PIL import Image
import os
import sys

SRC_DIR = '.'
DST_DIR = 'thumbs'
WIDTH = 200
QUALITY = 75

if not os.path.isdir(DST_DIR):
    os.makedirs(DST_DIR)

allowed_ext = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

files = [f for f in os.listdir(SRC_DIR) if f.endswith(allowed_ext) and not f.startswith('.') and os.path.isfile(f) and not f.startswith(DST_DIR + os.sep)]

if not files:
    print('No image files found in the repository root to thumbnail.')
    sys.exit(0)

for fname in files:
    src_path = os.path.join(SRC_DIR, fname)
    dst_path = os.path.join(DST_DIR, fname)
    try:
        with Image.open(src_path) as im:
            # Convert PNG with alpha to RGB white background
            if im.mode in ('RGBA', 'LA'):
                bg = Image.new('RGB', im.size, (255,255,255))
                bg.paste(im, mask=im.split()[-1])
                im = bg
            else:
                im = im.convert('RGB')

            wpercent = (WIDTH / float(im.size[0]))
            hsize = int((float(im.size[1]) * float(wpercent)))
            im = im.resize((WIDTH, hsize), Image.LANCZOS)
            im.save(dst_path, 'JPEG', quality=QUALITY, optimize=True)
            print(f'Wrote {dst_path}')
    except Exception as e:
        print(f'Failed to process {src_path}: {e}')
