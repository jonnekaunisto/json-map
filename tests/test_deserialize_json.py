import pytest
import os
import sys
import json

from pyser import (JSONBase, SerializeField, DeserializeField,
                   DeserializeObjectField)

currPath = os.path.dirname(os.path.abspath(__file__))
raw_json = '{\"name\": \"basket\", \"fruit\": \"banana\", \"ref\": 123,\
            \"intString\": 12345}'
test_data_path = currPath + os.sep + 'test_data' + os.sep
fruit_basket_test_file = test_data_path + 'fruitBasket.json'
fruit_basket_missing_field_file = test_data_path +\
                                  'fruitBasketMissingField.json'

video_test_file = test_data_path + 'videos_test.json'


class FruitBasket(JSONBase):
    def __init__(self):
        super().__init__()
        self.name = DeserializeField()
        self.fruit = DeserializeField()
        self.iD = DeserializeField(name='ref', kind=int)
        self.private = ''
        # self.created = DeserializeField(kind=Time)
        self.intString = DeserializeField(kind=int)
        self.optionalString = DeserializeField(kind=str, optional=True)
        self.init_deserialize_json()

        self.name = SerializeField()
        self.fruit = SerializeField()
        self.iD = SerializeField(name='ref', kind=int)
        self.private = ''  # alternatively self.private = Field(private=True)
        # self.created = Field(kind=Time)
        self.intString = SerializeField(kind=int)
        self.init_serialize_json()


class VideoListResponse(JSONBase):
    def __init__(self):
        super().__init__()

        self.videos = DeserializeObjectField(name="items", repeated=True,
                                             kind=YouTubeVideo)
        self.init_deserialize_json()


class YouTubeVideo(JSONBase):
    def __init__(self):
        super().__init__()
        self.id = DeserializeField()
        self.title = DeserializeField(parent_keys=['snippet'])
        self.thumb = DeserializeField(name="url",
                                           parent_keys=["snippet",
                                                        "thumbnails",
                                                        "maxres"])

        self.snippet = DeserializeObjectField(kind=Snippet)
        self.init_deserialize_json()


class Snippet(JSONBase):
    def __init__(self):
        super().__init__()
        self.title = DeserializeField()

        self.init_deserialize_json()


class FruitBasketNotCallable(JSONBase):
    def __init__(self):
        super().__init__()
        self.name = DeserializeField(kind="not a valid kind")
        self.init_deserialize_json()


def test_deserialize_raw_json():
    basket = FruitBasket()
    basket.from_json(raw_json=raw_json)
    assert basket.name == "basket"
    assert basket.fruit == "banana"
    assert basket.iD == 123
    assert basket.intString == 12345


def test_deserialize_file():
    basket = FruitBasket()
    basket.from_json(filename=fruit_basket_test_file)
    assert basket.name == "basket"
    assert basket.fruit == "banana"
    assert basket.iD == 123
    assert basket.intString == 12345


def test_complex_deserialize():
    with open(video_test_file, 'r') as f:
        raw_json = f.read()
    data_dict = json.loads(raw_json)

    videoResponse = VideoListResponse()
    videoResponse.from_json(filename=video_test_file)

    for i, video in enumerate(videoResponse.videos):
        d_vid = data_dict["items"][i]
        assert video.id == d_vid['id']
        assert video.title == d_vid['snippet']['title']
        assert video.thumb == d_vid["snippet"]["thumbnails"]["maxres"]["url"]
        assert video.snippet.title == video.title


def test_deserialize_negative():
    with pytest.raises(Exception, match="Kind needs to be callable"):
        basket = FruitBasketNotCallable()

    with pytest.raises(Exception, match='Specify filename or raw json'):
        basket = FruitBasket()
        basket.from_json()

    with pytest.raises(Exception, match='fruit field not found in the json'):
        basket = FruitBasket()
        basket.from_json(filename=fruit_basket_missing_field_file)


def test_deserialize_str():
    str(DeserializeField())
