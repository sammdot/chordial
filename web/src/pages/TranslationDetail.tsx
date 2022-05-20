import { useCallback, useMemo } from "react"
import { useParams } from "react-router"

import { SearchResults } from "src/api/models"
import Error from "src/components/Error"
import Loader from "src/components/Loader"
import OutlineList from "src/components/OutlineList"
import TranslationInfo from "src/components/TranslationInfo"
import { useApiQuery } from "src/utils/hooks"

type Params = {
  layout: string
  translation: string
}

export default function TranslationDetail() {
  const { layout, translation } = useParams<Params>()
  const { loading, data, error } = useApiQuery<SearchResults | undefined>(
    useCallback(
      (api) =>
        layout && translation
          ? api.searchByTranslation(layout!, decodeURIComponent(translation!))
          : Promise.resolve(undefined),
      [layout, translation]
    ),
    useCallback(
      (re?: SearchResults) => re?.search.translation?.translation || undefined,
      []
    )
  )

  const layoutName: string | undefined = useMemo(
    () => (data ? data.layout!.short_name : undefined),
    [data]
  )

  return loading ? (
    <Loader />
  ) : data ? (
    <>
      <TranslationInfo translation={data.search.translation!} />
      <OutlineList
        layout={layoutName!}
        translation={data!.search.translation!.translation}
        outlines={data!.entries_ranked!}
      />
    </>
  ) : (
    <Error err={error} />
  )
}
