import { Link as BaseLink } from "react-router-dom"

export default function Link(props: any) {
  return (
    <BaseLink
      {...props}
      className={
        "text-blue-500 hover:underline underline-offset-2 " + props.className
      }
    />
  )
}
