
# atomicredteam-streamlit

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

This is a helper web app for the [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) project


## Features

 - New Atomic: Create new atomics via web forms
 - Validate Atomic: Upload your YAML file and validate them

More features coming soon...
## Run Locally

Clone the project

```bash
  git clone https://github.com/cyberbuff/atomicredteam-streamlit
```

Go to the project directory

```bash
  cd atomicredteam-streamlit
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Start the server

```bash
  streamlit run Hello.py
```


## Running Tests

To run tests, run the following command

```bash
  pytest . -v
```


## Contributing

Contributions are always welcome! 
Source code is located in `pages/` directory. Feel free to edit them and create a PR. 

Before committing and pushing the code, install `pre-commit` and install pre-commit hooks. `pre-commit` hooks are used for linting.

Install pre-commit

```bash
pip3 install pre-commit
```

Install pre-commit hooks
```bash
pre-commit install-hooks
```
