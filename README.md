# Experimental Hub

<!-- goals, product vision, and roadmap. -->

An online tool for researchers to host and conduct customizable online experiments with users.

![Quick Demo Exp Hub](.gif)

As a part of our vision for the experimental hub, we hope to make at home video conferencing studies have more laboratory control through the **experimenter and participant workflows** we have designed in allowing safegaurds in the workflow and a flexible UI (e.g. custom participant video screen position, size, and order, limiting participant exposure pre-experiment to others in the call or seeing themselves with a fitler too early, etc.). We also hope that the experimental templates and filters our platform uses helps the **egological validity and repeatability** of both HCI and psychology experiments and encourages sharing of anonymized data of the experiment. Finally, because our expirmental hub is self hosted, there should be more control over the **data privacy** of where potentially sensitive video and audio data is being stored. 

For in detail motivation about the Experimental hub see our [introduciton to the Experimental Hub](https://github.com/TUMFARSynchrony/experimental-hub/wiki/) , otherwise check out our [quick start](./README.md#Building&Starting) or [detailed set up instructions](https://github.com/TUMFARSynchrony/experimental-hub/wiki/Project-Setup) to try it out yourself!

# Setup
<!-- **TODO**: _pre-build release can be found_ ...

**TODO**: _quick setup / start + requirements_
--- -->

## Building & Starting

In case you want to build the frontend yourself, follow the steps in this section.

For the general setup and prerequisites, please take a look at the [frontend](./frontend/README.md#configuration) and [backend](./backend/README.md#configuration) READMEs.
Continue with the steps bellow after both the frontend and backend are set up.

1. Build frontend
    - Skip this step if there where no changes to the frontend since the last build process
    - Go to the frontend directory: `cd frontend`
    - Build the frontend: `npm run build`. Make sure the build process finishes without any errors
2. (Re-) Start server
    - If the server is already running: stop the server
    - Make sure to take a look at the settings. For more details see [backend configuration](./backend/README.md#configuration)
        - It is recommended to set `environment` to `prod` to disable [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
    - Start the server by executing `main.py` in the backend directory. For example from the root directory: `python backend/main.py`

### Notes

-   For development, the React / frontend development server is recommended: `npm start`
