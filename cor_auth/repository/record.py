from typing import List

from sqlalchemy.orm import Session

from cor_auth.database.models import Record
from cor_auth.schemas import RecordModel, RecordResponse
from cor_auth.services.cipher import encrypt_data, decrypt_data, generate_aes_key


async def get_records(skip: int, limit: int, db: Session) -> List[Record]:
    """
    Get a list of records from the database.

    :param skip: The number of records to skip.
    :param limit: The maximum number of records to retrieve.
    :param db: The database session used to interact with the database.
    :return: A list of record objects.
    """
    records = db.query(Record).offset(skip).limit(limit).all()
    record_dicts = [
        {"record": str(record.record), "id": record.id} for record in records
    ]
    return record_dicts


async def get_record(record_id: int, db: Session, encryption_key: str) -> Record:
    """
    Get a record from the database by its ID.

    :param record_id: The ID of the record to retrieve.
    :param db: The database session used to interact with the database.
    :param encryption_key: The encryption key used to decrypt the record
    :return: The retrieved record object.
    """
    encryption_key = generate_aes_key(encryption_key)
    record = db.query(Record).filter(Record.id == record_id).first()
    if record:
        decrypted_record_data = decrypt_data(record.record, encryption_key)
        record.record = decrypted_record_data
    return record


async def create_record(
    body: RecordModel, db: Session, encryption_key: str
) -> RecordResponse:
    """
    Create a new record in the database.

    :param body: The record data used to create the record.
    :param db: The database session used to interact with the database.
    :param encryption_key: The encryption key used to encrypt the record.
    :return: The created record response object.
    """
    encryption_key = generate_aes_key(encryption_key)
    record_data = body.record
    encrypted_record_data = encrypt_data(record_data, encryption_key)
    record = Record(record=encrypted_record_data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return RecordResponse(id=record.id, record=str(record.record))


async def update_record(
    record_id: int, body: RecordModel, db: Session, encryption_key: str
) -> Record | None:
    """
    Update an existing record in the database.

    :param record_id: The ID of the record to update.
    :param body: The updated record data.
    :param db: The database session used to interact with the database.
    :return: The updated record object if found, else None.
    """
    encryption_key = generate_aes_key(encryption_key)
    record = db.query(Record).filter(Record.id == record_id).first()
    if record:
        record.record = encrypt_data(body.record, encryption_key)
        db.commit()
    return RecordResponse(id=record.id, record=str(record.record))


async def remove_record(record_id: int, db: Session) -> Record | None:
    """
    Remove a record from the database.

    :param record_id: The ID of the record to remove.
    :param db: The database session used to interact with the database.
    :return: The removed record object if found, else None.
    """
    record = db.query(Record).filter(Record.id == record_id).first()
    if record:
        db.delete(record)
        db.commit()
    return record
