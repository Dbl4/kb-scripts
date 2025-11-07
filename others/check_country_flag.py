import hashlib
import os
import re
from shutil import copyfile

IMG_REGEX = re.compile('.*(\.(?:jpe?g|png|bmp|gif))', re.IGNORECASE)
IMG_DST_DIR = './data/img_dst/'
IMG_SRC_DIR = './data/img_src/'

def prepare_imgname(imgname):
    imgname = imgname.strip()
    try:
        imgname = IMG_REGEX.search(imgname)
        return imgname.group(), imgname.group(1)
    except AttributeError:
        print('{} is not valid image filename'.format(imgname))
        # raise CoercionError('{} is not valid image filename'.format(imgname))


def transform_image(old_path, ext):
    checksum = _md5(old_path)

    new_dirs = os.path.join(checksum[0:2], checksum[2:4])
    full_new_dirs = os.path.join(IMG_DST_DIR, new_dirs)
    if not os.path.exists(full_new_dirs):
        os.makedirs(full_new_dirs)

    new_filename = checksum + ext
    new_subpath = os.path.join(new_dirs, new_filename)

    new_path = os.path.join(IMG_DST_DIR, new_subpath)
    if not os.path.exists(new_path):
        copyfile(old_path, new_path)

    return new_subpath


def get_image(data):
    imgname, ext = prepare_imgname(data)
    old_path = os.path.join(IMG_SRC_DIR, imgname)
    if not os.path.exists(old_path):
        print('Image `{}` does not exist'.format(old_path))

    return transform_image(old_path, ext)


def _md5(filename):
    hash_md5 = hashlib.md5()
    # with open(filename, "rb") as f:
    #     for chunk in iter(lambda: f.read(4096), b""):
    #         hash_md5.update(chunk)
    return hash_md5.hexdigest()


print(get_image('slovenia.jpg'))
