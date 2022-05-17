import React from "react"
import { Link } from "react-router-dom"

import config from "src/config"
import logo from "src/logo.svg"

export default function Logo(props: any) {
  return (
    <Link to="/" {...props} className="cursor-pointer">
      <img src={logo} alt={config.appName} className="h-12" />
    </Link>
  )
}
