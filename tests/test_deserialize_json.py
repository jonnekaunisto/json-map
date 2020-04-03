import pytest
import os
import sys
import json
import re


from pyser import (BaseJSON, SchemaJSON, SerField, DeserField,
                   DeserObjectField)

currPath = os.path.dirname(os.path.abspath(__file__))
test_data_path = currPath + os.sep + 'test_data' + os.sep
fruit_basket_test_file = test_data_path + 'fruitBasket.json'
fruit_basket_missing_field_file = test_data_path +\
                                  'fruitBasketMissingField.json'

video_test_file = test_data_path + 'videos_test.json'

with open(fruit_basket_test_file, 'r') as f:
    raw_json = f.read()
    raw_dict = json.loads(raw_json)
    raw_json = json.dumps(raw_dict)


def camel_to_underscore(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def underscore_to_camel(word):
    word = ''.join(x.capitalize() or '_' for x in word.split('_'))
    word = word[0].lower() + word[1:]
    return word


class FruitBasketSchema(SchemaJSON, BaseJSON):
    def __init__(self):
        self.name = DeserField()
        self.fruit = DeserField()
        self.iD = DeserField(name_conv=lambda x: 'ref', kind=int)
        self.private = ''

        self.int_string = DeserField(name_conv=underscore_to_camel, kind=int)
        self.optionalString = DeserField(kind=str, optional=True)
        self.items = DeserField(repeated=True)
        self.name = SerField()
        self.fruit = SerField()
        self.iD = SerField(name='ref', kind=int)
        self.private = ''
        # self.created = Field(kind=Time)
        self.int_string = SerField(kind=int)


fruit_basket_schema = FruitBasketSchema()


class FruitBasket(BaseJSON):
    def __init__(self):
        self.set_schema_json(fruit_basket_schema)


class VideoListResponse(SchemaJSON, BaseJSON):
    def __init__(self):
        self.videos = DeserObjectField(name="items", repeated=True,
                                       kind=YouTubeVideo)


class YouTubeVideo(SchemaJSON, BaseJSON):
    def __init__(self):
        self.id = DeserField()
        self.title = DeserField(parent_keys=['snippet'])
        self.thumb = DeserField(name="url", parent_keys=["snippet",
                                                         "thumbnails",
                                                         "maxres"])

        self.snippet = DeserObjectField(kind=Snippet)


class Snippet(SchemaJSON, BaseJSON):
    def __init__(self):

        self.title = DeserField()


class FruitBasketNotCallable(SchemaJSON, BaseJSON):
    def __init__(self):
        self.name = DeserField(kind="not a valid kind")


def test_deserialize_raw_json():
    basket = FruitBasket()
    basket.from_json(raw_json=raw_json)
    assert basket.name == "basket"
    assert basket.fruit == "banana"
    assert basket.iD == 123
    assert basket.int_string == 12345


def test_deserialize_file():
    basket = FruitBasket()
    basket.from_json(filename=fruit_basket_test_file)
    assert basket.name == "basket"
    assert basket.fruit == "banana"
    assert basket.iD == 123
    assert basket.int_string == 12345


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
    str(DeserField())
