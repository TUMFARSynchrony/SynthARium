# Setup

## Prerequisites

-   python 3.10.x
    -   Previous versions may work, but are not yet checked

**TODO** check compatibility with older python versions

## Installing dependencies

Execute `pip install -r requirements.txt` inside the backend folder

## Configuration

The backend can be configured using the `backend/config.json`.

-   `host` - str : host address the backend should use
-   `port` - int : port the backend should use
-   `environment` - str : `dev` or `prod`
-   `https` - bool : Weather the backend should use https
-   `ssl_cert` - str : path to ssl certificate. Only used if https is true
-   `ssl_key` - str : path to ssl private key. Only used if https is true
-   `log` - str : Logging level for Hub. Must be one of: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Default: `INFO`
-   `log_file` - null | str : If given, the logger will write the log into the file instead of the console
-   `log_dependencies` - str : Logging level for project 3rd party dependencies (see [requirements.txt](./requirements.txt)). Must be one of: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Default: `WARNING`. Using `INFO` or `DEBUG` may lead to a strong increase in output.

### Logging overview

The following logging levels are available for `log` and `log_dependencies` in the [configuration](#configuration):

| Logger output | `DEBUG` | `INFO` | `WARNING` | `ERROR` | `CRITICAL` |
| ------------- | :-----: | :----: | :-------: | :-----: | :--------: |
| debug         |    x    |   -    |     -     |    -    |     -      |
| info          |    x    |   x    |     -     |    -    |     -      |
| warning       |    x    |   x    |     x     |    -    |     -      |
| error         |    x    |   x    |     x     |    x    |     -      |
| critical      |    x    |   x    |     x     |    x    |     x      |

-   If the logger is set to `INFO`, information with the debug level is ignored and only important events are logged, possibly with less detail.
-   If the logger is set to `DEBUG` everything is logged. This also includes additional information that can be helpful in debugging.

## Using a SSL Certificate

Most browsers only allow access to media devices (webcam, microphone, ...) if the website is localhost or HTTPS. Additionally, websites served over HTTPS can not make requests to HTTP servers. Therefore a SSL certificate is required to access the backend from other devices.

Place the certificate and private key in `backend/certificate` and make sure `ssl_cert` and `ssl_key` in `config.json` are set correctly.
Then set `https` to `true` and start the server.

In case the frontend dev server is used, make sure to update the backend server address there. See [frontend readme](./../frontend/README.md#configuring-the-development-server).

### Acquiring a SSL Certificates

If you want to conduct an experiment, you need to get a trusted SSL Certificate. One way to get free SSL certificates is [Let's Encrypt](https://letsencrypt.org/).

### Using a Self Signed Certificate

For development and testing purposes, self signed certificates can be used. **Don't use self signed certificates for production!**

A bash script using openssl to generate a self signed certificate can be found at: `backend/certificate/generate_certificate.sh`. You can check if openssl is installed using: `openssl version`.

In case openssl is not an option, take a look at [Generating self-signed certificates on Windows](https://medium.com/the-new-control-plane/generating-self-signed-certificates-on-windows-7812a600c2d8).

When using a self signed certificate, your browser will likely warn you about it.
To allow the frontend to connect to the server, you must manually "accept the risk" by directly opening the backend in the browser. The server will tell you its address after starting, it will look something like: https://127.0.0.1:8080.

# Start

Execute `python3 main.py`

Depending on your system, `python3` can be replaced with `py` or `python`

# Development Guidelines

See [Contributing](./../CONTRIBUTING.md).
