import os, glob
from PIL import Image
from datetime import datetime
import random

from dotenv import load_dotenv
from nsfw_detector import predict
from  pathlib import Path

load_dotenv()

def image_searcher(path, number, date="", size=8, rd=False):
    dir_path = path
    unfiltered = (p.resolve() for p in Path(dir_path).glob("**/*") if p.suffix in {".png", ".jpg"})
    image_files = []
    for img in unfiltered:
        if (os.path.getsize(img) / (1024 * 1024)) <= size:
            image_files.append(img)
    images = []

    if rd:
        images = filler(image_files, number, rd=rd)
    else:
        if date:
            images = filler(image_files, number, date=date)
        else:
            images = filler(image_files, number)

    return images


def filler(image_files, limit, date="", rd=False):
    #if we want random images
    if rd: #TODO test if this truly return me a list of paths
        return random.sample(image_files, limit)

    count = 0
    images = []

    #if we want images specified by date
    if date:
        for img in image_files:
            # makes date argument compatible with machine date
            modified = os.path.getmtime(img)
            modified_datetime = datetime.fromtimestamp(modified)
            specified_date = datetime.strptime(date, "%Y-%m-%d")

            # if modified date of img is the same as in arg and less then we asked
            if modified_datetime.date() == specified_date.date() and count < limit:
                print(f" size {(os.path.getsize(img) / (1024 * 1024))} name: {img}")
                images.append(img)
                count += 1

            if count == limit:
                break
    # if we want just images not specified by date
    else:
        for img in image_files:
            if count < limit:
                images.append(img)
                count += 1
            if count == limit:
                break
    return images

"""
    make it with buttons each button represents folder on disk d aka telegram/image, anime, car, girls so on
      
"""

model = predict.load_model('./nsfw_mobilenet2.224x224.h5')
def is_nsfw(path):
    if not os.path.isfile(path):
        print(f"{path} Not a picture")
        return
    # Open image file
    results = predict.classify(model, path)
    if (results[path]['hentai'] + results[path]['porn']) > 0.65 or (results[path]['sexy']) > 0.7:
        print(f"hentai: {results[path]['hentai']} porn: {results[path]['porn']} sexy: {results[path]['sexy']}")
        return True
    return False


if __name__ == "__main__":
    images_list = image_searcher(os.getenv('IMAGE_FOLDER'), 5, rd=True)

    for img in images_list:
        print(img)

    #image_searcher(dir_path, "2022-08-21", 1, 2)
