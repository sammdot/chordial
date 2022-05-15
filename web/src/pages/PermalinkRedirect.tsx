import { useCallback, useEffect } from "react"
import { useNavigate, useParams } from "react-router"

import { Dictionary, User } from "src/api/models"
import Error from "src/components/Error"
import Loader from "src/components/Loader"
import { useApiQuery } from "src/utils/hooks"

type Params = {
  uid: string
}

type ItemType = "user" | "dict"
type Item = User | Dictionary

type Props = {
  type: ItemType
}

function buildApiUrl(uid: string, type: ItemType): string | undefined {
  if (type === "user") {
    return `/users/${uid}`
  } else if (type === "dict") {
    return `/dicts/${uid}`
  }
}

function buildRedirectUrl(type: ItemType, data: Item): string | undefined {
  if (type === "user") {
    let user = data as User
    return `/${user.username}`
  } else if (type === "dict") {
    let dict = data as Dictionary
    return `/${dict.user.username}/${dict.name}`
  }
}

export default function PermalinkRedirect({ type }: Props) {
  const navigateTo = useNavigate()
  const { uid } = useParams<Params>()
  const { loading, data, error } = useApiQuery<Item | undefined>(
    useCallback(
      (api) => {
        let url = buildApiUrl(uid!, type)
        if (url) {
          return api.get(url!)
        }
        return Promise.resolve(undefined)
      },
      [uid]
    )
  )

  useEffect(() => {
    if (!loading && data) {
      let url = buildRedirectUrl(type, data)
      if (url) {
        navigateTo(url!)
      }
    }
  }, [loading, data])

  return loading ? <Loader /> : error ? <Error err={error} /> : <></>
}
