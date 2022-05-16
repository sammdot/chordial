import {
  AccessToken,
  Dictionary,
  EntryDetails,
  EntryResults,
  SearchResults,
  User,
} from "src/api/models"

import config from "src/config"

export class ChordialApiError extends Error {
  constructor(public message: string, public status: number) {
    super(message)
  }
}

type EntryOptions = {
  count: number
  offset: number
  sort: "steno" | "translation"
}

export class ChordialApi {
  static authToken?: string

  static async get(url: string): Promise<any> {
    return ChordialApi._get(url)
  }

  static async auth(): Promise<User> {
    return ChordialApi._get("/auth")
  }

  static async login(username: string, password: string): Promise<AccessToken> {
    return ChordialApi._post("/auth", { username, password })
  }

  static async logout(): Promise<any> {
    return ChordialApi._delete("/auth")
  }

  static async userByName(name: string): Promise<User> {
    return ChordialApi._get("/users", { name })
  }

  static async dictByName(username: string, name: string): Promise<Dictionary> {
    return ChordialApi._get("/dicts", { username, name })
  }

  static async searchBySteno(
    layout: string,
    steno: string
  ): Promise<SearchResults> {
    return ChordialApi._get("/entries", { layout, steno })
  }

  static async searchByTranslation(
    layout: string,
    translation: string
  ): Promise<SearchResults> {
    return ChordialApi._get("/entries", { layout, translation })
  }

  static async searchByStenoAndTranslation(
    layout: string,
    steno: string,
    translation: string
  ): Promise<SearchResults> {
    return ChordialApi._get("/entries", { layout, steno, translation })
  }

  static async entries(
    dict: string,
    options: EntryOptions
  ): Promise<EntryResults> {
    return ChordialApi._get(`/dicts/${dict}/entries`, options)
  }

  static async entryById(uid: string): Promise<EntryDetails> {
    return ChordialApi._get(`/entries/${uid}`)
  }

  private static async _get(url: string, params?: any): Promise<any> {
    return ChordialApi._fetch(
      "get",
      url + (params ? "?" + new URLSearchParams(params) : "")
    )
  }

  private static async _post(url: string, body?: any): Promise<any> {
    return ChordialApi._fetch("post", url, body)
  }

  private static async _delete(url: string, body?: any): Promise<any> {
    return ChordialApi._fetch("delete", url, body)
  }

  private static async _fetch(
    method: string,
    url: string,
    body?: any
  ): Promise<any> {
    const headers: any = {
      Accept: "application/json",
      "Content-Type": "application/json",
    }
    if (ChordialApi.authToken) {
      headers.Authorization = `Bearer ${ChordialApi.authToken}`
    }
    const response = await fetch(`${config.baseUrl}${url}`, {
      method,
      body: !!body ? JSON.stringify(body) : null,
      headers: headers,
    })
    if (response.ok) {
      return await response.json()
    }
    throw new ChordialApiError(await response.json(), response.status)
  }
}
