import * as _ from "lodash"
import { useCallback, useMemo } from "react"
import { useParams } from "react-router"
import { Link } from "react-router-dom"

import { Entry, SearchResults } from "src/api/models"
import { EntryCounter, OutlineCounter } from "src/components/Counter"
import DictLink from "src/components/DictLink"
import Error from "src/components/Error"
import Loader from "src/components/Loader"
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

  const entriesBySteno = useMemo(
    () => (data ? _.groupBy(data.entries, (e: Entry) => e.outline.steno) : {}),
    [data]
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
      <div>
        <EntryCounter number={data.entries.length} className="font-semibold" />,{" "}
        <OutlineCounter
          number={Object.keys(entriesBySteno).length}
          className="font-semibold"
        />
      </div>
      <div className="my-6">
        {_.sortBy(
          Object.keys(entriesBySteno),
          (steno) => -entriesBySteno[steno].length
        ).map((steno) => {
          const outlines = entriesBySteno[steno]
          return (
            <Link
              to={`/entries/${layoutName}/${encodeURIComponent(
                steno
              )}/${encodeURIComponent(data.search.translation!.translation)}`}
              key={data.search.translation!.translation}
            >
              <div
                className="grid grid-cols-4 py-2 px-2 mx-[-0.5rem] hover:bg-gray-200 hover:rounded-md"
                key={steno}
              >
                <div className="font-mono text-xl">{steno}</div>
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
    </>
  ) : (
    <Error err={error} />
  )
}
