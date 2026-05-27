import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getJob, getTranscript } from "../api";

export default function JobStatus() {
  const { jobId } = useParams();

  const [job, setJob] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let intervalId;

    async function pollJob() {
      try {
        const jobData = await getJob(jobId);
        setJob(jobData);

        if (jobData.status === "completed") {
          const transcriptText = await getTranscript(jobId);
          setTranscript(transcriptText);
          clearInterval(intervalId);
        }

        if (jobData.status === "failed") {
          clearInterval(intervalId);
        }
      } catch (err) {
        setError(err.message || "Failed to load job.");
        clearInterval(intervalId);
      }
    }

    pollJob();
    intervalId = setInterval(pollJob, 3000);

    return () => clearInterval(intervalId);
  }, [jobId]);

  return (
    <section className="card">
      <h1>Job Status</h1>

      <p className="job-id">Job ID: {jobId}</p>

      {error && <p className="error">{error}</p>}

      {job && (
        <>
          <div className={`status ${job.status}`}>
            Status: {job.status}
          </div>

          {job.error_message && (
            <p className="error">{job.error_message}</p>
          )}
        </>
      )}

      {transcript && (
        <div className="transcript">
          <h2>Transcript</h2>
          <pre>{transcript}</pre>
        </div>
      )}
    </section>
  );
}