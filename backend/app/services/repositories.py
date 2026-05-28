from abc import ABC, abstractmethod

from app import job_store
from app.models import Job


class JobRepository(ABC):
    @abstractmethod
    def create_job(self) -> Job:
        pass

    @abstractmethod
    def get_job(self, job_id: str) -> Job | None:
        pass

    @abstractmethod
    def list_jobs(self) -> list[Job]:
        pass

    @abstractmethod
    def update_job(self, job_id: str, updates: dict) -> Job | None:
        pass


class LocalJobRepository(JobRepository):
    def create_job(self) -> Job:
        return job_store.create_job()

    def get_job(self, job_id: str) -> Job | None:
        return job_store.get_job(job_id)

    def list_jobs(self) -> list[Job]:
        return job_store.list_jobs()

    def update_job(self, job_id: str, updates: dict) -> Job | None:
        return job_store.update_job(job_id, updates)


class DynamoDBJobRepository(JobRepository):
    def create_job(self) -> Job:
        raise NotImplementedError("DynamoDB repository is prepared but not implemented yet")

    def get_job(self, job_id: str) -> Job | None:
        raise NotImplementedError("DynamoDB repository is prepared but not implemented yet")

    def list_jobs(self) -> list[Job]:
        raise NotImplementedError("DynamoDB repository is prepared but not implemented yet")

    def update_job(self, job_id: str, updates: dict) -> Job | None:
        raise NotImplementedError("DynamoDB repository is prepared but not implemented yet")