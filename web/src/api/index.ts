import React from "react"
import { ChordialApi as Api } from "src/api/ChordialApi"

export const ApiContext = React.createContext(Api)
export const ChordialApi = Api
