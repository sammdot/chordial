import * as _ from "lodash"
import { useCallback, useMemo } from "react"
import { useParams } from "react-router"

import { Entry, SearchResults } from "src/api/models"
import DictLink from "src/components/DictLink"
import Error from "src/components/Error"
import Loader from "src/components/Loader"
import OutlineInfo from "src/components/OutlineInfo"
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
    )
  )

  const entriesByTranslation = useMemo(
    () =>
      data
        ? _.groupBy(data.entries, (e: Entry) => e.translation.translation)
        : {},
    [data]
  )

  return loading ? (
    <Loader />
  ) : data ? (
    <>
      <OutlineInfo outline={data.search.outline!} />
      <div>
        <span className="font-semibold">{data.entries.length}</span> entr
        {data.entries.length === 1 ? "y" : "ies"},{" "}
        <span className="font-semibold">
          {Object.keys(entriesByTranslation).length}
        </span>{" "}
        translation{Object.keys(entriesByTranslation).length === 1 ? "" : "s"}
      </div>
      <div className="my-6">
        {_.sortBy(
          Object.keys(entriesByTranslation),
          (tl) => -entriesByTranslation[tl].length
        ).map((tl) => {
          const entries = entriesByTranslation[tl]
          return (
            <div className="grid grid-cols-4 py-4" key={tl}>
              <div className="text-xl">{tl}</div>
              <div className="col-span-3">
                {entries.map((entry) => (
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
