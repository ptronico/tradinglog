import os

from PIL import Image


def handle_uploaded_file(temppath, f):
    with open(temppath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def reduce_image_size(temppath, finalpath):
    im = Image.open(temppath)
    im = im.convert('RGB')
    im = im.resize(im.size, Image.ANTIALIAS)
    im.save(finalpath, quality=80)
    if os.path.exists(temppath):
        os.remove(temppath)
