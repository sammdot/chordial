import React, { useCallback } from "react"
import { useParams } from "react-router"

import { Dictionary } from "src/api/models"
import DictInfo from "src/components/DictInfo"
import Error from "src/components/Error"
import { useApiQuery } from "src/utils/hooks"

type Params = {
  user: string
  dict: string
}

export default function DictDetail() {
  const { user, dict } = useParams<Params>()
  const { loading, data, error } = useApiQuery<Dictionary>(
    useCallback((api) => api.dictByName(user!, dict!), [user, dict]),
    useCallback((d: Dictionary) => `${d.user.username}/${d.name}`, [])
  )

  return loading ? (
    <></>
  ) : data ? (
    <>
      <DictInfo dict={data} />
    </>
  ) : (
    <Error err={error} />
  )
}
