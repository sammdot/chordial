import { ChordialApiError } from "src/api/ChordialApi"

type Props = {
  err?: ChordialApiError
}

export default function Error({ err }: Props) {
  let errorMessage = err?.message as any
  return (
    <div
      className="mx-auto mt-60 px-6 py-4 bg-red-200 border border-red-600 rounded-md w-80"
      role="alert"
    >
      <p>{errorMessage.message}</p>
    </div>
  )
}
