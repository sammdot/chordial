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
}
