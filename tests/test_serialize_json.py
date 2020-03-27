import pytest
import os
import sys
import json

from pyser import (JSONBase, SerializeField, DeserializeField, 
                   SerializeObjectField)


currPath = os.path.dirname(os.path.abspath(__file__))
test_data_path = currPath + os.sep + 'test_data' + os.sep
basket_complex_json = test_data_path + 'fruitBasketComplex.json'
with open(basket_complex_json, 'r') as f:
    basket_json = f.read()
    basket_dict = json.loads(basket_json)
    basket_json = json.dumps(basket_dict)


class FruitBasket(JSONBase):
    def __init__(self):
        super().__init__()
        self.name = SerializeField()
        self.fruit = SerializeField()
        self.iD = SerializeField(name="ref", kind=int)
        self.private = ""  # alternatively self.private = Field(private=True)
        # self.created = Field(kind=Time)
        self.intString = SerializeField(kind=int)
        self.optionalString = SerializeField(optional=True)
        self.items = SerializeField(repeated=True)
        self.register = SerializeField(parent_keys=["checkout"], kind=int)
        self.amount = SerializeField(parent_keys=["checkout"], kind=int)

        self.init_serialize_json()

        self.name = DeserializeField()
        self.fruit = DeserializeField()
        self.iD = DeserializeField(name="ref", kind=int)
        self.private = ""
        # self.created = DeserializeField(kind=Time)
        self.intString = DeserializeField(kind=int)
        self.init_deserialize_json()

        self.name = "basket"
        self.optionalString = None

        self.fruit = 'banana'
        self.iD = "123"
        self.intString = "12345"
        self.items = ["paper", "rock"]
        self.register = "1"
        self.amount = "10"


class FruitBasketNotCallable(JSONBase):
    def __init__(self):
        super().__init__()
        self.name = SerializeField(kind="not a valid kind")
        self.init_serialize_json()


class FruitBasketOverlappingKeys(JSONBase):
    def __init__(self):
        super().__init__()
        self.name = SerializeField()
        self.thingy = SerializeField(parent_keys=['name'])
        self.init_serialize_json()


class VideoListResponse(JSONBase):
    def __init__(self):
        super().__init__()
        self.videos = SerializeObjectField(name="items", repeated=True)
        self.init_serialize_json()

        self.videos = []


class YouTubeVideo(JSONBase):
    def __init__(self):
        super().__init__()
        self.id = SerializeField()
        self.snippet = SerializeObjectField()
        self.init_serialize_json()


class Snippet(JSONBase):
    def __init__(self):
        super().__init__()
        self.title = SerializeField()

        self.init_serialize_json()


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
    str(SerializeField())
    str(SerializeObjectField())
