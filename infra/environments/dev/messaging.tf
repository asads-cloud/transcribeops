resource "aws_sqs_queue" "transcription_dlq" {
  name = "${local.name_prefix}-transcription-dlq"

  message_retention_seconds = 1209600

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_sqs_queue" "transcription_queue" {
  name = "${local.name_prefix}-transcription-queue"

  visibility_timeout_seconds = 300
  message_retention_seconds  = 345600

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.transcription_dlq.arn
    maxReceiveCount     = 3
  })

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}