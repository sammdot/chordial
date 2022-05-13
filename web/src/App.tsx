import React from "react"

import config from "src/config"
import useDocumentTitle from "src/utils/title"

import logo from "src/logo.svg"

export default function App() {
  useDocumentTitle()
  return (
    <div className="mx-auto flex justify-center items-center h-screen select-none">
      <img src={logo} alt={config.appName} />
    </div>
  )
}
