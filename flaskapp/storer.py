from google.cloud import datastore
from typing import List

class Storer:
    """Baseclass for Storing objects 
    """
    
    def __init__(self):
        pass

    def get_client(self):
        """Get a datastore client

        NOTE: implicitly uses envvar for project name
        """
        return datastore.Client()

    def put(self, kind: str, object: object):
        """Put a generic object
        """
        client = self.get_client()
        key = client.key(kind)
        entity = datastore.Entity(key)
        entity.update(object.__dict__)
        return object

    def get_by_field(self, kind: str, key: str, value: str) -> List[object]:
        client = self.get_client()
        query = client.query(kind=kind)
        query.add_filter(key, '=', value)
        return list(query.fetch())
        
