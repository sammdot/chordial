import * as _ from "lodash"
import { useCallback, useMemo } from "react"
import { useParams } from "react-router"

import { Entry, SearchResults } from "src/api/models"
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
    )
  )

  const entriesBySteno = useMemo(
    () => (data ? _.groupBy(data.entries, (e: Entry) => e.outline.steno) : {}),
    [data]
  )

  return loading ? (
    <Loader />
  ) : data ? (
    <>
      <TranslationInfo translation={data.search.translation!} />
      <div>
        <span className="font-semibold">{data.entries.length}</span> entr
        {data.entries.length === 1 ? "y" : "ies"},{" "}
        <span className="font-semibold">
          {Object.keys(entriesBySteno).length}
        </span>{" "}
        outline{Object.keys(entriesBySteno).length === 1 ? "" : "s"}
      </div>
      <div className="my-6">
        {_.sortBy(
          Object.keys(entriesBySteno),
          (steno) => -entriesBySteno[steno].length
        ).map((steno) => {
          const outlines = entriesBySteno[steno]
          return (
            <div className="grid grid-cols-4 py-4" key={steno}>
              <div className="font-mono text-xl">{steno}</div>
              <div className="col-span-3">
                {outlines.map((entry) => (
                  <div className="mb-2" key={entry.uid}>
                    <DictLink dict={entry.dictionary!} className="text-right" />
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
    </>
  ) : (
    <Error err={error} />
  )
}
