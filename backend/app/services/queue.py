from abc import ABC, abstractmethod
from uuid import UUID


class QueueService(ABC):
    @abstractmethod
    def enqueue_transcription_job(self, job_id: UUID, upload_key: str, transcript_key: str, model: str) -> None:
        pass


class LocalQueueService(QueueService):
    def enqueue_transcription_job(self, job_id: UUID, upload_key: str, transcript_key: str, model: str) -> None:
        return None


class SQSQueueService(QueueService):
    def enqueue_transcription_job(self, job_id: UUID, upload_key: str, transcript_key: str, model: str) -> None:
        raise NotImplementedError("SQS queue is prepared but not implemented yet")