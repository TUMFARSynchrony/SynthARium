# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app, npx create-react-app my-app)

## Prerequisites

- node and npm - [NodeJS](https://nodejs.org/)

## Setup

- go to frontend folder
- `npm install` - installs all dependencies
- `npm run build` - builds the frontend

## Using HTTPS

To use HTTPS instead of just http, set `HTTPS=true` in `frontend/.env` and restart the frontend dev server if already running.
A custom certificate can also be defined there.

Most browsers will require that requests send to the backend are also HTTPS, if HTTPS is enabled.
See [backend readme](./../backend/README.md#using-a-ssl-certificate) for details on how to enable HTTPS for the backend.

## Configuring the Development Server

In the `frontend` folder: copy the `.env.template` file and rename it to `.env`
The file can be configured:

- `REACT_APP_BACKEND`: address of the backend server
- `HTTPS`: If true, the frontend dev server will use HTTPS. See [Create React App Docs](https://create-react-app.dev/docs/using-https-in-development/)
- `SSL_CRT_FILE`: Optional path to SSL certificate file. See [Create React App Docs](https://create-react-app.dev/docs/using-https-in-development/)
- `SSL_KEY_FILE`: Optional path to SSL certificate private key file. See [Create React App Docs](https://create-react-app.dev/docs/using-https-in-development/)

## Available Scripts

In the project directory folder `frontend/`, you can run:

### `npm install`

Which installs all our frontend dependancies.

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder. Make sure to run this command only in the `frontend/` directory.
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.
