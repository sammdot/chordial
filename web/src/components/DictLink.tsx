import { Dictionary } from "src/api/models"
import Link from "src/components/Link"

type Props = {
  dict: Dictionary
  className?: string
}

export default function DictLink({ dict, className }: Props) {
  return (
    <Link to={`/${dict.user.username}/${dict.name}`} className={className}>
      {dict.user.username}/{dict.name}
    </Link>
  )
}
