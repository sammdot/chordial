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

export type Visibility = "public" | "unlisted" | "private"

export interface Dictionary extends Item, CreatedTime, UpdatedTime {
  name: string
  user: User
  visibility: Visibility
  proprietary: boolean
  theory?: Theory
  num_entries: number
  layout?: Layout
}

export interface Outline extends Item {
  steno: string
  steno_without_number: string
  layout?: Layout
}

export interface Translation extends Item {
  translation: string
  spelling_variant?: string | null
  layout?: Layout
}

export type EntryStatus =
  | "unknown"
  | "mandatory"
  | "recommended"
  | "preferred"
  | "correct"
  | "misstroke"

export type Derivation =
  | "unknown"
  | "phonetic"
  | "semi_phonetic"
  | "orthographic"
  | "skeletal"
  | "shape_based"
  | "arbitrary"
  | "phrase"

export interface Entry extends Item, CreatedTime {
  outline: Outline
  translation: Translation
  dictionary?: Dictionary
  status: EntryStatus
  derivation: Derivation
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

export interface Related {
  outline?: string
  translation?: string
  score: number
  entries: Entry[]
}

export interface SearchResults {
  layout: Layout
  search: SearchQuery
  entries?: Entry[]
  entries_ranked?: Related[]
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
  outline: Related[]
  translation: Related[]
}

export interface EntryDetails {
  layout?: Layout
  entry: Entry
  related: EntryRelated
}

export interface AccessToken {
  access_token: string
}
