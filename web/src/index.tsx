import React from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter as Router } from "react-router-dom"

import "src/index.css"
import App from "src/App"

const container = document.getElementById("root") as HTMLElement
const root = createRoot(container)
root.render(
  <React.StrictMode>
    <Router>
      <App />
    </Router>
  </React.StrictMode>
)
