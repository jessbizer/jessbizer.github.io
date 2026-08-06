#!/usr/bin/env python3
"""
generate_thumbnails.py

Enhanced thumbnail generator for the repo.
- Produces JPEG thumbnails at 200px width (thumbs/<original>.<ext>)
- Also saves a WebP sibling (thumbs/<original>.webp) for each image
- Overwrites existing thumbnails so re-running is safe

Usage:
  - Install Pillow: pip install pillow
  - From the repo root run: python generate_thumbnails.py

This script is safe to run in CI (GitHub Actions) and will create/update the thumbs/ directory.
"""

from PIL import Image
import os
import sys

SRC_DIR = '.'
DST_DIR = 'thumbs'
WIDTHS = [200]  # base thumb width; additional widths can be added if you update images.html
QUALITY = 75

if not os.path.isdir(DST_DIR):
    os.makedirs(DST_DIR)

allowed_ext = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

files = [f for f in os.listdir(SRC_DIR) 
         if f.endswith(allowed_ext) and not f.startswith('.') and os.path.isfile(f) and not f.startswith(DST_DIR + os.sep)]

if not files:
    print('No image files found in the repository root to thumbnail.')
    sys.exit(0)

for fname in files:
    src_path = os.path.join(SRC_DIR, fname)
    name, ext = os.path.splitext(fname)
    try:
        with Image.open(src_path) as im:
            # Normalize to RGB
            if im.mode in ('RGBA', 'LA'):
                bg = Image.new('RGB', im.size, (255,255,255))
                bg.paste(im, mask=im.split()[-1])
                im = bg
            else:
                im = im.convert('RGB')

            # Generate base thumbnail at WIDTHS[0] and also a WebP version
            w = WIDTHS[0]
            wpercent = (w / float(im.size[0]))
            hsize = int((float(im.size[1]) * float(wpercent)))
            thumb = im.resize((w, hsize), Image.LANCZOS)

            # JPEG output (preserve original extension as .jpg/.jpeg)
            dst_jpeg = os.path.join(DST_DIR, name + ext.lower())
            thumb.save(dst_jpeg, 'JPEG', quality=QUALITY, optimize=True)
            print(f'Wrote {dst_jpeg}')

            # WebP output
            dst_webp = os.path.join(DST_DIR, name + '.webp')
            try:
                thumb.save(dst_webp, 'WEBP', quality=QUALITY, method=6)
                print(f'Wrote {dst_webp}')
            except Exception as e:
                # Pillow build may not support WebP; ignore but report
                print(f'Could not write WebP for {fname}: {e}')

    except Exception as e:
        print(f'Failed to process {src_path}: {e}')
