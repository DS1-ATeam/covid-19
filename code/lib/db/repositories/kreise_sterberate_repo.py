from lib.db.repositories.abstract_repo import AbstractRepository
from lib.config.Configuration import Configuration


class KreiseSterberateRepository(AbstractRepository):
    def __init(self, table_name = 'kreise_sterberate', connection_string = Configuration.db_connection):
        AbstractRepository.__init__(table_name, connection_string)


#repo = KreiseSterberateRepository('kreise_sterberate', Configuration.db_connection)
