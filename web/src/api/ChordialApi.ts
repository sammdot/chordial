import config from "src/config"

export class ChordialApi {
  private static async _get(url: string): Promise<any> {
    return ChordialApi._fetch("get", url)
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
    throw new Error(await response.json())
  }
}
