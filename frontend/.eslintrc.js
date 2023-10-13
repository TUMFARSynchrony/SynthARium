module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es2021: true,
    jest: true
  },
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaFeatures: {
      jsx: true
    },
    ecmaVersion: 2021,
    sourceType: "module"
  },
  plugins: ["react", "react-hooks", "@typescript-eslint", "prettier"],
  extends: [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "plugin:storybook/recommended",
    "airbnb",
    "plugin:prettier/recommended"
  ],
  overrides: [
    {
      files: ["*.ts", "*.tsx"], // Your TypeScript files extension

      // As mentioned in the comments, you should extend TypeScript plugins here,
      // instead of extending them outside the `overrides`.
      // If you don't want to extend any rules, you don't need an `extends` attribute.
      extends: [
        "eslint:recommended",
        "plugin:react/recommended",
        "plugin:react-hooks/recommended",
        "plugin:@typescript-eslint/recommended",
        "airbnb-typescript",
        "plugin:prettier/recommended"
      ],

      parserOptions: {
        project: ["./tsconfig.json"],
        tsconfigRootDir: __dirname
      },
      rules: {
        // TypeScript-specific rules here
        "react/react-in-jsx-scope": "off",
        "@typescript-eslint/ban-ts-comment": "off",
        "@typescript-eslint/no-explicit-any": "off",
        "@typescript-eslint/no-use-before-define": "off",
        "@typescript-eslint/no-shadow": "off",
        "@typescript-eslint/no-unused-vars": "off",
        "import/no-extraneous-dependencies": "off"
      }
    }
  ],
  rules: {
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off",
    "react/destructuring-assignment": "off",
    "no-underscore-dangle": "off",
    "no-console": "off",
    "react/require-default-props": "off",
    "jsx-a11y/label-has-associated-control": "off",
    "import/no-cycle": "off",
    "react/no-array-index-key": "off",
    "import/no-extraneous-dependencies": "off",
    "react/jsx-filename-extension": "off",
    "func-names": "off",
    "no-param-reassign": "off", // could be checked later
    "no-use-before-define": "off", // could be checked later
    "no-unused-vars": "off", // could be checked later
    "no-shadow": "off", // could be checked later
    "react/button-has-type": "off", // could be checked later
    "consistent-return": "off",
    "no-nested-ternary": "off",
    "react/jsx-props-no-spreading": "off",
    "react/no-unstable-nested-components": "off", // could be checked later
    "react-hooks/exhaustive-deps": "off", // could be checked later
    "no-plusplus": "off",
    "jsx-a11y/media-has-caption": "off",
    "array-callback-return": "off", // could be checked later
    "import/no-import-module-exports": "off", // could be checked later,
    "import/extensions": "off",
    "prettier/prettier": [
      "error",
      {
        endOfLine: "auto"
      }
    ],
    "max-len": [
      "error",
      {
        code: 100,
        ignoreUrls: true,
        ignoreStrings: true,
        ignoreTemplateLiterals: true,
        ignoreRegExpLiterals: true,
        ignoreComments: true
      }
    ]
  },
  settings: {
    react: {
      version: "detect"
    },
    "import/resolver": {
      node: {
        extensions: [".js", ".jsx", ".ts", ".tsx"]
      }
    }
  },
  ignorePatterns: [
    "build/",
    "node_modules/",
    "public/",
    "ConnectionTest.tsx",
    "ConnectionLatencyTest.tsx",
    "ParticipantDataModal.tsx",
    "tsconfig.json",
    "package.json",
    "package-lock.json"
  ]
};
