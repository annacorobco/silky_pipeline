from config import VENDORS, HEADERS, BATCH_LEN
from db import MongoDBClient
from dedupe import Deduplicator
from fetch import fetch_data
from models import UnifiedAsset
from utils import logger


DB = MongoDBClient()


def run() -> None:
    logger.info('Started processing the data')
    # 3. Step -  Preparing for deduping
    unique_ids = Deduplicator.get_all_unique_ids(model=UnifiedAsset)
    for vendor, normalize_handler in VENDORS.items():
        # 1. Step - fetching. Getting all the data for all the vendors
        params = {
            'skip': 0,
            'limit': 1  # for testing purposes - that is what mockup allows, not to be greater than 2
        }
        try:
            data = fetch_data(vendor=vendor, headers=HEADERS, params=params)
        except Exception as e:
            logger.error(f'{e}. Cannot proceed')

        if not data:
            logger.info(f'All the records for {vendor} have been processed. Finished the fetching')
            continue

        while data:
            docs = []
            # 2. Step - Normalizing
            handler = normalize_handler(data=data)
            for doc in handler.normalize():
                # 3. Step - Deduping
                if not Deduplicator.is_doc_unique(doc=doc, unique_ids=unique_ids):
                    continue

                # 4. Step - Save in batches to DB
                docs.append(doc.to_mongo().to_dict())
                if len(docs) >= BATCH_LEN:
                    DB.insert_documents(docs=docs, model_class=handler.base_model)
                    logger.info(f'Inserted batch of {BATCH_LEN} records')
                    docs = []
            if docs:
                DB.insert_documents(docs=docs, model_class=handler.base_model)
                logger.info(f'Inserted batch of {BATCH_LEN} records')

            params['skip'] += params['limit']
            if params['skip'] > 7:
                # As we never reach end of data (data=[]) using the provided mockup
                # And as we get this condition:
                # {
                #     "code": "too_big",
                #     "maximum": 7,
                #     "type": "number",
                #     "inclusive": true,
                #     "exact": false,
                #     "message": "Number must be less than or equal to 7",
                #     "path": []
                # }
                # So I add this extra row that checks skip_nr and considers that data has been
                # collected if skip_nr > 7
                # Otherwise we will exit the loop when data is [] -> then there is no more data
                # returned by API
                break

            try:
                data = fetch_data(vendor=vendor, headers=HEADERS, params=params)
            except Exception as e:
                logger.error(f'{e}. Cannot proceed')

        logger.info(f'All the records for {vendor} have been processed. Finished the fetching')
        continue


if __name__ == '__main__':
    run()
