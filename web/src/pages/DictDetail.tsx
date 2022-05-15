import React, { useCallback, useMemo, useState } from "react"
import ReactPaginate from "react-paginate"
import { useParams } from "react-router"
import { Column, useTable, usePagination } from "react-table"

import { Dictionary, Entry, EntryResults } from "src/api/models"
import DictInfo from "src/components/DictInfo"
import Error from "src/components/Error"
import Loader from "src/components/Loader"
import { useApiQuery } from "src/utils/hooks"

type Params = {
  user: string
  dict: string
}

export default function DictDetail() {
  const { user, dict } = useParams<Params>()

  const { loading, data, error } = useApiQuery<Dictionary>(
    useCallback((api) => api.dictByName(user!, dict!), [user, dict]),
    useCallback((d: Dictionary) => `${d.user.username}/${d.name}`, [])
  )

  const entryCount = 100
  const [pageId, setPageId] = useState(0)
  const [sortBy, setSortBy] = useState<"steno" | "translation">("steno")
  const {
    loading: entriesLoading,
    data: entriesData,
    error: entriesError,
  } = useApiQuery<EntryResults | undefined>(
    useCallback(
      (api) =>
        data?.uid
          ? api.entries(data?.uid, {
              count: entryCount,
              offset: pageId * entryCount,
              sort: sortBy,
            })
          : Promise.resolve(undefined),
      [data, pageId, sortBy]
    )
  )

  const columns: Column<Entry>[] = useMemo(
    () => [
      {
        accessor: (row: Entry) => row.outline.steno,
        Header: "Outline",
        Cell: ({ value }: { value: any }) => (
          <>
            <div className="font-mono">{value}</div>
          </>
        ),
      },
      {
        accessor: (row: Entry) => row.translation.translation,
        Header: "Translation",
      },
    ],
    []
  )
  const { getTableProps, headerGroups, prepareRow, page, pageCount, gotoPage } =
    useTable(
      {
        columns,
        data: entriesData?.entries || [],
        initialState: {
          pageIndex: pageId,
          pageSize: entryCount,
        },
        pageCount: data ? Math.ceil(data.num_entries / entryCount) : -1,
        manualPagination: true,
      },
      usePagination
    )

  const goto = (page: number) => {
    setPageId(page)
    gotoPage(page)
  }

  return loading ? (
    <Loader />
  ) : data ? (
    <>
      <DictInfo dict={data} />
      {entriesLoading ? (
        <Loader />
      ) : entriesData ? (
        entriesData.entries ? (
          <>
            <ReactPaginate
              breakLabel="•••"
              previousLabel="←"
              nextLabel="→"
              onPageChange={({ selected: page }) => goto(page)}
              disableInitialCallback={true}
              pageRangeDisplayed={5}
              pageCount={pageCount}
              className="mt-6 text-center font-medium"
              previousClassName="py-1 inline-block select-none hover:bg-gray-200 border-gray-400 border-y border-l rounded-l-md"
              pageClassName="py-1 inline-block select-none hover:bg-gray-200 border-gray-400 border-y"
              breakClassName="py-1 inline-block select-none hover:bg-gray-200 border-gray-400 border-y"
              nextClassName="py-1 inline-block select-none hover:bg-gray-200 border-gray-400 border-y border-r rounded-r-md"
              activeClassName="bg-brand text-white hover:bg-brand"
              previousLinkClassName="px-3 py-2.5 leading-6"
              pageLinkClassName="px-3 py-2.5 leading-6"
              breakLinkClassName="px-3 py-2.5 leading-6"
              nextLinkClassName="px-3 py-2.5 leading-6"
              disabledClassName="text-gray-400 hover:bg-white"
            />
            <div {...getTableProps()} role="table" className="mt-4">
              <div className="hidden sm:grid">
                {headerGroups.map((headerGroup, i) => (
                  <div className="grid grid-cols-2 my-2" key={`group-${i}`}>
                    {headerGroup.headers.map((column, i) => (
                      <div
                        className="font-semibold text-left text-sm uppercase text-gray-500"
                        key={`column-${i}`}
                      >
                        {column.render("Header")}
                      </div>
                    ))}
                  </div>
                ))}
              </div>
              <div>
                {page.map((row) => {
                  prepareRow(row)
                  return (
                    <div
                      {...row.getRowProps()}
                      className="sm:grid sm:grid-cols-2 py-1 text-lg px-2 mx-[-0.5rem] hover:bg-gray-200 hover:rounded-md"
                      key={row.original.outline.steno}
                    >
                      {row.cells.map((cell, i) => {
                        return (
                          <div {...cell.getCellProps()} key={`cell-${i}`}>
                            {cell.render("Cell")}
                          </div>
                        )
                      })}
                    </div>
                  )
                })}
              </div>
            </div>
          </>
        ) : (
          <></>
        )
      ) : entriesError ? (
        <Error err={entriesError} />
      ) : (
        <></>
      )}
    </>
  ) : (
    <Error err={error} />
  )
}
