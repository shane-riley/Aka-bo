from google.cloud import datastore
from typing import List

class InvalidInputException(Exception):
    pass

class DuplicateException(Exception):
    pass

class Store:
    """Baseclass for Storing objects 
    """
    
    def __init__(self):
        pass

    def get_client(self):
        """Get a datastore client

        NOTE: implicitly uses envvar for project name
        """
        return datastore.Client()

    def put(self, Model, obj: object):
        """Put a generic object
        """
        client = self.get_client()
        key = client.key(Model.KIND)
        entity = datastore.Entity(key)
        entity.update(obj.__dict__)
        client.put(entity)
        print("Put: {}".format(obj))
        return obj

    def get_by_field(self, Model, key: str, value: str):
        client = self.get_client()
        query = client.query(kind=Model.KIND)
        query.add_filter(key, '=', value)
        items = []
        for en in query.fetch():
            item = Model()
            for k,y in en.items():
                setattr(item,k,y)
            items.append(item)
            print("Get: {}".format(item))
        return items
        
