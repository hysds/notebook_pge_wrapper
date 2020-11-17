# Notebook PGE Wrapper

### Related projects:
* [Papermill Project](https://github.com/nteract/papermill)
* [container-builder (HySDS)](https://github.com/hysds/container-builder)

### Dependencies:
* Python 3
* `click>=7.1.2`
* `papermill>=2.2.0` (`2.2.0` added `inspect_notebook`)

### Installation
```bash
cd notebook_pge_wrapper
pip install -e .
```

`notebook-pge-wrapper` will have 3 main sub-commands
* `create` - generates a base skeleton project for end-users to develop notebook PGEs
* `specs` - takes a `-n <path to notebook>` argument and generates a `hysdsio` and `job_spec` json file in the `docker/` directory
* `execute` for notebook execution
```bash
$ notebook-pge-wrapper --help
Usage: notebook-pge-wrapper [OPTIONS] COMMAND [ARGS]...

  A CLI wrapper for notebook_pge_wrapper

Options:
  --help  Show this message and exit.

Commands:
  create   Creates the project root directory: <project_root> ├── README.md...
  execute  Execute a .ipynb notebook :param notebook_path: path to the...
  specs    Generates the hysdsio and job specs for json files (in the
           docker...
```

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

### HySDS job specs generation
* Tag the top notebook cell with `parameters`
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
* `papermill`'s `inspect_notebook` function will extract variables from this cell

<p>
The scripts here will help end users generate hysds-io.json and job-spec.json for Jupyter notebooks

`spec_generator.py` has all the methods 
* `generate_hysdsio` to generate `hysds-io.json.*`
* `generate_job_spec` to generate `job-spec.json.*`


The `main.py` script will iterate over all `.ipynb` files in your repo's `notebook_pges/` directory and generate a 
`hysds_io` and `job_spec` and place it in `docker/`

Or you can use the `notebook-pge-wrapper` cli to generate the spec files
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


HySDS spec `json` files

`hysds-io.json`
```json
{
  "submission_type": "iteration",
  "params": [
    {
      "name": "a",
      "from": "submitter",
      "type": "number",
      "default": 100
    },
    {
      "name": "b",
      "from": "submitter",
      "type": "text",
      "default": "jfksl"
    },
    {
      "name": "c",
      "from": "submitter",
      "type": "number",
      "default": 10.2553
    },
    {
      "name": "d",
      "from": "submitter",
      "type": "list",
      "default": [
        1,
        2,
        3,
        4,
        5
      ]
    },
    {
      "name": "e",
      "from": "submitter",
      "type": "text",
      "default": "['a', 'b', 'c']"
    },
    {
      "name": "f",
      "from": "submitter",
      "type": "text",
      "default": "fjskl"
    },
    {
      "name": "g",
      "from": "submitter",
      "type": "text",
      "default": [
        "a",
        "b",
        "c"
      ]
    }
  ],
  "component": "tosca"
}
```

`job_spec.json`
```json
{
  "command": "python notebook_wrapper.py $HOME/notebook_pges/test.ipynb",
  "time_limit": 57389,
  "soft_time_limit": 4738,
  "disk_usage": "10GB",
  "required_queues": [
    "factotum-job_worker-small"
  ],
  "imported_worker_files": {
    "$HOME/.aws": "/home/ops/.aws"
  },
  "params": [
    {
      "name": "a",
      "destination": "context"
    },
    {
      "name": "b",
      "destination": "context"
    },
    {
      "name": "c",
      "destination": "context"
    },
    {
      "name": "d",
      "destination": "context"
    },
    {
      "name": "e",
      "destination": "context"
    },
    {
      "name": "f",
      "destination": "context"
    },
    {
      "name": "g",
      "destination": "context"
    }
  ]
}
```

### Notebook execution
`notebook-pge-wrapper` has a `execute` sub-command for notebook execution
* Optional `--context` flag for the path to `_context.json` but will default to the current directory if not provided 

```bash
$ notebook-pge-wrapper execute --help
Usage: notebook-pge-wrapper execute [OPTIONS] NOTEBOOK_PATH

  Execute a .ipynb notebook :param notebook_path: path to the .ipynb file
  :param context: path to the _context.json file, default to _context.json
  in current directory if not supplied

Options:
  --context TEXT
  --help          Show this message and exit.
```

### Python Unit Tests
Add unit test files under `test/`
```bash
python -m unittest
```
</p>


### Related issues:
* `hysds_io` and `job_specs` has values that are needed for job specification on execution
    * [Open Github issue (Papermill)](https://github.com/nteract/papermill/issues/547)
    * If the notebook can have a cell tagged with `specifications` we can re-use the existing functionality in
    `inspect_notebook` and use those values to populate `hysds_io.json` and `job_spec.json`
