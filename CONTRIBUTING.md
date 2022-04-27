# Contributing

## Workflow

To contribute follow the following steps:

1. Create a new branch in which changes are made. Branches should be named using the following convention: `[<frontend/backend>-]<initials>-<topic>`.  
Branch names are in lowercase. If the change regards the frontend or backend start the name with `frontend` or `backend` respectively. If it's a general change this part is omitted. The topic can be multiple words which should be sperated by hyphens (`-`).
2. Make sure your code works with the latest version of `main`, then create a pull request.
    - Assign the person who will perform the merge as *Assignee* (usually yourself).
    - Optionally: Assign specific people who should review the code as *Reviewers*.
3. Make a comment on our Discord that a pull request is waiting for a faster response.
4. Person reviewing replies on Discord that they will take the request and:
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
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Provide a more detailed description in the next line, if the first line is not descriptive enough

### Folder Structure _(WIP)_
`backend/`: Everything belonging to the backend  
`frontend/`: Everything belonging to the frontend

### Python Style Guide
- The PEP 8 style guide is used: [PEP 8 - Style Guid for Python Code](https://peps.python.org/pep-0008/)
- You can use the [autopep8](https://code.visualstudio.com/docs/python/editing#_general-formatting-settings) formatter of the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) for Visual Studio Code.

### React
_TODO_
