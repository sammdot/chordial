import { Dispatch, useContext, useEffect, useState } from "react"

import { ApiContext, ChordialApi } from "src/api"
import { ChordialApiError } from "src/api/ChordialApi"
import { setDocumentTitle } from "src/utils/title"

type ApiQueryResult<T> = {
  loading: boolean
  data?: T
  error?: ChordialApiError
}

export function useApiQuery<T>(
  queryFn: (api: typeof ChordialApi) => Promise<T>,
  titleFn?: (_: T) => string | undefined
): ApiQueryResult<T> {
  const api = useContext(ApiContext)
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState<T>()
  const [error, setError] = useState<ChordialApiError>()

  useEffect(() => {
    setLoading(true)
    queryFn(api)
      .then((data: T) => {
        setData(data)
        if (titleFn) {
          setDocumentTitle(titleFn(data))
        }
        setLoading(false)
      })
      .catch((err: ChordialApiError) => {
        setError(err)
        setLoading(false)
      })
  }, [api, queryFn, titleFn])

  return { loading, data, error }
}

export function useAuth(): [string | undefined, Dispatch<string | undefined>] {
  const [authToken, setStoredToken] = useState<string | undefined>(() => {
    let token = window.localStorage.getItem("token") || undefined
    ChordialApi.authToken = token
    return token
  })

  const setAuthToken = (value?: string) => {
    if (value) {
      window.localStorage.setItem("token", value)
    } else {
      window.localStorage.removeItem("token")
    }
    ChordialApi.authToken = value
    setStoredToken(value)
  }

  return [authToken, setAuthToken]
}
