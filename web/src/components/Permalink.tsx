import { FaLink } from "react-icons/fa"

import Link from "src/components/Link"

type Props = {
  url: string
}

export default function Permalink({ url }: Props) {
  return (
    <span className="font-mono">
      <Link to={url}>
        <FaLink className="inline translate-y-[-2px] mr-2" />
        {url}
      </Link>
    </span>
  )
}
