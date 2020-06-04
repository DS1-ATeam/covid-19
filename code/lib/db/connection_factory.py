import sqlalchemy as db

#
# ConnectionFactory Class handles database connections. This is a static class and folows the singleton pattern.
#
class ConnectionFactory:
    engines = {}
    connections = {}
    meta_data = {}

    @staticmethod
    def add_connection(connection_string):
        if not connection_string in ConnectionFactory.engines.keys():
            engine = db.create_engine(connection_string)
            ConnectionFactory.engines[connection_string] = engine
            ConnectionFactory.connections[connection_string] = engine.connect()
            ConnectionFactory.meta_data[connection_string] = db.MetaData()

    @staticmethod
    def get_engine(connection_string):
        if connection_string in ConnectionFactory.engines.keys():
            return ConnectionFactory.engines[connection_string]
        else:
            return None

    @staticmethod
    def get_connection(connection_string):
        if connection_string in ConnectionFactory.connections.keys():
            return ConnectionFactory.connections[connection_string]
        else:
            return None

    @staticmethod
    def get_meta_data(connection_string):
        if connection_string in ConnectionFactory.meta_data.keys():
            return ConnectionFactory.meta_data[connection_string]
        else:
            return None
