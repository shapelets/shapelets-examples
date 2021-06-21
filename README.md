# shapelets-solo-examples

A set of examples using shapelets-solo platform.

## Requirements

Have been installed the JVM.
Have been installed shapelets-solo.

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

These lines above starts a server in https://localhost:8443 by default and starts a session as admin.

## GUI

Shapelets provides you a web application we call **Cristal-UI**. After start shapelets with the cli or with init*session function the web application **Cristal-UI** is available in https://localhost:8443, so you can go to your favourite browser and type that in the url. Now you can go into **Cristal-UI** login with \_admin*, _admin_ credentials

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
