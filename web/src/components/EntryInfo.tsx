import { Layout, Outline, Translation } from "src/api/models"
import FlagEmoji from "src/components/FlagEmoji"
import Permalink from "src/components/Permalink"

type Props = {
  outline: Outline
  translation: Translation
  layout: Layout
}

export default function EntryInfo({ layout, outline, translation }: Props) {
  return (
    <div className="flex items-center">
      <div className="flex-grow">
        <div className="text-3xl font-mono">{outline.steno}</div>
        <div className="text-2xl">
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
      </div>
      <Permalink url={`/e/${outline.uid}/${translation.uid}`} />
    </div>
  )
}
