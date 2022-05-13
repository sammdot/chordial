import { useEffect } from "react"

import config from "src/config"

export function setDocumentTitle(title?: string) {
  document.title = title ? `${title} | ${config.appName}` : config.appName
}

export default function useDocumentTitle(title?: string) {
  useEffect(() => {
    setDocumentTitle(title)
  }, [title])
}
