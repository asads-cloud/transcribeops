import { Link, Outlet } from "react-router-dom";

export default function App() {
  return (
    <div className="app">
      <header className="navbar">
        <Link to="/" className="logo">TranscribeOps</Link>

        <nav>
          <Link to="/upload">Upload</Link>
          <Link to="/architecture">Architecture</Link>
          <a
            href="https://github.com/asads-cloud/transcribeops"
            target="_blank"
            rel="noreferrer"
          >
            GitHub
          </a>
        </nav>
      </header>

      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}