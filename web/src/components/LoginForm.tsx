import { Formik } from "formik"
import { Dispatch, useContext } from "react"

import { useNavigate } from "react-router"

import { ApiContext } from "src/api"
import { ChordialApiError } from "src/api/ChordialApi"
import Loader from "src/components/Loader"

type LoginParams = {
  username?: string
  password?: string
}

type Props = {
  setAuthToken: Dispatch<string | undefined>
}

export default function LoginForm({ setAuthToken }: Props) {
  const api = useContext(ApiContext)
  const navigateTo = useNavigate()

  return (
    <Formik
      initialValues={{ username: "", password: "" } as LoginParams}
      validate={(values) => {
        const errors: LoginParams = {}
        if (!values.username) {
          errors.username = "Username required"
        }
        if (!values.password) {
          errors.password = "Password required"
        }
        return errors
      }}
      onSubmit={(values, { setFieldError, setSubmitting }) => {
        api
          .login(values.username!, values.password!)
          .then((d) => {
            setSubmitting(false)
            setAuthToken(d.access_token)
            navigateTo("/")
          })
          .catch((e: ChordialApiError) => {
            setSubmitting(false)
            setFieldError("password", (e.message as any).message)
          })
      }}
    >
      {({
        values,
        errors,
        touched,
        handleChange,
        handleBlur,
        handleSubmit,
        isSubmitting,
      }) => (
        <>
          <input
            type="text"
            name="username"
            onChange={handleChange}
            onBlur={handleBlur}
            value={values.username}
            placeholder="Username"
            className="block w-full py-3 px-4 rounded-t-md border-x border-t border-gray-400"
          />
          <input
            type="password"
            name="password"
            onChange={handleChange}
            onBlur={handleBlur}
            value={values.password}
            placeholder="Password"
            className="block w-full py-3 px-4 rounded-b-md border border-gray-400 mb-2"
          />
          {(errors.username && touched.username) ||
          (errors.password && touched.password) ? (
            <span className="text-red-400 text-italic">
              {errors.username || errors.password}
            </span>
          ) : (
            <></>
          )}
          <span className="flex flex-row gap-6 mt-6">
            {/* TODO: Implement signup */}
            <button
              disabled
              className="block w-full text-center py-2 px-4 rounded-md font-medium border border-gray-400 bg-gray-100 text-gray-400"
            >
              Sign Up
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              onClick={() => handleSubmit()}
              className={
                "block w-full text-center py-2 px-4 rounded-md font-semibold bg-brand text-white flex flex-row justify-center items-center" +
                (isSubmitting ? "" : " hover:drop-shadow-lg")
              }
            >
              {isSubmitting ? (
                <Loader
                  containerClassName="inline mr-3"
                  className="w-4 h-4 fill-white"
                />
              ) : (
                <></>
              )}
              Log In
            </button>
          </span>
        </>
      )}
    </Formik>
  )
}
