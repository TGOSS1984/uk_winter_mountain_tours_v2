module.exports = {
  env: { browser: true, es2021: true },
  extends: ["eslint:recommended", "plugin:prettier/recommended"],
  parserOptions: { ecmaVersion: "latest", sourceType: "module" },
  rules: {
    // keep strict minimal rules; you can tighten later
    "no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
    "no-console": "off"
  }
};
