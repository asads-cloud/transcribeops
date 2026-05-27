export default function Architecture() {
  return (
    <section className="card">
      <h1>Architecture</h1>

      <p>
        TranscribeOps is designed as a production-style cloud platform for
        asynchronous transcription workloads.
      </p>

      <ol className="architecture-list">
        <li>User uploads an audio file through the frontend.</li>
        <li>FastAPI backend creates a transcription job.</li>
        <li>The uploaded file is stored in shared local storage.</li>
        <li>A separate worker container polls for uploaded jobs.</li>
        <li>The worker runs Whisper and creates a transcript.</li>
        <li>The frontend polls the backend until the transcript is ready.</li>
      </ol>

      <h2>Future AWS Architecture</h2>

      <p>
        This local Docker setup maps directly to the future AWS version using
        S3, SQS, DynamoDB, ECS Fargate, ALB, CloudFront, Route 53, ACM,
        CloudWatch and WAF.
      </p>
    </section>
  );
}