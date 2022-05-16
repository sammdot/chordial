export interface Item {
  uid: string
}

export interface CreatedTime {
  created_time: string
}

export interface UpdatedTime {
  updated_time: string
}

export interface Layout extends Item {
  short_name: string
  display_name: string
}

export interface Theory extends Item {
  short_name: string
  display_name: string
}

export interface User extends Item, CreatedTime {
  username: string
  is_admin: boolean
  is_system: boolean
  dictionaries?: Dictionary[]
}

export interface Dictionary extends Item, CreatedTime, UpdatedTime {
  name: string
  user: User
  visibility: "public" | "unlisted" | "private"
  proprietary: boolean
  theory?: Theory
  num_entries: number
  layout?: Layout
}

export interface Outline extends Item {
  steno: string
  layout?: Layout
}

export interface Translation extends Item {
  translation: string
  spelling_variant?: string | null
  layout?: Layout
}

export interface Entry extends Item, CreatedTime {
  outline: Outline
  translation: Translation
  dictionary?: Dictionary
}

export interface EntryResults {
  count: number
  offset: number
  entries: Entry[]
}

export interface SearchQuery {
  outline?: Outline
  translation?: Translation
}

export interface SearchResults {
  layout: Layout
  search: SearchQuery
  entries: Entry[]
}

export interface OutlineResults {
  layout: Layout
  outline: Outline
  entries: Entry[]
}

export interface TranslationResults {
  layout: Layout
  translation: Translation
  entries: Entry[]
}

export interface EntryRelated {
  outline: Entry[]
  translation: Entry[]
}

export interface EntryDetails {
  entry: Entry
  related: EntryRelated
}
