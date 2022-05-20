import { Link } from "react-router-dom"

import { Entry, Related, Translation } from "src/api/models"
import { EntryStatusBadge } from "src/components/Badge"
import { TranslationCounter } from "src/components/Counter"
import FlagEmoji from "src/components/FlagEmoji"
import ColoredLink from "src/components/Link"

type Props = {
  steno: string
  translations: Related[]
  layout: string
  className?: string
}

type ItemProps = {
  layout: string
  steno: string
  translation: Translation
  entries: Entry[]
}

export function TranslationListItem({
  layout,
  steno,
  translation,
  entries,
}: ItemProps) {
  return (
    <Link
      to={`/entries/${layout}/${encodeURIComponent(steno)}/${encodeURIComponent(
        translation.translation
      )}`}
    >
      <div className="grid grid-cols-4 py-1 text-lg px-2 mx-[-0.5rem] hover:bg-gray-200 hover:rounded-md">
        <div className="text-xl my-1">
          {translation.translation}
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
            <div className="inline my-1 " key={entry.uid}>
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

export default function TranslationList({
  steno,
  translations,
  layout,
  className,
}: Props) {
  return (
    <div className={className}>
      <div className="mb-2">
        <TranslationCounter
          number={translations.length}
          className="font-semibold"
        />{" "}
        for{" "}
        <ColoredLink
          to={`/outlines/${layout}/${encodeURIComponent(steno)}`}
          className="font-mono"
        >
          {steno}
        </ColoredLink>
      </div>
      {translations.map(({ translation: tl, entries }) => (
        <TranslationListItem
          layout={layout}
          steno={steno}
          translation={entries[0].translation}
          entries={entries}
          key={tl!}
        />
      ))}
    </div>
  )
}
