import { Dispatch, useContext } from "react"
import { useNavigate } from "react-router"

import { ApiContext } from "src/api"
import { User } from "src/api/models"
import UserInfo from "src/components/UserInfo"

type Props = {
  user: User
  setAuthToken: Dispatch<string | undefined>
}

export default function UserPopover({ user, setAuthToken }: Props) {
  const api = useContext(ApiContext)
  const navigateTo = useNavigate()

  return (
    <div className="w-96 mt-4 rounded-md bg-white border border-gray-400 drop-shadow-md px-4 py-3">
      <UserInfo user={user} hidePermalink={true} />
      {/* TODO: implement user settings and other actions */}
      <div className="mt-4 mb-2">
        <button
          className="block w-full text-center py-2 px-4 rounded-md font-medium border border-gray-400"
          onClick={() => {
            api
              .logout()
              .catch((e) => {
                console.log(JSON.stringify(e))
              })
              .then(() => {
                setAuthToken(undefined)
                navigateTo("/")
              })
          }}
        >
          Log Out
        </button>
      </div>
    </div>
  )
}
