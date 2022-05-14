const formatter = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
})

type Props = {
  date: string
}

export default function ShortDate({ date }: Props) {
  return <>{formatter.format(new Date(date))}</>
}
