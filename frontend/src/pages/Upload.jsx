import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createJob, uploadFile } from "../api";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    if (!file) {
      setError("Please choose an audio file first.");
      return;
    }

    try {
      setIsUploading(true);

      const job = await createJob();
      await uploadFile(job.job_id, file);

      navigate(`/jobs/${job.job_id}`);
    } catch (err) {
      setError(err.message || "Something went wrong during upload.");
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <section className="card">
      <h1>Upload audio</h1>

      <p>
        Select a short audio file. The backend will create a job, save the file,
        and the worker will process it asynchronously.
      </p>

      <form onSubmit={handleSubmit} className="upload-form">
        <input
          type="file"
          accept="audio/*"
          onChange={(event) => setFile(event.target.files[0])}
        />

        <button type="submit" disabled={isUploading}>
          {isUploading ? "Uploading..." : "Start transcription"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}
    </section>
  );
}