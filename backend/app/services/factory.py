from app import config
from app.services.queue import LocalQueueService, QueueService, SQSQueueService
from app.services.repositories import DynamoDBJobRepository, JobRepository, LocalJobRepository
from app.services.storage import LocalStorageService, S3StorageService, StorageService


def get_storage_service() -> StorageService:
    if config.STORAGE_MODE == "local":
        return LocalStorageService()

    if config.STORAGE_MODE == "aws":
        return S3StorageService()

    raise ValueError(f"Unsupported STORAGE_MODE: {config.STORAGE_MODE}")


def get_queue_service() -> QueueService:
    if config.QUEUE_MODE == "local":
        return LocalQueueService()

    if config.QUEUE_MODE == "aws":
        return SQSQueueService()

    raise ValueError(f"Unsupported QUEUE_MODE: {config.QUEUE_MODE}")


def get_job_repository() -> JobRepository:
    if config.DATABASE_MODE == "local":
        return LocalJobRepository()

    if config.DATABASE_MODE == "aws":
        return DynamoDBJobRepository()

    raise ValueError(f"Unsupported DATABASE_MODE: {config.DATABASE_MODE}")