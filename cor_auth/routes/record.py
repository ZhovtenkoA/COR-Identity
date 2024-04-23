from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from cor_auth.repository import record as repository_record

from cor_auth.database.db import get_db
from cor_auth.schemas import RecordResponse, RecordModel
from cor_auth.services.roles import free_access, admin, admin_moderator
from cor_auth.conf.config import settings

router = APIRouter(prefix="/records", tags=["Records"])
encryption_key = settings.encryption_key


@router.get(
    "/", response_model=List[RecordResponse], dependencies=[Depends(free_access)]
)
async def read_records(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Get a list of records.

    :param skip: The number of records to skip (for pagination). Default is 0.
    :type skip: int
    :param limit: The maximum number of records to retrieve. Default is 50.
    :type limit: int
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: A list of RecordResponse objects representing the records.
    :rtype: List[RecordResponse]
    """
    records = await repository_record.get_records(skip, limit, db)
    return records


@router.get(
    "/{record_id}",
    response_model=RecordResponse,
    dependencies=[Depends(admin_moderator)],
)
async def read_record(record_id: int, db: Session = Depends(get_db)):
    """
    Get a specific record by ID.

    :param record_id: The ID of the record.
    :type record_id: int
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The RecordResponse object representing the record.
    :rtype: RecordResponse
    :raises HTTPException 404: If the record with the specified ID does not exist.
    """
    record = await repository_record.get_record(record_id, db, encryption_key)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )
    return record


@router.post(
    "/", response_model=RecordResponse, dependencies=[Depends(admin_moderator)]
)
async def create_record(body: RecordModel, db: Session = Depends(get_db)):
    """
    Create a new record.

    :param body: The request body containing the record data.
    :type body: RecordModel
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The created RecordResponse object representing the new record.
    :rtype: RecordResponse
    """
    return await repository_record.create_record(body, db, encryption_key)


@router.put(
    "/{record_id}", response_model=RecordResponse, dependencies=[Depends(admin)]
)
async def update_record(
    record_id: int, body: RecordModel, db: Session = Depends(get_db)
):
    """
    Update an existing record.

    :param record_id: The ID of the record to update.
    :type record_id: int
    :param body: The request body containing the updated record data.
    :type body: RecordModel
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The updated RecordResponse object representing the updated record.
    :rtype: RecordResponse
    :raises HTTPException 404: If the record with the specified ID does not exist.
    """
    record = await repository_record.update_record(record_id, body, db, encryption_key)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )
    return record


@router.delete(
    "/{record_id}", response_model=RecordResponse, dependencies=[Depends(admin)]
)
async def remove_record(record_id: int, db: Session = Depends(get_db)):
    """
    Remove a record.

    :param record_id: The ID of the record to remove.
    :type record_id: int
    :param db: The database session. Dependency on get_db.
    :type db: Session, optional
    :return: The removed RecordResponse object representing the removed record.
    :rtype: RecordResponse
    :raises HTTPException 404: If the record with the specified ID does not exist.
    """
    record = await repository_record.remove_record(record_id, db)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )
    return record
