import React, { ReactNode } from "react"

type Props = {
  children?: ReactNode
}

export default function Footer({ children }: Props) {
  return (
    <div className="bg-gray-100 dark:bg-gray-600">
      <div className="w-full md:container mx-auto p-6 flex flex-row">
        {children}
        <span className="flex-grow text-right pl-6">
          © 2022 Open Steno Project and contributors
        </span>
      </div>
    </div>
  )
}
