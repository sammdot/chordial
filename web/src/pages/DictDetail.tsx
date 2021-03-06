import React, { useCallback, useMemo, useState } from "react"
import { FaChevronLeft, FaChevronRight } from "react-icons/fa"
import ReactPaginate from "react-paginate"
import { useParams } from "react-router"
import { Link } from "react-router-dom"
import { Column, useTable, usePagination } from "react-table"

import { Dictionary, Entry, EntryResults } from "src/api/models"
import DictInfo from "src/components/DictInfo"
import EntryList from "src/components/EntryList"
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
  // TODO: Implement sorting
  // const [sortBy, setSortBy] = useState<"steno" | "translation">("steno")
  const sortBy = "steno"
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
        id: "outline",
        accessor: (row: Entry) => row.outline.steno,
        Header: "Outline",
        Cell: ({ value }: { value: any }) => (
          <>
            <div className="font-mono">{value}</div>
          </>
        ),
      },
      {
        id: "translation",
        accessor: (row: Entry) => row.translation.translation,
        Header: "Translation",
      },
    ],
    []
  )
  const { headerGroups, prepareRow, page, pageCount, gotoPage } = useTable(
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

  const layoutName: string | undefined = useMemo(
    () => (data ? data.layout!.short_name : undefined),
    [data]
  )

  return loading ? (
    <Loader />
  ) : data ? (
    <>
      <DictInfo dict={data} />
      <ReactPaginate
        breakLabel="?????????"
        previousLabel={<FaChevronLeft />}
        nextLabel={<FaChevronRight />}
        onPageChange={({ selected: page }) => goto(page)}
        disableInitialCallback={true}
        pageRangeDisplayed={5}
        pageCount={pageCount}
        className="mt-6 text-center font-medium"
        previousClassName="py-2 px-2 translate-y-3 inline-block select-none hover:bg-gray-200 border-gray-400 border-y border-l rounded-l-md"
        pageClassName="py-1 inline-block select-none hover:bg-gray-200 border-gray-400 border-y"
        breakClassName="py-1 inline-block select-none hover:bg-gray-200 border-gray-400 border-y"
        nextClassName="py-2 px-2 translate-y-3 inline-block select-none hover:bg-gray-200 border-gray-400 border-y border-r rounded-r-md"
        activeClassName="bg-brand text-white hover:bg-brand"
        pageLinkClassName="px-3 py-2.5 leading-6"
        breakLinkClassName="px-3 py-2.5 leading-6"
        disabledClassName="text-gray-400 hover:bg-white"
        renderOnZeroPageCount={() => null}
      />
      {entriesLoading ? (
        <Loader />
      ) : entriesData ? (
        entriesData.entries.length ? (
          <EntryList className="mt-6">
            <EntryList.Header
              className="hidden sm:grid sm:grid-cols-2 my-2"
              cellClassName="font-semibold text-left text-sm uppercase text-gray-500"
              headers={headerGroups}
            />
            {page.map((row) => {
              prepareRow(row)
              return (
                <Link
                  to={`/entries/${layoutName}/${encodeURIComponent(
                    row.original.outline.steno
                  )}/${encodeURIComponent(
                    row.original.translation.translation
                  )}`}
                >
                  <EntryList.Row
                    key={row.original.outline.steno}
                    className="sm:grid sm:grid-cols-2 py-1 text-lg px-2 mx-[-0.5rem] hover:bg-gray-200 hover:rounded-md"
                    row={row}
                  />
                </Link>
              )
            })}
          </EntryList>
        ) : (
          <div className="mt-12 text-italic text-gray-500">
            No entries to display.
          </div>
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
