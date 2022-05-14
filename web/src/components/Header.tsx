import React, { ReactNode } from "react"

import Logo from "src/components/Logo"

type Props = {
  children?: ReactNode
}

export default function Header({ children }: Props) {
  return (
    <div className="w-full md:container mx-auto p-6 pt-10 flex flex-row items-center">
      <Logo className="pr-6" />
      {children}
    </div>
  )
}
