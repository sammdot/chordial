import { useCallback, useMemo } from "react"
import { useParams } from "react-router"

import { SearchResults } from "src/api/models"
import Error from "src/components/Error"
import Loader from "src/components/Loader"
import OutlineInfo from "src/components/OutlineInfo"
import TranslationList from "src/components/TranslationList"
import { useApiQuery } from "src/utils/hooks"

type Params = {
  layout: string
  steno: string
}

export default function OutlineDetail() {
  const { layout, steno } = useParams<Params>()
  const { loading, data, error } = useApiQuery<SearchResults | undefined>(
    useCallback(
      (api) =>
        layout && steno
          ? api.searchBySteno(layout!, decodeURIComponent(steno!))
          : Promise.resolve(undefined),
      [layout, steno]
    ),
    useCallback(
      (re?: SearchResults) => re?.search.outline?.steno || undefined,
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
      <OutlineInfo outline={data.search.outline!} />
      <TranslationList
        layout={layoutName!}
        steno={data!.search.outline!.steno}
        translations={data!.entries_ranked!}
      />
    </>
  ) : (
    <Error err={error} />
  )
}
