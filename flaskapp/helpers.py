from google.cloud import datastore
from typing import List
from datetime import datetime


class InvalidInputException(Exception):
    pass


class DuplicateException(Exception):
    pass

SUPPORTED_GAMES = ['Connect4']

class Model:
    """
    BaseClass for Model objects
    """

    def serialize(self):
        """
        Make json representation

        NOTE: Because of dynamic reasons, this method can see subclass attributes

        Returns:
            dictionary json response
        """

        # Use default
        return self.__dict__

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

    def update_object(self, Model, obj, key, value):
        """
        Update object of kind=Model.KIND

        Args:
            Model (class): classname of kind
            obj (object): object to write
            key (string): key to match
            value (string): value to match
        """

        # Pull object
        en = self.get_entities_by_field(Model, key, value)[0]
        en.update(obj.__dict__)
        client = self.get_client()
        client.put(en)
        return self.convert_entity_to_object(Model, en)

    def post_object(self, Model, obj: object):
        """
        Put object of kind=Model.KIND
        This includes creation only

        Args:
            Model (class): classname of kind
            obj (object): object to put 

        Returns:
            List[object]: List of backend objects
        """
        client = self.get_client()
        key = client.key(Model.KIND)
        entity = datastore.Entity(key)
        entity.update(obj.__dict__)
        client.put(entity)
        print("Put: {}".format(obj))
        return obj

    def get_objects_by_field(self, Model, key: str, value: str):
        """
        Get backend objects of kind=Model.KIND, given a key=value match

        Args:
            Model (class): classname of kind
            key (str): key to match
            value (any): value to match 

        Returns:
            List[object]: List of backend objects
        """
        objs = self.convert_entities_to_objects(Model,
                                                self.get_entities_by_field(Model, key, value))
        print('GET: {}'.format(objs))
        return objs

    def get_objects(self, Model):
        """
        Get backend objects of kind=Model.KIND, given a key=value match

        Args:
            Model (class): classname of kind

        Returns:
            List[object]: List of backend objects
        """
        objs = self.convert_entities_to_objects(Model,
                                                self.get_entities(Model))
        print('GET: {}'.format(objs))
        return objs

    def get_object_by_field(self, Model, key: str, value: str):
        """
        Get backend object of kind=Model.KIND, given a key=value match

        Args:
            Model (class): classname of kind
            key (str): key to match
            value (any): value to match 

        Returns:
            object: First backend match
        """
        objs = self.convert_entities_to_objects(Model,
                                                self.get_entities_by_field(Model, key, value))
        obj = objs[0] if len(objs) else None
        print('GET: {}'.format(obj))
        return obj

    def convert_entities_to_objects(self, Model, entities):
        """
        Convert entities to objects

        Args:
            Model (class): class to convert to
            entities (List[Entity]): List of entities

        Returns:
            List[object]: List of objects of type Model
        """

        items = []
        for en in entities:
            item = Model()
            for k, y in en.items():
                setattr(item, k, y)
            items.append(item)
        return items

    def convert_entity_to_object(self, Model, en):
        """
        Convert entities to objects

        Args:
            Model (class): class to convert to
            en (Entity): entity

        Returns:
            object: Object form
        """

        item = Model()
        for k, y in en.items():
            setattr(item, k, y)
        return item

    def get_entities_by_field(self, Model, key: str, value: str):
        """
        Get entities of kind=Model.KIND, given a key=value match
        
        NOTE: Expired tickets disappear from this view

        Args:
            Model (class): classname of kind
            key (str): String key
            value (any): Value to match 

        Returns:
            List[Entity]: List of entites
        """
        client = self.get_client()
        query = client.query(kind=Model.KIND)
        query.add_filter(key, '=', value)
        if hasattr(Model, 'expires'):
            query.add_filter('expires', '>', datetime.now().timestamp())
        return list(query.fetch())
    
    def get_entities(self, Model):
        """
        Get entities of kind=Model.KIND, given a key=value match
        
        NOTE: Expired tickets disappear from this view

        Args:
            Model (class): classname of kind


        Returns:
            List[Entity]: List of entites
        """
        client = self.get_client()
        query = client.query(kind=Model.KIND)
        if hasattr(Model, 'expires'):
            query.add_filter('expires', '>', datetime.now().timestamp())
        return list(query.fetch())

    def delete_by_field(self, Model, key: str, value: any) -> List[object]:
        """
        Delete entities of kind=Model.KIND, given a key=value match

        Args:
            Model (class): classname of kind
            key (str): String key
            value (any): Value to match 

        Returns:
            List[object]: List of dropped objects
        """
        client = self.get_client()
        entities = self.get_entities_by_field(Model, key, value)
        objs = self.convert_entities_to_objects(Model, entities)
        for en in entities:
            client.delete(en)
        print('DELETE: {}'.format(objs))
        return objs
