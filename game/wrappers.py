#import pygame
#from pygame.color import THECOLORS as COLOURS

from local.asciisprites import Image


class MissingData(Exception):
    def __init__(s, msg, list):
        s.item = msg
        s.list = list
        #Exception.__init__(s, msg)
    def __str__(s):
        return "Item '" + s.item + "' not found in " + s.list + "."


class ImageContainer(dict):

    def __init__(s, input_):
        ''' _input: The raw ascii '''
        s._data = input_

    def get_image(s, item):
        if item not in s._data:
            raise MissingData(item, 'images')

        if not isinstance(s._data[item], Image):
            # Parse it, if not already done.
            s._format(item)
        return s._data[item]

    def get(s, item):
        return s.get_image(item)

    def _format(s, item):
        new_image = Image(s._data[item]['sprite'], s._data[item]['colours'])
        s._data[item] = new_image

    def append_data(s, new_data):
        for i in new.data.iter():
            appdend_item(i)

    def append_item(s, item):
        # Append a new item to the list
        pass
    def change_item(s, name, newitem):
        # Change an item with another
        pass
    def interchange_item(s, name, name2):
        pass
    def delete_item(s, name):
        pass
    def pop(s, name):
        return s._data.pop(name)

class SoundContainer:

    def __init__(s):
        pass
