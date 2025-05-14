from threading import Lock

from mongoengine import connect, Document, StringField, DateTimeField
from pymongo.errors import BulkWriteError

from config import MONGODB_URI, MONGODB_DB_NAME, MONGODB_ALIAS
from utils import logger

# Use Singletone
class MongoDBClient:
    _instance = None
    _lock = Lock()

    def __new__(cls, db_name: str=MONGODB_DB_NAME, uri:str=MONGODB_URI, alias:str=MONGODB_ALIAS) -> "MongoDBClient":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MongoDBClient, cls).__new__(cls)
                cls._instance.db_name = db_name
                cls._instance.uri = uri
                cls._instance.alias = alias
                cls._instance._connect()
            return cls._instance

    def _connect(self) -> None:
        connect(
            db=self.db_name,
            host=self.uri,
            alias=self.alias
        )

    def get_connection(self) -> str:
        return self.alias

    def insert_document(self, doc: Document) -> None:
        if doc:
            doc.save()

    def insert_documents(self, docs: list[Document], model_class: type[Document], ordered: bool=False) -> None:
        if docs:
            try:
                # If ordered is set to false and an insert fails,
                # the server continues inserting records.
                model_class._get_collection().insert_many(docs, ordered=ordered)
            except BulkWriteError as bwe:
                logger.info("Some inserts failed but others succeeded.")

    def find_documents(self, model: Document, **filters) -> list:
        return model.objects(**filters)

    def delete_documents(self, model: Document, **filters) -> int:
        return model.objects(**filters).delete()
