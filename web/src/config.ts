const config = {
  appName: "Chordial",
  baseUrl:
    process.env.NODE_ENV === "production" ? "/api" : "http://localhost:3241",
}

export default config
