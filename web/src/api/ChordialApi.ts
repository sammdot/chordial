import { Dictionary, EntryResults, User } from "src/api/models"

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
  static async get(url: string): Promise<any> {
    return ChordialApi._get(url)
  }

  static async userByName(name: string): Promise<User> {
    return ChordialApi._get("/users", { name })
  }

  static async dictByName(username: string, name: string): Promise<Dictionary> {
    return ChordialApi._get("/dicts", { username, name })
  }

  static async entries(
    dict: string,
    options: EntryOptions
  ): Promise<EntryResults> {
    return ChordialApi._get(`/dicts/${dict}/entries`, options)
  }

  private static async _get(url: string, params?: any): Promise<any> {
    return ChordialApi._fetch(
      "get",
      url + (params ? "?" + new URLSearchParams(params) : "")
    )
  }

  private static async _post(url: string, body?: any): Promise<any> {
    return ChordialApi._fetch("get", url, body)
  }

  private static async _fetch(
    method: string,
    url: string,
    body?: any
  ): Promise<any> {
    const response = await fetch(`${config.baseUrl}${url}`, {
      method,
      body: !!body ? JSON.stringify(body) : null,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
    if (response.ok) {
      return await response.json()
    }
    throw new ChordialApiError(await response.json(), response.status)
  }
}
