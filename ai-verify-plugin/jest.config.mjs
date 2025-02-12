// jest.config.mjs
import nextJest from 'next/jest.js'
import { rootDir } from './src/utils.mjs';

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
  dir: rootDir,
})

// Add any custom config to be passed to Jest
/** @type {import('jest').Config} */
const customConfig = {
  // Add more setup options before each test is run
  setupFilesAfterEnv: ['<rootDir>/jest.setup.mjs'],
  testEnvironment: 'jest-environment-jsdom',
  snapshotResolver: "<rootDir>/snapshotResolver.cjs",
  moduleNameMapper: {
    "src/(.*)": "<rootDir>/src/$1",
    "playground/(.*)": "<rootDir>/playground/$1",
    // "aiverify-shared-library/(.*)": "<rootDir>/node_modules/aiverify-shared-library/$1",
    "aiverify-shared-library/(.*)": "<rootDir>/node_modules/aiverify-shared-library/packages/$1/src",
  },
  // moduleFileExtensions: ["mjs", "js", "jsx", "ts", "tsx"],
  testMatch: [
    "**/__tests__/**/*.[jt]s?(x)",
    "**/__tests__/**/*.mjs"
  ],
  collectCoverageFrom: [
    // "pages/**/*.{ts,tsx}"
  ],
  globals: {
		Uint8Array: Uint8Array,
	},
}

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
// export default createJestConfig(config);
export default async() => ({
  ...(await createJestConfig(customConfig)()),
  "transformIgnorePatterns": [
    "^.+\\.module\\.(css|sass|scss)$",
    "/node_modules/(?!mdx-bundler|uuid|@mdx-js)"
  ],
})
