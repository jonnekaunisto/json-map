import pytest
import os
import sys
import json

from pyser import (BaseJSON, SchemaJSON, SerField, DeserField, 
                   SerObjectField)


currPath = os.path.dirname(os.path.abspath(__file__))
test_data_path = currPath + os.sep + 'test_data' + os.sep
basket_complex_json = test_data_path + 'fruitBasketComplex.json'
with open(basket_complex_json, 'r') as f:
    basket_json = f.read()
    basket_dict = json.loads(basket_json)
    basket_json = json.dumps(basket_dict)


class FruitBasket(SchemaJSON, BaseJSON):
    def __init__(self):
        super().__init__()
        self.name = SerField()
        self.fruit = SerField()
        self.iD = SerField(name="ref", kind=int)
        self.private = ""  # alternatively self.private = Field(private=True)
        # self.created = Field(kind=Time)
        self.intString = SerField(kind=int)
        self.optionalString = SerField(optional=True)
        self.items = SerField(repeated=True)
        self.register = SerField(parent_keys=["checkout"], kind=int)
        self.amount = SerField(parent_keys=["checkout"], kind=int)

        self.name = DeserField()
        self.fruit = DeserField()
        self.iD = DeserField(name="ref", kind=int)
        self.private = ""
        # self.created = DeserField(kind=Time)
        self.intString = DeserField(kind=int)

        self.name = "basket"
        self.optionalString = None

        self.fruit = 'banana'
        self.iD = "123"
        self.intString = "12345"
        self.items = ["paper", "rock"]
        self.register = "1"
        self.amount = "10"


class FruitBasketNotCallable(SchemaJSON, BaseJSON):
    def __init__(self):
        super().__init__()
        self.name = SerField(kind="not a valid kind")


class FruitBasketOverlappingKeys(SchemaJSON, BaseJSON):
    def __init__(self):
        super().__init__()
        self.name = SerField()
        self.thingy = SerField(parent_keys=['name'])


class VideoListResponse(SchemaJSON, BaseJSON):
    def __init__(self):
        super().__init__()
        self.videos = SerObjectField(name="items", repeated=True)

        self.videos = []


class YouTubeVideo(SchemaJSON, BaseJSON):
    def __init__(self):
        super().__init__()
        self.id = SerField()
        self.snippet = SerObjectField()


class Snippet(SchemaJSON, BaseJSON):
    def __init__(self):
        super().__init__()
        self.title = SerField()



def test_serialize():
    basket = FruitBasket()
    assert basket.name == 'basket'
    assert basket.to_json() == basket_json


def test_serialize_file():
    temp_file = 'test_file.json'

    basket = FruitBasket()
    assert basket.name == 'basket'

    basket.to_json(filename=temp_file)

    with open(temp_file, 'r') as f:
        raw_json = f.read()
    assert raw_json == basket_json
    os.remove(temp_file)


def test_complex_serialize():
    real_dict = {'id': 1, 'snippet': {'title': 'hello world'}}
    videoResponse = VideoListResponse()

    video = YouTubeVideo()

    video.id = 1

    video.snippet = Snippet()
    video.snippet.title = "hello world"

    videoResponse.videos.append(video)
    videoResponse.videos.append(video)

    assert real_dict == video.to_dict()
    assert real_dict == videoResponse.to_dict()['items'][0]


def test_serialize_negative():
    with pytest.raises(Exception, match="Kind needs to be callable"):
        basket = FruitBasketNotCallable()

    with pytest.raises(Exception, match="var \"title\" is None"):
        video = YouTubeVideo()
        video.id = 1
        video.snippet = Snippet()
        video.to_dict()

    with pytest.raises(Exception, match="parent key \"name\" is populated"):
        basket = FruitBasketOverlappingKeys()
        basket.name = "name"
        basket.thingy = "thing"
        basket.to_dict()


def test_serialize_str():
    str(SerField())
    str(SerObjectField())
