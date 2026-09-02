module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: ['eslint:recommended'],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  rules: {
    // JSX component references are not recognised by ESLint without the React plugin.
    'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z]' }],
  },
};
