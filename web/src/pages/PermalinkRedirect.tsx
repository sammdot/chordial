import { useCallback, useEffect } from "react"
import { useNavigate, useParams } from "react-router"

import {
  Dictionary,
  User,
  OutlineResults,
  TranslationResults,
} from "src/api/models"
import Error from "src/components/Error"
import Loader from "src/components/Loader"
import { useApiQuery } from "src/utils/hooks"

type Params = {
  uid: string
}

type ItemType = "user" | "dict" | "outline" | "translation"
type Item = User | Dictionary | OutlineResults | TranslationResults

type Props = {
  type: ItemType
}

function buildApiUrl(uid: string, type: ItemType): string | undefined {
  if (type === "user") {
    return `/users/${uid}`
  } else if (type === "dict") {
    return `/dicts/${uid}`
  } else if (type === "outline") {
    return `/outlines/${uid}`
  } else if (type === "translation") {
    return `/translations/${uid}`
  }
}

function buildRedirectUrl(type: ItemType, data: Item): string | undefined {
  if (type === "user") {
    let user = data as User
    return `/${user.username}`
  } else if (type === "dict") {
    let dict = data as Dictionary
    return `/${dict.user.username}/${dict.name}`
  } else if (type === "outline") {
    let ol = (data as OutlineResults).outline
    return `/outlines/${ol.layout?.short_name}/${ol.steno}`
  } else if (type === "translation") {
    let tl = (data as TranslationResults).translation
    return `/translations/${tl.layout?.short_name}/${tl.translation}`
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
      [uid, type]
    )
  )

  useEffect(() => {
    if (!loading && data) {
      let url = buildRedirectUrl(type, data)
      if (url) {
        navigateTo(url!)
      }
    }
  }, [loading, data, type, navigateTo])

  return loading ? <Loader /> : error ? <Error err={error} /> : <></>
}
