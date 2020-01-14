import pytest
import os

from pyser import (ConfigSectionBase, ConfigBase, CompositeConfigOption,
                   SerializeConfigOption, DeserializeConfigOption)

currPath = os.path.dirname(os.path.abspath(__file__))
test_data_path = currPath + os.sep + 'test_data' + os.sep
fruit_basket_test_file = test_data_path + 'fruitBasket.ini'