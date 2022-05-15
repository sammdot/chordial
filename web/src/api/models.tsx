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
}

export interface Outline extends Item {
  steno: string
}

export interface Translation extends Item {
  translation: string
}

export interface Entry extends Item, CreatedTime {
  outline: Outline
  translation: Translation
}

export interface EntryResults {
  count: number
  offset: number
  entries: Entry[]
}
