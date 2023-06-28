# Contributing

## Workflow

To contribute code to this project, see the following steps:

0. Checkout our current open [Issues](https://github.com/TUMFARSynchrony/experimental-hub/issues) and add your contribution idea to our [discussion board](https://github.com/TUMFARSynchrony/experimental-hub/discussions/categories/ideas). 
1. Create a new branch in which changes are made. Branches should be named using the following convention: `[<frontend/backend>-]<initials>-<topic>`.  
Branch names are in lowercase. If the change regards the frontend or backend start the name with `frontend` or `backend` respectively. If it's a general change this part is omitted. The topic can be multiple words which should be sperated by hyphens (`-`).
2. Make sure your code works with the latest version of `main`, then create a pull request.
    - Assign the person who will perform the merge as *Assignee* (usually yourself).
    - Optionally: Assign specific people who should review the code as *Reviewers*. If you don't know who to assign, put NCEghtebas there as a default.
3. (External) An appropriate reviewer will be assigned and review the code contribution like with the steps below.
   (Internal) Person reviewing replies on Discord that they will take the request and:
    1. Add themselves as *Reviewer* (if not already)
    1. Try running the code
    1. Review the code (errors, style, comments, etc.)
5. If
    - **Major changes** are needed then repeat the process after addressing changes which were requested by the reviewer.
    - **Minor changes** are needed then the reviewer can approve the request and let the code contributor know that they are free to merge after addressing the minor changes.
6. Delete branch(es) after merging into `main`

## Conventions
The following conventions should be followed when working on experimental-hub.

### Git Commit Messages
- Use the past tense ("Added feature" not "Add feature")
- Limit the first line to 72 characters or less
- Provide a more detailed description in the next line, if the first line is not descriptive enough

### Folder Structure _(WIP)_
`backend/`: Everything belonging to the backend  
`frontend/`: Everything belonging to the frontend

### Python 

- The PEP 8 style guide is used: [PEP 8 - Style Guid for Python Code](https://peps.python.org/pep-0008/)
- Since the corresponding [Docstring Conventions](https://peps.python.org/pep-0257/) are quite open, we use the [numpy Style Guide](https://numpydoc.readthedocs.io/en/latest/format.html) for docstrings.
	- Additional docstring examples can be taken from the [pandas docstring guide](https://python-sprints.github.io/pandas/guide/pandas_docstring.html), which follows the numpy docstring convention.
- For code formatting, we use [Black](https://github.com/psf/black).
	- Note that black uses a line width of 88 characters instead of 79 proposed in pep8. We follow the black convention. [See black docs](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#line-length).
- Static type checking should be enabled.
	- We use [Pyright](https://github.com/microsoft/pyright), which is included in the vscode extension [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance).

We provide some settings for vscode in ./vscode/settings.json, e.g. for code formatting and static type checking.


### React
Using Husky, Prettier, and ESLint which are installed upon `npm install` we define our frontend style guidelines: 
- Husky pre-commit script will auto-format changed files using prettier and if your commit breaks es-lint rules it won't allow you to commit before fixing those issues.
- For code formatting, we use [Prettier](https://prettier.io/).
- For static code analysis, we use [ESLint](https://eslint.org/docs/latest/rules/).
- To format all files, run `npm run format` but this should not be necessary because we have the Husky library which will auto format upon commiting to a branch. 
- To check all syntactic errors and warnings `npm run lint` which is also not necessary because Husky library run the command upon commit. 

## Recommended vscode extensions

For development with vscode, we recommend the following vscode extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) for python language support.
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) for static type checking.
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) for styling on frontend.
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) for static code analysis on frontend.

