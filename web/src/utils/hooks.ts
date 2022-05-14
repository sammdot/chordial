import { useContext, useMemo, useState } from "react"

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
  titleFn?: (_: T) => string
): ApiQueryResult<T> {
  const api = useContext(ApiContext)
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState<T>()
  const [error, setError] = useState<ChordialApiError>()

  useMemo(() => {
    queryFn(api)
      .then((data: T) => {
        setData(data)
        setDocumentTitle(titleFn?.(data))
        setLoading(false)
      })
      .catch((err: ChordialApiError) => {
        setError(err)
        setLoading(false)
      })
  }, [api, queryFn, titleFn])

  return { loading, data, error }
}
