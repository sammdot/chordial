import { Outline } from "src/api/models"
import Permalink from "src/components/Permalink"

type Props = {
  outline: Outline
}

export default function OutlineInfo({ outline }: Props) {
  return (
    <div className="flex items-center">
      <div className="flex-grow">
        <span className="text-3xl font-mono">{outline.steno}</span>
      </div>
      <Permalink url={`/ol/${outline.uid}`} />
    </div>
  )
}
