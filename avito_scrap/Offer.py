import io
import json

import requests
from PIL import Image


class Offer:
    def __init__(self):
        self.name = str()
        self.description = str()
        self.price = int()
        self.photo = []
        self.link = str()
        self.geo = str()
        self.time = str()

    def to_json(self):
        offer = {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'photo': self.photo,
            'link': self.link,
            'geo': self.geo,
            'time': self.time
        }
        return json.dumps(offer)

    def from_json(self, ofj):
        ofj = json.loads(ofj)
        self.name = ofj['name']
        self.description = ofj['description']
        self.price = ofj['price']
        self.photo = ofj['photo']
        self.link = ofj['link']
        self.geo = ofj['geo']
        self.time = ofj['time']
        return self

    def to_sql(self):
        if self.photo:
            photo = str()
            for i in self.photo:
                photo = photo + i + ' '
        else:
            photo = ''
        price = 'NULL'
        if self.price != 'NULL':
            price = int(self.price)
        sql_params = (self.name, self.description, price, photo, self.link, self.geo, self.time)
        return sql_params

    def from_sql(self, ofsql):
        self.name = ofsql[1]
        self.description = ofsql[2]
        price = str(ofsql[3])
        if price == "NULL":
            self.price = price
        else:
            self.price = int(price)
        self.photo = ofsql[4].split()
        self.link = ofsql[5]
        self.geo = ofsql[6]
        self.time = ofsql[7]
        return self

    def download_image(self):
        link_to_img = self.photo
        images_bytes = []
        images_pil = []
        if link_to_img:
            for i in link_to_img:
                img_bytes = requests.get(i).content
                images_bytes.append(img_bytes)
                img_pil = Image.open(io.BytesIO(img_bytes))
                images_pil.append(img_pil)
        return images_bytes, images_pil

    def __str__(self):
        name = self.name + '\n'
        if self.description:
            description = self.description[:100] + '\n'
        else:
            description = ''
        price = str(self.price) + '\n'
        if self.photo:
            photo = str()
            for i in self.photo:
                photo = photo + i + ' '
            photo += '\n'
        else:
            photo = ''
        link = self.link + '\n'
        geo = self.geo + '\n'
        time = self.time + '\n'
        return f'{name}{description}{price}{link}{photo}{geo}{time}\n'

    def __repr__(self):
        return self.name
