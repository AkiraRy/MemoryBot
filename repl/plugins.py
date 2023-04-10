import os, glob, shutil
from datetime import datetime
import random
import io
import os.path
import json

from dotenv import load_dotenv
from nsfw_detector import predict
from pathlib import Path
from PIL import Image

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError

load_dotenv()


def image_searcher(path, number, date="", size=8, rd=False):
    if size == 0:
        size = 1000

    dir_path = path
    unfiltered = (str(p.resolve()) for p in Path(dir_path).glob("**/*") if p.suffix in {".png", ".jpg"})
    image_files = []
    for img in unfiltered:
        if (os.path.getsize(img) / (1024 * 1024)) <= size:
            image_files.append(img)
    images = []

    if rd:
        images = filler(image_files, limit=number, rd=rd)
    else:
        if date:
            images = filler(image_files, limit=number, date=date)
        else:
            images = filler(image_files, limit=number)
    return images


# if used with google`s list of file, with google LEAVE DATE EMPTY
def filler(image_files, limit, date="", rd=False):
    # if we want random images
    # TODO test if this truly return me a list of paths
    if rd:
        return random.sample(image_files, limit)

    count = 0
    if (limit == 0):
        limit = None
    images = []

    # if we want images specified by date
    if date:
        for img in image_files:
            # makes date argument compatible with machine date
            modified = os.path.getmtime(img)
            modified_datetime = datetime.fromtimestamp(modified)
            specified_date = datetime.strptime(date, "%Y-%m-%d")

            # if modified date of img is the same as in arg and less then we asked
            if modified_datetime.date() == specified_date.date() and (limit is None or count < limit):
                print(f" size {(os.path.getsize(img) / (1024 * 1024))} name: {img}")
                images.append(img)
                count += 1

            if limit is not None and count == limit:
                break
    # if we want just images not specified by date
    else:
        for img in image_files:
            if limit is None or count < limit:
                images.append(img)
                count += 1
            if limit is not None and count == limit:
                break
    return images


"""
    make it with buttons each button represents folder on disk d aka telegram/image, anime, car, girls so on
      
"""


def copiesDelete(path_to_folder):
    path_to_folder = os.path.abspath(path_to_folder)
    if not os.path.exists(path_to_folder):
        print(f"there is no such folder! {path_to_folder}")
        return

    images = image_searcher(path_to_folder, number=0, size=0)

    img_dict = {
    }

    for img in images:
        value = is_nsfwPr(img)
        if value in img_dict.values():
            os.remove(img)
        else:
            img_dict[img] = value

    print("copiesDelete has ended it work!")


model = predict.load_model('./nsfw_mobilenet2.224x224.h5')


def is_nsfw(path):
    if not os.path.isfile(path):
        print(f"{path} Not a picture")
        return
    # Open image file
    results = predict.classify(model, path)
    hentai = results[path]['hentai']
    sexy = results[path]['sexy']
    porn = results[path]['porn']
    triple = hentai + sexy + porn

    if hentai >= 0.80 or (triple >= 0.80 and hentai >= 0.5):
        print(
            f"path: {path} hentai: {results[path]['hentai']} porn: {results[path]['porn']} sexy: {results[path]['sexy']}")
        return True
    if sexy >= 0.80 or (triple >= 0.80 and sexy >= 0.5):
        print(
            f"path: {path} hentai: {results[path]['hentai']} porn: {results[path]['porn']} sexy: {results[path]['sexy']}")
        return True
    if porn >= 0.80 or (triple >= 0.80 and porn >= 0.5):
        print(
            f"path: {path} hentai: {results[path]['hentai']} porn: {results[path]['porn']} sexy: {results[path]['sexy']}")
        return True

    return False


def is_nsfwPr(path):
    if not os.path.isfile(path):
        print(f"{path} Not a picture")
        return
    # Open image file
    results = predict.classify(model, path)
    return {"hentai": results[path]['hentai'], "porn": results[path]['porn'], "sexy": results[path]['sexy']}


# functions to sort between 50-100% of hentai, sexy, porn with names of folders category+number
def switchH(value, org_path):
    # MAKE SURE THESE FOLDERS EXIST I DONT WANT TO CREATE A CHECKER FOR 12 IF ELSES
    if value >= 0.9:
        target_folder = os.path.abspath('.\\hentai90')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    elif value >= 0.80:
        target_folder = os.path.abspath('.\\hentai80')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    elif value >= 0.70:
        target_folder = os.path.abspath('.\\hentai70')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    elif value >= 0.60:
        target_folder = os.path.abspath('.\\hentai60')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    else:
        pass


def switchS(value, org_path):
    if value >= 0.90:
        target_folder = os.path.abspath('.\\porn90')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    elif value >= 0.80:
        target_folder = os.path.abspath('.\\porn80')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    elif value >= 0.70:
        target_folder = os.path.abspath('.\\porn70')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    elif value >= 0.60:
        target_folder = os.path.abspath('.\\porn60')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    else:
        pass


def switchP(value, org_path):
    if value >= 0.90:
        target_folder = os.path.abspath('.\\sexy90')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    elif value >= 0.80:
        target_folder = os.path.abspath('.\\sexy80')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    elif value >= 0.70:
        target_folder = os.path.abspath('.\\sexy70')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    elif value >= 0.60:
        target_folder = os.path.abspath('.\\sexy60')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    else:
        pass


# function to sort between 3 values sexy, hent, porn if value is >=0.8 or other criteria

def switchM(list_value, org_path):
    # PATH IN TARGET_FOLDERS JUST REPLAES WITH YOUR COMFORTABLE, I`M LAZY TO MAKE MORE TRY_CATCH
    hentai = list_value['hentai']
    sexy = list_value['sexy']
    porn = list_value['porn']
    triple = hentai + sexy + porn

    if hentai >= 0.80 or (triple >= 0.75 and hentai >= 0.5):
        if not os.path.isfile(org_path):
            print(f"{org_path} Not a picture")
            return
        target_folder = os.path.abspath('D:\Images\\AnimeH')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    elif sexy >= 0.70 or (triple >= 0.8 and sexy >= 0.5):
        if not os.path.isfile(org_path):
            print(f"{org_path} Not a picture")
            return
        target_folder = os.path.abspath('D:\Images\\AnimeS')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    elif porn >= 0.65 or (triple >= 0.8 and porn >= 0.5):
        if not os.path.isfile(org_path):
            print(f"{org_path} Not a picture")
            return
        target_folder = os.path.abspath('D:\Images\\AnimeP')
        shutil.move(org_path, os.path.join(target_folder, org_path.split("\\")[-1]))
    pass


def search_folders():
    scopes = ['https://www.googleapis.com/auth/drive.readonly']
    creds_dict = json.loads(os.environ['TOKEN_JSON'])
    creds = Credentials.from_authorized_user_file(str(creds_dict), scopes=scopes)

    # create drive api client
    service = build('drive', 'v3', credentials=creds)
    folders = {}
    page_token = None
    try:

        query = "mimeType='application/vnd.google-apps.folder' and trashed = false"
        results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No folders found.')
        else:
            #print('Folders:')
            for item in items:
                # uncomment this in case of debugging
                # print(f'{item["name"]} ({item["id"]})')
                folders[item["name"]] = item["id"]

    except Exception as e:
        print('Error listing folders:', e)
        return

    return folders

def search_folderID(folders, name) :
    # folders list of folders, name - name to search
    dict = search_folders()
    # for name, id in dict.items():
    if name in dict:
        #print(f"name: {name}, id {dict[name]}")
        return dict[name]
    else:
        print("The Name is not correct or there is no such folder")

def search_files(folder_id, size=8) :
    """
        Search for files within a folder that are smaller than the specified size.

        :param folder_id: The ID of the folder to search within.
        :param max_size_mb: The maximum file size in MB.
        :return: A list of file objects that match the search criteria.
        """
    try:
        # Load credentials and create Drive API client
        scopes = ['https://www.googleapis.com/auth/drive.readonly']
        creds_dict = json.loads(os.environ['TOKEN_JSON'])
        creds = Credentials.from_authorized_user_file(str(creds_dict), scopes=scopes)
        service = build('drive', 'v3', credentials=creds)

        # Search for files within the specified folder
        query = f"'{folder_id}' in parents and trashed = false and mimeType != 'application/vnd.google-apps.folder' and (fileExtension='jpg' or fileExtension='png')"
        results = service.files().list(q=query, fields="nextPageToken, files(name, id, size)").execute()
        files = results.get("files", [])

        # Filter files by size
        filtered_files = [
            {"name": f.get("name"), "id": f.get("id"), "size": f.get("size")}
            for f in files
            if int(f.get("size", 0)) < size * 1024 * 1024
        ]
        #TODO make a complex filler for googles images, code under just returs 5 random image
        return random.sample(filtered_files, 5)


    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def download_file(file_id):
    """Downloads a file
        Args:
            real_file_id: ID of the file to download
        Returns : IO object with location.

        Load pre-authorized user credentials from the environment.
    """
    scopes = ['https://www.googleapis.com/auth/drive.readonly']
    creds_dict = json.loads(os.environ['TOKEN_JSON'])
    creds = Credentials.from_authorized_user_file(str(creds_dict), scopes=scopes)
    service = build('drive', 'v3', credentials=creds)

    try:
        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.getvalue()



if __name__ == "__main__":
    dic = search_folders()
    # print(dic)
    my_folder = search_folderID(dic, 'test')
    filedic = search_files(my_folder)
    print(filedic)
    for items in filedic:
        value = download_file(items['id'])
        image = Image.open(io.BytesIO(value))
        print(value)
        image.show()
