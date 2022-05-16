import * as _ from "lodash"
import { useCallback, useMemo } from "react"
import { useParams } from "react-router"
import { Link } from "react-router-dom"

import { Entry, EntryDetails, SearchResults } from "src/api/models"
import DictLink from "src/components/DictLink"
import EntryInfo from "src/components/EntryInfo"
import Error from "src/components/Error"
import FlagEmoji from "src/components/FlagEmoji"
import ColoredLink from "src/components/Link"
import Loader from "src/components/Loader"
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
        !loading && data && data.entries.length
          ? api.entryById(data.entries[0].uid)
          : Promise.resolve(undefined),
      [loading, data]
    )
  )

  const entriesBySteno = useMemo(
    () =>
      entryData
        ? _.groupBy(
            entryData.related.translation,
            (e: Entry) => e.outline.steno
          )
        : {},
    [entryData]
  )
  const entriesByTranslation = useMemo(
    () =>
      entryData
        ? _.groupBy(
            entryData.related.outline,
            (e: Entry) => e.translation.translation
          )
        : {},
    [entryData]
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
          <div className="mt-8">
            <div className="mb-2">
              <span className="font-semibold">
                {Object.keys(entriesBySteno).length}
              </span>{" "}
              outline
              {Object.keys(entriesBySteno).length === 1 ? "" : "s"} for '
              <ColoredLink
                to={`/translations/${layoutName}/${encodeURIComponent(
                  data!.search.translation!.translation
                )}`}
              >
                {data!.search.translation!.translation}
              </ColoredLink>
              '
            </div>
            {Object.keys(entriesBySteno).map((steno) => {
              let outlines = entriesBySteno[steno]
              return (
                <Link
                  to={`/entries/${layoutName}/${encodeURIComponent(
                    steno
                  )}/${encodeURIComponent(
                    data!.search.translation!.translation
                  )}`}
                  key={steno}
                >
                  <div
                    className="grid grid-cols-4 py-1 text-lg px-2 mx-[-0.5rem] hover:bg-gray-200 hover:rounded-md"
                    key={steno}
                  >
                    <div className="font-mono text-xl my-1">{steno}</div>
                    <div className="col-span-3">
                      {outlines.map((entry) => (
                        <div className="my-1" key={entry.uid}>
                          <DictLink
                            dict={entry.dictionary!}
                            className="text-right"
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                </Link>
              )
            })}
          </div>
          <div className="mt-8">
            <div className="mb-2">
              <span className="font-semibold">
                {Object.keys(entriesByTranslation).length}
              </span>{" "}
              translation
              {Object.keys(entriesByTranslation).length === 1
                ? ""
                : "s"} for{" "}
              <ColoredLink
                to={`/outlines/${layoutName}/${encodeURIComponent(
                  data!.search.outline!.steno
                )}`}
                className="font-mono"
              >
                {data!.search.outline!.steno}
              </ColoredLink>
            </div>
            {Object.keys(entriesByTranslation).map((tl) => {
              let entries = entriesByTranslation[tl]
              let translation = entries[0].translation
              return (
                <Link
                  to={`/entries/${layoutName}/${encodeURIComponent(
                    data!.search.outline!.steno
                  )}/${encodeURIComponent(translation.translation)}`}
                  key={tl}
                >
                  <div className="grid grid-cols-4 py-1 text-lg px-2 mx-[-0.5rem] hover:bg-gray-200 hover:rounded-md">
                    <div className="text-xl my-1">
                      {tl}
                      {translation.spelling_variant ? (
                        <FlagEmoji
                          variant={translation.spelling_variant}
                          className="ml-2"
                        />
                      ) : (
                        <></>
                      )}
                    </div>
                    <div className="col-span-3">
                      {entries.map((entry) => (
                        <div className="my-1" key={entry.uid}>
                          <DictLink
                            dict={entry.dictionary!}
                            className="text-right"
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                </Link>
              )
            })}
          </div>
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
