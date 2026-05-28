data "aws_iam_policy_document" "backend_policy" {
  statement {
    effect = "Allow"

    actions = [
      "s3:PutObject",
      "s3:GetObject"
    ]

    resources = [
      "${aws_s3_bucket.uploads.arn}/*",
      "${aws_s3_bucket.transcripts.arn}/*"
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "sqs:SendMessage"
    ]

    resources = [
      aws_sqs_queue.transcription_queue.arn
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "dynamodb:PutItem",
      "dynamodb:GetItem",
      "dynamodb:UpdateItem"
    ]

    resources = [
      aws_dynamodb_table.jobs.arn
    ]
  }
}

resource "aws_iam_policy" "backend_policy" {
  name        = "${local.name_prefix}-backend-policy"
  description = "Least-privilege policy for TranscribeOps backend"
  policy      = data.aws_iam_policy_document.backend_policy.json
}

data "aws_iam_policy_document" "worker_policy" {
  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject"
    ]

    resources = [
      "${aws_s3_bucket.uploads.arn}/*"
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:PutObject",
      "s3:GetObject"
    ]

    resources = [
      "${aws_s3_bucket.transcripts.arn}/*"
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:ChangeMessageVisibility"
    ]

    resources = [
      aws_sqs_queue.transcription_queue.arn
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "dynamodb:GetItem",
      "dynamodb:UpdateItem"
    ]

    resources = [
      aws_dynamodb_table.jobs.arn
    ]
  }
}

resource "aws_iam_policy" "worker_policy" {
  name        = "${local.name_prefix}-worker-policy"
  description = "Least-privilege policy for TranscribeOps worker"
  policy      = data.aws_iam_policy_document.worker_policy.json
}