import { Translation } from "src/api/models"
import FlagEmoji from "src/components/FlagEmoji"
import Permalink from "src/components/Permalink"

type Props = {
  translation: Translation
}

export default function TranslationInfo({ translation }: Props) {
  return (
    <div className="flex items-center">
      <div className="flex-grow">
        <span className="text-3xl">
          {translation.translation}
          {translation.spelling_variant ? (
            <FlagEmoji
              variant={translation.spelling_variant}
              className="ml-2"
            />
          ) : (
            <></>
          )}
        </span>
      </div>
      <Permalink url={`/tl/${translation.uid}`} />
    </div>
  )
}
