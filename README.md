# Experimental Hub

An online tool for researchers in the field of synchrony to host and conduct customizable online experiments with users.

**TODO** _features_

# Setup

**TODO**: _pre-build release can be found_ ...

**TODO**: _quick setup / start + requirements_

---

## Building & Starting

For the general setup and prerequisites, please take a look at the [frontend](./frontend/README.md#configuration) and [backend](./backend/README.md#configuration) READMEs.

1. Build frontend
    - Skip this step if there where no changes to the frontend since the last build process
    - Go to the frontend directory: `cd frontend`
    - Build the frontend: `npm run build`. Make sure the build process finishes without any errors
2. (Re-) Start server
    - If the server is already running: stop the server
    - Make sure to take a look at the settings. For more details see [backend README](./backend/README.md#configuration)
        - It is recommended to set `environment` to `prod` to disable [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
    - Start the server by executing `main.py` in the backend directory. For example from the root directory: `python backend/main.py`

### Notes

-   For development, the React / frontend development server is recommended: `npm start`
