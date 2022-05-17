import React from "react"
import { Route, Routes } from "react-router-dom"

import { ChordialApiError } from "src/api/ChordialApi"
import Error from "src/components/Error"
import Footer from "src/components/Footer"
import Header from "src/components/Header"
import UserProfile from "src/components/UserProfile"
import DictDetail from "src/pages/DictDetail"
import EntryDetail from "src/pages/EntryDetail"
import OutlineDetail from "src/pages/OutlineDetail"
import PermalinkRedirect from "src/pages/PermalinkRedirect"
import TranslationDetail from "src/pages/TranslationDetail"
import UserDetail from "src/pages/UserDetail"
import { useAuth } from "src/utils/hooks"
import useDocumentTitle from "src/utils/title"

export default function App() {
  const [authToken, setAuthToken] = useAuth()
  useDocumentTitle()
  return (
    <div className="bg-white dark:bg-gray-700 text-black dark:text-white min-h-screen flex flex-col">
      <Header>
        <div className="flex-grow" />
        <UserProfile authToken={authToken} setAuthToken={setAuthToken} />
      </Header>
      <div className="w-full md:container mx-auto px-6 pt-4 pb-10 flex-grow min-h-full">
        <Routes>
          <Route path="/d/:uid" element={<PermalinkRedirect type="dict" />} />
          <Route path="/u/:uid" element={<PermalinkRedirect type="user" />} />
          <Route
            path="/tl/:uid"
            element={<PermalinkRedirect type="translation" />}
          />
          <Route
            path="/ol/:uid"
            element={<PermalinkRedirect type="outline" />}
          />
          <Route
            path="/entries/:layout/:steno/:translation"
            element={<EntryDetail />}
          />
          <Route
            path="/translations/:layout/:translation"
            element={<TranslationDetail />}
          />
          <Route path="/outlines/:layout/:steno" element={<OutlineDetail />} />
          <Route path="/:user/:dict" element={<DictDetail />} />
          <Route path="/:user" element={<UserDetail />} />
          <Route path="/" element={<></>} />
          <Route
            path="*"
            element={<Error err={new ChordialApiError("Not found", 404)} />}
          />
        </Routes>
      </div>
      <Footer />
    </div>
  )
}
