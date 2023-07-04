# Contributing

## Workflow

To contribute code to this project, see the following steps:

0. Checkout our current open [Issues](https://github.com/TUMFARSynchrony/experimental-hub/issues) and add your contribution idea to our [discussion board](https://github.com/TUMFARSynchrony/experimental-hub/discussions/categories/ideas).
1. Create a new branch in which changes are made. Branches should be named using the following convention: `[<frontend/backend>-]<initials>-<topic>`.  
   Branch names are in lowercase. If the change regards the frontend or backend start the name with `frontend` or `backend` respectively. If it's a general change this part is omitted. The topic can be multiple words which should be sperated by hyphens (`-`).
2. Make sure your code works with the latest version of `main`, then create a pull request.
   - Assign the person who will perform the merge as _Assignee_ (usually yourself).
   - Assign specific people who should review the code as _Reviewers_. If you don't know who to assign, put NCEghtebas there as a default. At least one approval is required for the merge.
3. (External) An appropriate reviewer will be assigned and review the code contribution like with the steps below.
   (Internal) Person reviewing replies on Discord that they will take the request and:
   1. Add themselves as _Reviewer_ (if not already)
   1. Try running the code
   1. Review the code (errors, style, comments, etc.)
4. If
   - **Major changes** are needed then repeat the process after addressing changes which were requested by the reviewer.
   - **Minor changes** are needed then the reviewer can approve the request and let the code contributor know that they are free to merge after addressing the minor changes.
5. Delete branch(es) after merging into `main`

## Conventions

The following conventions should be followed when working on experimental-hub.

- Do not push your own IDE settings. We want every contributor to have their freedom on IDE settings.

### Git Commit Messages

- Use the past tense ("Added feature" not "Add feature")
- Limit the first line to 72 characters or less
- Provide a more detailed description in the next line, if the first line is not descriptive enough

### Folder Structure _(WIP)_

`backend/`: Everything belonging to the backend  
`frontend/`: Everything belonging to the frontend

### Python for Backend

- We suggest to use a virtual environment. All required libraries are installed with `pip install -r ./backend/requirements.txt`.
- The PEP 8 style guide is used: [PEP 8 - Style Guid for Python Code](https://peps.python.org/pep-0008/)
- Since the corresponding [Docstring Conventions](https://peps.python.org/pep-0257/) are quite open, we use the [numpy Style Guide](https://numpydoc.readthedocs.io/en/latest/format.html) for docstrings.
  - Additional docstring examples can be taken from the [pandas docstring guide](https://python-sprints.github.io/pandas/guide/pandas_docstring.html), which follows the numpy docstring convention.
- For code formatting, we use [Black](https://github.com/psf/black) targetting `Python 3.10`.
  - Note that black uses a line width of 88 characters instead of 79 proposed in pep8. We follow the black convention. [See black docs](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#line-length).
  - Configuration is available in `backend/pyproject.toml` file.
  - Github pre-commit hook is used in order to run automated formatting on the staged files at each commit.
  - Github workflows for formatting are triggered at each push and pull request to `main` branch.
- For linting, we use [Flake8](https://flake8.pycqa.org/en/latest/).
  - Configuration is available in `backend/.flake8` file.
  - Github workflows for linting are triggered at each pull request to `main` branch.
- Static type checking should be enabled.
  - We use [Pyright](https://github.com/microsoft/pyright), which is included in the vscode extension [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance).

We provide some example settings for vscode in `./vscode.example/settings.json`, e.g. for code formatting and static type checking.

### ReactJS for Frontend

Using Husky, Prettier, and ESLint which are installed upon `npm install` we define our frontend style guidelines:

- Husky pre-commit script will auto-format changed files using prettier and if your commit breaks es-lint rules it won't allow you to commit before fixing those issues.
- For code formatting, we use [Prettier](https://prettier.io/).
- For static code analysis, we use [ESLint](https://eslint.org/docs/latest/rules/).
- To format all files, run `npm run format` but this should not be necessary because we have the Husky library which will auto format upon commiting to a branch.
- To check all syntactic errors and warnings `npm run lint` which is also not necessary because Husky library run the command upon commit.

## Recommended vscode extensions

For development with vscode, we recommend the following vscode extensions:

Backend:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) for python language support.
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) for python formatting.
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8) for python linting.
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) for static type checking.

Frontend:

- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) for styling on frontend.
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) for static code analysis on frontend.
