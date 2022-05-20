import { useCallback, useMemo } from "react"
import { useParams } from "react-router"

import { EntryDetails, SearchResults } from "src/api/models"
import EntryInfo from "src/components/EntryInfo"
import Error from "src/components/Error"
import Loader from "src/components/Loader"
import OutlineList from "src/components/OutlineList"
import TranslationList from "src/components/TranslationList"
import { useApiQuery } from "src/utils/hooks"

type Params = {
  layout: string
  steno: string
  translation: string
}

export default function EntryDetail() {
  const { layout, steno, translation } = useParams<Params>()
  const { loading, data, error } = useApiQuery<SearchResults | undefined>(
    useCallback(
      (api) =>
        layout && steno && translation
          ? api.searchByStenoAndTranslation(
              layout!,
              decodeURIComponent(steno!),
              decodeURIComponent(translation!)
            )
          : Promise.resolve(undefined),
      [layout, steno, translation]
    )
  )

  const {
    loading: entryLoading,
    data: entryData,
    error: entryError,
  } = useApiQuery<EntryDetails | undefined>(
    useCallback(
      (api) =>
        !loading && data && data.entries!.length
          ? api.entryById(data.entries?.[0].uid!)
          : Promise.resolve(undefined),
      [loading, data]
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
      <EntryInfo
        outline={data!.search.outline!}
        translation={data!.search.translation!}
        layout={data!.layout}
      />
      {entryLoading ? (
        <Loader />
      ) : entryData ? (
        <>
          <OutlineList
            className="mt-8"
            layout={layoutName!}
            translation={data!.search.translation!.translation}
            outlines={entryData!.related.translation}
          />
          <TranslationList
            className="mt-8"
            layout={layoutName!}
            steno={data!.search.outline!.steno}
            translations={entryData!.related.outline}
          />
        </>
      ) : entryError ? (
        <Error err={entryError} />
      ) : (
        <></>
      )}
    </>
  ) : error ? (
    <Error err={error} />
  ) : (
    <></>
  )
}
