type Config = {
  baseUrl: string
}

const developmentConfig: Config = {
  baseUrl: "http://localhost:3241",
}

const stagingConfig: Config = {
  ...developmentConfig,
  baseUrl: "https://staging-api.chordial.app",
}

const productionConfig: Config = {
  ...stagingConfig,
  baseUrl: "https://api.chordial.app",
}

const env = process.env.CHORDIAL_ENV || process.env.NODE_ENV
const config =
  env === "production"
    ? productionConfig
    : env === "staging"
    ? stagingConfig
    : developmentConfig

export default config
