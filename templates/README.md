# Notebook PGE

### Generating a base Notebook PGE project
```bash
$ notebook-pge-wrapper create <project_name>
```
The following project structure will be generated
```
<project_name>
├── README.md
├── docker/
│   └── Dockerfile
└── notebook_pges/
```
* `Dockerfile` will go through [container-builder](https://github.com/hysds/container-builder) to build the docker image
    * Will later be used to execute the notebook in a PGE setting
* Place all your `.ipynb` files in `notebook_pges/`

### Papermill
Your notebooks will leverage `papermill` to execute notebooks
* [Papermill Project](https://papermill.readthedocs.io/en/latest/)
* [Papermill parameters documentation](https://papermill.readthedocs.io/en/latest/usage-parameterize.html)
* Can set parameter types 2 ways
    * Adding a comment, ie. `x = 34  # type: int`
    * [Python type hinting](https://docs.python.org/3/library/typing.html) (introduced in python 3.5)

### HySDS job specs generation
* Tag the top notebook cell with `parameters`
    * To add tags in your notebook, go to the toolbar: `View` -> `Cell Toolbar` -> `Tags`
* prepend any hysds specification fields with `hysds_` and `extract_hysds_specs` will populate `hysds-io` and 
`job_specs` with it's specified values
    * If not found it will set to `default` values (ie. `time_limit: 3600`)
```
# job_specs
hysds_time_limit -> time_limit
hysds_soft_time_limit -> soft_time_limit
hysds_disk_usage -> disk_usage
hysds_required_queue -> required_queue

# hysds-ios
hysds_submission_type -> submission_type
hysds_label -> label
```   
Example:
```python
# parameters
from typing import List

a = 100 # type: int
b = "jfksl" # type: str
c = 10.2553 # type: float
d = [1,2,3,4,5] # type: List
e: List[str] = ['a', 'b', 'c']
f = "fjskl"
g: List[str] = ["a", "b", "c"]

# hysds specs
hysds_time_limit = 57389
hysds_soft_time_limit = 4738
hysds_disk_usage = "10GB"
hysds_submission_type = "iteration"
hysds_required_queue = "test_queue-worker"
hysds_label = "TEST LABEL FOR HYSDS_IOS"
``` 

Use the `notebook-pge-wrapper` cli to generate the spec files
* `notebook-pge-wrapper specs all` to iterate generate spec files for all notebooks in `notebook_pges/`
* `notebook-pge-wrapper specs <notebook path>` to generate spec files for a notebook
```bash
$ notebook-pge-wrapper specs --help
Usage: notebook-pge-wrapper specs [OPTIONS] NOTEBOOK_PATH

  Generates the hysdsio and job specs for json files (in the docker
  directory) for a notebook

  enter "all" to generate all spec files in notebook_pges/

  ie. notebook-pge-wrapper specs <notebook_path or all>

  :param notebook_path: str :return: None
```
