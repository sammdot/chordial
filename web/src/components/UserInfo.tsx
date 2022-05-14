import { User } from "src/api/models"
import ShortDate from "src/components/ShortDate"

type Props = { user: User }

export function UserBadge({ user }: Props) {
  return user.is_system || user.is_admin ? (
    <div className="inline-block translate-y-[-0.25rem] before:content-['✓_'] px-1.5 pt-0.5 rounded-md uppercase text-sm font-medium bg-brand text-white ml-3 select-none">
      {user.is_system && "system"}
      {user.is_admin && "admin"}
    </div>
  ) : (
    <></>
  )
}

export default function UserInfo({ user }: Props) {
  return (
    <>
      <div>
        <span className="text-3xl font-medium">{user.username}</span>
        <UserBadge user={user} />
      </div>
      <div className="text-md text-gray-400">
        {user.is_system ? "Created " : "Joined "}
        <ShortDate date={user.created_time} />
      </div>
    </>
  )
}
