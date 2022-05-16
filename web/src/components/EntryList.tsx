import { ReactNode } from "react"
import { HeaderGroup, Row } from "react-table"

import { Entry } from "src/api/models"
import Link from "src/components/Link"

type HeaderProps = {
  className?: string
  cellClassName?: string
  headers: HeaderGroup<Entry>[]
}

type RowProps = {
  className?: string
  children?: ReactNode
  row: Row<Entry>
}

type Props = {
  className?: string
  children?: ReactNode
}

function Header({ className, cellClassName, headers }: HeaderProps) {
  return (
    <div>
      {headers.map((headerGroup, i) => (
        <div className={className} key={`group-${i}`}>
          {headerGroup.headers.map((column, i) => (
            <div className={cellClassName} key={`column-${i}`}>
              {column.render("Header")}
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

function EntryItem({ className, row }: RowProps) {
  return (
    <div className={className}>
      {row.cells.map((cell, i) => {
        return <div key={`cell-${i}`}>{cell.render("Cell")}</div>
      })}
    </div>
  )
}

export default function EntryList({ className, children }: Props) {
  return (
    <div role="table" className={" " + className}>
      {children}
    </div>
  )
}

EntryList.Header = Header
EntryList.Row = EntryItem
