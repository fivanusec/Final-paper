import os
import imagehash
import numpy as np
from PIL import Image
from uuid import uuid4
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail


class TokenHandler:
    __token = None
    instance = None
    model_instance = None

    def __init__(self, instance=None, model_instance=None, token=None):
        self.__token = str(uuid4()) if token is None else token
        self.instance = instance
        self.model_instance = model_instance

    def create_token(self) -> None:
        cache.set(self.instance + self.__token,
                  self.model_instance.id,
                  timeout=1000 * 60 * 60 * 24 * 3)

    def get_token(self, instance, token):
        return cache.get(instance + token)

    def retrive_token(self):
        return self.__token

    def email_token(self, model_instance):
        send_mail(
            subject="Confirm your attendance",
            message=f"Here is token to confirm your attendance {self.__token}",
            from_email=[
                settings.EMAIL_HOST_USER,
            ],
            recipient_list=[
                model_instance.email,
            ])


class DuplicateRemover:

    def __init__(self, dirname, hash_size=8):
        self.dirname = dirname
        self.hash_size = hash_size

    def find_duplicates(self):
        fnames = os.listdir(self.dirname)
        hashes = {}
        duplicates = []
        print("Finding duplicates now")
        for image in fnames:
            with Image.open(os.path.join(self.dirname, image)) as img:
                temp_hash = imagehash.average_hash(img, self.hash_size)
                if temp_hash in hashes:
                    print("Duplicate {} found for Image {}".format(
                        image, hashes[temp_hash]))
                    duplicates.append(image)
                else:
                    hashes[temp_hash] = image

        if len(duplicates) != 0:
            space_saved = 0
            for duplicate in duplicates:
                space_saved += os.path.getsize(
                    os.path.join(self.dirname, duplicate))

                os.remove(os.path.join(self.dirname, duplicate))
            print("All duplicates are deleted")
        else:
            print("No Duplicates Found")

    def find_similar(self, location, similarity=80):
        fnames = os.listdir(self.dirname)
        threshold = 1 - similarity / 100
        diff_limit = int(threshold * (self.hash_size**2))

        with Image.open(location) as img:
            hash1 = imagehash.average_hash(img, self.hash_size).hash

        print("Finding Similar Images to {} Now!\n".format(location))
        for image in fnames:
            with Image.open(os.path.join(self.dirname, image)) as img:
                hash2 = imagehash.average_hash(img, self.hash_size).hash

                if np.count_nonzero(hash1 != hash2) <= diff_limit:
                    print("{} image found {}% similar to {}".format(
                        image, similarity, location))
