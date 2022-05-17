import { FaCheck } from "react-icons/fa"

import { Dictionary } from "src/api/models"
import { EntryCounter } from "src/components/Counter"
import Link from "src/components/Link"
import Permalink from "src/components/Permalink"
import ShortDate from "src/components/ShortDate"

type Props = {
  dict: Dictionary
}

export function DictBadge({ dict }: Props) {
  return dict.theory ? (
    <div className="inline-block translate-y-[-0.25rem] px-1.5 pt-0.5 rounded-md text-sm font-medium bg-brand text-white ml-3 select-none">
      <FaCheck className="inline translate-y-[-1px] mr-1" />
      {dict.theory.display_name}
    </div>
  ) : (
    <></>
  )
}

export default function DictInfo({ dict }: Props) {
  return (
    <div className="flex items-center">
      <div className="flex-grow">
        <div>
          <span className="text-3xl">
            <Link to={`/${dict.user.username}`}>{dict.user.username}</Link>
            <span className="mx-2">/</span>
            <span className="font-medium">{dict.name}</span>
            <DictBadge dict={dict} />
          </span>
        </div>
        <div className="text-md text-gray-700">
          <EntryCounter number={dict.num_entries} className="font-semibold" />
        </div>
        <div className="text-md text-gray-400">
          Created <ShortDate date={dict.created_time} />
        </div>
      </div>
      <Permalink url={`/d/${dict.uid}`} />
    </div>
  )
}
