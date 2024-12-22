import json
import os

class JsonSerde:
    """
    JsonSerde is a class for serializing and deserializing JSON data to and from a file.
    Attributes:
        _path (str): The file path where the JSON data is stored.
        _content (list): The list of objects loaded from the JSON file.
    Methods:
        __init__(path):
            Initializes the JsonSerde instance with the given file path.
            If the file does not exist, it creates an empty JSON file.
        _load():
            Loads the JSON data from the file into the _content attribute.
        serialize(obj):
            Appends the given object to the _content list and writes the updated list to the file.
        deserialize():
            Returns the list of objects loaded from the JSON file.
    """
    def __init__(self, path):
        self._path = path
        self._content = []
        
        if not os.path.exists(self._path):
            with open(self._path, 'w') as f:
                json.dump(self._content, f)
        
        self._load()
    
    def _load(self):
        with open(self._path, 'r') as f:
            self._content = json.load(f)
    
    def serialize(self, obj):
        self._content.append(obj)
        with open(self._path, 'w') as f:
            json.dump(self._content, f, indent=4)
    
    def deserialize(self):
        return self._content