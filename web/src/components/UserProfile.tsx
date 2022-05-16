import { Dispatch, useCallback } from "react"
import { FaChevronDown } from "react-icons/fa"
import * as Dialog from "@radix-ui/react-dialog"
import * as Popover from "@radix-ui/react-popover"

import { User } from "src/api/models"
import LoginForm from "src/components/LoginForm"
import Logo from "src/components/Logo"
import UserPopover from "src/components/UserPopover"
import { useApiQuery } from "src/utils/hooks"

type Props = {
  authToken: string | undefined
  setAuthToken: Dispatch<string | undefined>
}

export default function UserProfile({ authToken, setAuthToken }: Props) {
  const { data: user } = useApiQuery<User | undefined>(
    useCallback(
      (api) =>
        api.auth().catch((e) => {
          setAuthToken(undefined)
          return undefined
        }),
      [setAuthToken]
    )
  )

  return user ? (
    <>
      <Popover.Root>
        <Popover.Trigger>
          {" "}
          <div className="rounded-md border border-gray-400 py-2 px-3 flex flex-row items-center hover:bg-gray-100">
            <div className="font-semibold">{user.username}</div>
            <FaChevronDown className="ml-2" />
          </div>
        </Popover.Trigger>
        <Popover.Content>
          <UserPopover user={user} setAuthToken={setAuthToken} />
        </Popover.Content>
      </Popover.Root>
    </>
  ) : (
    <>
      <Dialog.Root>
        <Dialog.Trigger className="bg-brand text-white font-semibold px-3 py-1.5 rounded-md">
          Log In
        </Dialog.Trigger>
        <Dialog.Portal>
          <Dialog.Overlay className="w-screen h-screen fixed top-0 left-0 z-50 flex justify-center items-center">
            <div className="w-screen h-screen bg-gray-200 opacity-40 fixed top-0 left-0" />
            <Dialog.Content className="mx-12 w-96 bg-white mx-auto drop-shadow-xl rounded-xl flex flex-col p-8 opacity-100">
              <Dialog.Title className="w-full text-center">
                <Logo className="inline-block" />
              </Dialog.Title>
              <Dialog.Description className="mt-4">
                <LoginForm setAuthToken={setAuthToken} />
              </Dialog.Description>
            </Dialog.Content>
          </Dialog.Overlay>
        </Dialog.Portal>
      </Dialog.Root>
    </>
  )
}
