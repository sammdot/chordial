import { Dictionary } from "src/api/models"
import {
  ProprietaryBadge,
  TheoryBadge,
  VisibilityBadge,
} from "src/components/Badge"
import { EntryCounter } from "src/components/Counter"
import Link from "src/components/Link"
import Permalink from "src/components/Permalink"
import ShortDate from "src/components/ShortDate"

type Props = {
  dict: Dictionary
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
            <ProprietaryBadge proprietary={dict.proprietary} className="ml-3" />
            <VisibilityBadge visibility={dict.visibility} className="ml-3" />
            <TheoryBadge theory={dict.theory} className="ml-3" />
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
