import ReactCountryFlag from "react-country-flag"

type Props = {
  variant: string
  className?: string
}

const variantToCountryCode = new Map([
  ["US", "US"],
  ["UK", "GB"],
])

export default function FlagEmoji({ variant, className }: Props) {
  let countryCode = variantToCountryCode.get(variant)
  return countryCode ? (
    <ReactCountryFlag countryCode={countryCode} className={className} />
  ) : (
    <></>
  )
}
