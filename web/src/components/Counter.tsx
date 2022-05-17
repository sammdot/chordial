type Props = {
  number: number
  singular?: string
  plural?: string
  className: string
}

export default function Counter({
  number,
  singular,
  plural,
  className,
}: Props) {
  let numberString = number.toLocaleString("en-US")
  return (
    <>
      {className ? (
        <span className={className}>{numberString}</span>
      ) : (
        <>{numberString}</>
      )}{" "}
      {number === 1 ? singular : plural}
    </>
  )
}

export function EntryCounter({ number, className }: Props) {
  return (
    <Counter
      number={number}
      singular="entry"
      plural="entries"
      className={className}
    />
  )
}

export function OutlineCounter({ number, className }: Props) {
  return (
    <Counter
      number={number}
      singular="outline"
      plural="outlines"
      className={className}
    />
  )
}

export function TranslationCounter({ number, className }: Props) {
  return (
    <Counter
      number={number}
      singular="translation"
      plural="translations"
      className={className}
    />
  )
}
