import { ReactNode } from "react"
import { Link } from "react-router-dom"

import { Dictionary, User } from "src/api/models"
import ShortDate from "src/components/ShortDate"

type ItemProps = {
  user: User
  dict: Dictionary
}

type ListProps = {
  children?: ReactNode
}

function DictListItem({ user, dict }: ItemProps) {
  let numEntries = dict.num_entries.toLocaleString("en-US")
  return (
    <Link to={`/${user.username}/${dict.name}`}>
      <li className="border border-gray-300 rounded-lg py-4 px-5 hover:shadow-md">
        <div className="text-xl font-medium text-blue-500">{dict.name}</div>
        <div className="text-md text-gray-700">
          <span className="font-semibold">{numEntries}</span> entries
        </div>
        <div className="text-md text-gray-400">
          Last updated <ShortDate date={dict.updated_time} />
        </div>
      </li>
    </Link>
  )
}

export default function DictList({ children }: ListProps) {
  return (
    <ul className="grid gap-6 grid-flow-row grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      {children}
    </ul>
  )
}

DictList.Item = DictListItem
