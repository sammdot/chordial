import { Link } from "react-router-dom"

import { Entry, Related } from "src/api/models"
import { EntryStatusBadge } from "src/components/Badge"
import { OutlineCounter } from "src/components/Counter"
import ColoredLink from "src/components/Link"

type Props = {
  translation: string
  outlines: Related[]
  layout: string
  className?: string
}

type ItemProps = {
  layout: string
  steno: string
  translation: string
  entries: Entry[]
}

export function OutlineListItem({
  layout,
  steno,
  translation,
  entries,
}: ItemProps) {
  return (
    <Link
      to={`/entries/${layout}/${encodeURIComponent(
        steno!
      )}/${encodeURIComponent(translation)}`}
    >
      <div
        className="grid grid-cols-4 py-1 text-lg px-2 mx-[-0.5rem] hover:bg-gray-200 hover:rounded-md"
        key={steno}
      >
        <div className="font-mono text-xl my-1">{steno}</div>
        <div className="col-span-3">
          {entries.map((entry) => (
            <div className="inline my-1" key={entry.uid}>
              {entry.dictionary?.theory ? (
                <EntryStatusBadge
                  theory={entry.dictionary!.theory}
                  status={entry.status}
                  className="inline-block mr-2"
                />
              ) : (
                <></>
              )}
            </div>
          ))}
        </div>
      </div>
    </Link>
  )
}

export default function OutlineList({
  translation,
  outlines,
  layout,
  className,
}: Props) {
  return (
    <div className={className}>
      <div className="mb-2">
        <OutlineCounter number={outlines.length} className="font-semibold" />{" "}
        for '
        <ColoredLink
          to={`/translations/${layout}/${encodeURIComponent(translation)}`}
        >
          {translation}
        </ColoredLink>
        '
      </div>
      {outlines.map(({ outline: steno, entries }) => (
        <OutlineListItem
          layout={layout}
          steno={steno!}
          translation={translation}
          entries={entries}
          key={steno!}
        />
      ))}
    </div>
  )
}
