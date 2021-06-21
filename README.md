# shapelets-solo-examples

A set of running data-apps examples for Shapelets platform.

## Requirements

This package requires the python package shapelets-solo and the Java JVM 1.8 to be installed before running the examples.

```shell
pip install shapelets-solo
python -m shapelets install
```

![cli example](./images/cli.png)

## Run

After the installation, you can run the application by typing `python -m shapelets start` from a terminal or runnning the script below in a python file or python cli.

```python
from shapelets import init_session
init_session("admin", "admin")
```

![init_session example](./images/code.png)

Above lines start a background process running the shapelets-server in https://localhost:8443 by default and starts a session as admin.

## GUI

Shapelets brings a built-in web application, named **Cristal-UI**. After starting shapelets from the CLI or the init_session, the web application is available at https://localhost:8443. Once the server is up and running, you could go to your favourite browser and login into the web applications with _admin_ as user and _admin_ as password.

![Cristal-UI](./images/login.png)

## CLI commands

| command | description                                   |
| ------- | --------------------------------------------- |
| install | Installs required 3rd party libs              |
| start   | Starts a Shapelets process                    |
| status  | Reports the status of the system              |
| stop    | Stops a Shapelets process by pid              |
| tail    | Tails the logs for a Shapelets process by pid |

All these commands accept `--help` flag also.
