import React, { useCallback } from "react"
import { useParams } from "react-router"

import { User } from "src/api/models"
import DictList from "src/components/DictList"
import Error from "src/components/Error"
import Loader from "src/components/Loader"
import UserInfo from "src/components/UserInfo"
import { useApiQuery } from "src/utils/hooks"

type Params = {
  user: string
}

export default function UserDetail() {
  const { user } = useParams<Params>()
  const { loading, data, error } = useApiQuery<User>(
    useCallback((api) => api.userByName(user!), [user]),
    useCallback((u: User) => u.username, [])
  )

  return loading ? (
    <Loader />
  ) : data ? (
    <>
      <UserInfo user={data} />
      <div className="w-full border-t border-gray-300 mt-6 mb-8" />
      <DictList>
        {data.dictionaries
          ?.sort((a, b) => a.name.localeCompare(b.name))
          .map((d) => (
            <DictList.Item
              user={data}
              dict={d}
              key={`${data.username}/${d.name}`}
            />
          ))}
      </DictList>
    </>
  ) : (
    <Error err={error} />
  )
}
