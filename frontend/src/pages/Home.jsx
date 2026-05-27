import { Link } from "react-router-dom";

export default function Home() {
  return (
    <section className="hero">
      <h1>Production-style AWS transcription platform</h1>

      <p>
        TranscribeOps lets users upload audio, queue a transcription job,
        process it through a Dockerised Whisper worker, and view the transcript
        in the browser.
      </p>

      <div className="actions">
        <Link className="button" to="/upload">Upload audio</Link>
        <Link className="button secondary" to="/architecture">View architecture</Link>
      </div>
    </section>
  );
}