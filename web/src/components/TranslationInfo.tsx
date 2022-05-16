import { Translation } from "src/api/models"
import Permalink from "src/components/Permalink"

type Props = {
  translation: Translation
}

export default function TranslationInfo({ translation }: Props) {
  return (
    <div className="flex items-center">
      <div className="flex-grow">
        <span className="text-3xl">{translation.translation}</span>
      </div>
      <Permalink url={`/tl/${translation.uid}`} />
    </div>
  )
}
