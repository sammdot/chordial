import { FaCheck } from "react-icons/fa"

import { User } from "src/api/models"
import Permalink from "src/components/Permalink"
import ShortDate from "src/components/ShortDate"

type Props = {
  user: User
  hidePermalink?: boolean
}

export function UserBadge({ user }: Props) {
  return user.is_system || user.is_admin ? (
    <div className="inline-block translate-y-[-0.25rem] px-1.5 pt-0.5 rounded-md uppercase text-sm font-medium bg-brand text-white ml-3 select-none">
      <FaCheck className="inline translate-y-[-1px] mr-1" />
      {user.is_system && "system"}
      {user.is_admin && "admin"}
    </div>
  ) : (
    <></>
  )
}

export default function UserInfo({ user, hidePermalink }: Props) {
  return (
    <div className="flex items-center">
      <div className="flex-grow">
        <div>
          <span className="text-3xl font-medium">{user.username}</span>
          <UserBadge user={user} />
        </div>
        <div className="text-md text-gray-400">
          {user.is_system ? "Created " : "Joined "}
          <ShortDate date={user.created_time} />
        </div>
      </div>
      {hidePermalink ? <></> : <Permalink url={`/u/${user.uid}`} />}
    </div>
  )
}
