import { ReactNode } from "react"

import { ChordialApiError } from "src/api/ChordialApi"

type Props = {
  className?: string
}

export default function Loader({ className }: Props) {
  return (
    <div className="w-full mx-auto center mt-40 md:mt-60">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 100 100"
        fill="none"
        role="status"
        className={
          "inline min-w-full h-12 text-gray-200 animate-spin dark:text-gray-600 fill-brand " +
          className
        }
      >
        <path
          d="M50 0c27.614 0 50 22.386 50 50s-22.386 50-50 50S0 77.614 0 50 22.386 0 50 0Zm0 8C26.804 8 8 26.804 8 50s18.804 42 42 42 42-18.804 42-42S73.196 8 50 8Z"
          fill="currentColor"
        />
        <path
          d="M50 0c13.758 0 26.217 5.556 35.258 14.547a4 4 0 1 1-5.553 5.75l-.006.006C72.1 12.7 61.6 8 50 8c-11.401 0-21.742 4.543-29.31 11.918l-.388.384a4.02 4.02 0 0 1-2.89 1.224 4 4 0 0 1-2.682-6.968l-.085.087C23.693 5.596 36.193 0 50 0Z"
          fill="currentFill"
        />
      </svg>
    </div>
  )
}
