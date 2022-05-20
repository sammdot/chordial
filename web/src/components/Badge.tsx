import {
  FaBan,
  FaCheck,
  FaDollarSign,
  FaEyeSlash,
  FaLock,
  FaStar,
} from "react-icons/fa"

import { EntryStatus, Theory, Visibility } from "src/api/models"

type VisibilityProps = {
  visibility: Visibility
  className?: string
}

type ProprietaryProps = {
  proprietary: boolean
  className?: string
}

type TheoryProps = {
  theory?: Theory
  className?: string
}

type EntryStatusProps = {
  theory?: Theory
  status?: EntryStatus
  className?: string
}

export function VisibilityBadge({ visibility, className }: VisibilityProps) {
  return visibility === "public" ? (
    <></>
  ) : (
    <div
      className={
        "inline-block translate-y-[-0.25rem] px-1.5 pt-0.5 rounded-md text-sm font-medium text-white select-none " +
        (visibility === "unlisted" ? "bg-amber-400" : "bg-gray-400") +
        " " +
        className
      }
    >
      {visibility === "unlisted" ? (
        <>
          <FaEyeSlash className="inline translate-y-[-1px] mr-1" />
          Unlisted
        </>
      ) : (
        <>
          <FaLock className="inline translate-y-[-1px] mr-1" />
          Private
        </>
      )}
    </div>
  )
}

export function ProprietaryBadge({ proprietary, className }: ProprietaryProps) {
  return proprietary ? (
    <div
      className={
        "inline-block translate-y-[-0.25rem] px-1.5 pt-0.5 rounded-md text-sm font-medium bg-sky-400 text-white select-none " +
        className
      }
    >
      <FaDollarSign className="inline translate-y-[-1px] mr-1" />
      Proprietary
    </div>
  ) : (
    <></>
  )
}

export function TheoryBadge({ theory, className }: TheoryProps) {
  return theory ? (
    <div
      className={
        "inline-block translate-y-[-0.25rem] px-1.5 pt-0.5 rounded-md text-sm font-medium text-white bg-brand select-none " +
        className
      }
    >
      <FaCheck className="inline translate-y-[-1px] mr-1" />
      {theory.display_name}
    </div>
  ) : (
    <></>
  )
}

export function EntryStatusBadge({
  theory,
  status,
  className,
}: EntryStatusProps) {
  const [Icon, style] =
    status === "mandatory"
      ? [FaStar, "bg-brand text-white"]
      : status === "recommended" || status === "preferred"
      ? [FaCheck, "bg-sky-400 text-white"]
      : status === "correct"
      ? [undefined, "bg-gray-600 text-white"]
      : status === "unknown"
      ? [undefined, "bg-gray-300"]
      : [FaBan, "bg-red-200"]
  return theory ? (
    <div
      className={
        "inline-block translate-y-0.5 px-1.5 pt-0.5 rounded-md text-sm font-medium select-none " +
        style +
        " " +
        className
      }
    >
      {Icon ? <Icon className="inline translate-y-[-1px] mr-1" /> : <></>}
      {theory.display_name}
    </div>
  ) : (
    <></>
  )
}
