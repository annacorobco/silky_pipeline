"""
One of ways of deduping is creating unique key in DB
It has been created = ('external_ip', 'hostname', 'mac_address')
But it works while saving data to DB
This class will make deduping before saving the data
"""
from collections import defaultdict

from mongoengine import Document


class Deduplicator:
    """
    Deduplicates Host documents based on a unique key of
    (external_ip, hostname, mac_address).
    """

    @staticmethod
    def get_all_unique_ids(model: Document) -> list:
        """
        Retrieve a list of IDs for the first occurrence of each unique
        (external_ip, hostname, mac_address) combination.
        """
        seen_keys = set()
        unique_ids = []

        for doc in model.objects.only('_id', 'external_ip', 'hostname', 'mac_address'):
            key = (doc.external_ip, doc.hostname, doc.mac_address)
            if key not in seen_keys:
                seen_keys.add(key)
                unique_ids.append(key)

        return unique_ids

    @staticmethod
    def delete_duplicates(model: Document, keep_first: bool=True) -> int:
        """
        Delete duplicate documents, keeping only the first one (by insertion order).
        """
        grouped = defaultdict(list)

        # Group by composite key
        for doc in model.objects.only('_id', 'external_ip', 'hostname', 'mac_address'):
            key = (doc.external_ip, doc.hostname, doc.mac_address)
            grouped[key].append(doc.id)

        # Identify and delete duplicates
        to_delete = []
        for ids in grouped.values():
            if len(ids) > 1:
                # Keep the first and delete the rest
                to_delete.extend(ids[1:] if keep_first else ids[:-1])

        if to_delete:
            model.objects(id__in=to_delete).delete()

        return len(to_delete)

    @staticmethod
    def is_doc_unique(doc: Document, unique_ids: list) -> bool:
        if unique_ids:
            key = (doc.external_ip, doc.hostname, doc.mac_address)
            return key in unique_ids
        else:
            # On the first run this function will return that record is unique
            # even it has been already inserted previously
            # we handle it in the code by updating unique_ids (but it won't work for a many records)
            # or/and we handle it on DB level by unique key
            return True
