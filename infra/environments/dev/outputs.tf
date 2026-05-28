output "upload_bucket_name" {
  value = aws_s3_bucket.uploads.bucket
}

output "transcript_bucket_name" {
  value = aws_s3_bucket.transcripts.bucket
}

output "transcription_queue_url" {
  value = aws_sqs_queue.transcription_queue.url
}

output "transcription_dlq_url" {
  value = aws_sqs_queue.transcription_dlq.url
}

output "jobs_table_name" {
  value = aws_dynamodb_table.jobs.name
}

output "backend_policy_arn" {
  value = aws_iam_policy.backend_policy.arn
}

output "worker_policy_arn" {
  value = aws_iam_policy.worker_policy.arn
}

