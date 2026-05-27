import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App.jsx";
import Home from "./pages/Home.jsx";
import Upload from "./pages/Upload.jsx";
import JobStatus from "./pages/JobStatus.jsx";
import Architecture from "./pages/Architecture.jsx";
import "./style.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route index element={<Home />} />
          <Route path="upload" element={<Upload />} />
          <Route path="jobs/:jobId" element={<JobStatus />} />
          <Route path="architecture" element={<Architecture />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);