# Notebook PGE Wrapper

### Related projects:
* [Papermill Project](https://github.com/nteract/papermill)
* [container-builder (HySDS)](https://github.com/hysds/container-builder)

### Dependencies:
* `papermill>=2.2.0` (2.2.0 added `inspect_notebook`)

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

`DockerBuildPGEParamsGenerator` has all the methods 
* `generate_hysdsio` to generate `hysds-io.json.*`
* `generate_job_spec` to generate `job-spec.json.*`

The `main.py` script will iterate over all `.ipynb` files in your repo's `notebook_pges/` directory and generate a 
`hysds_io` and `job_spec` and place it in `docker/`

```bash
usage: main.py [-h] [--submission_type SUBMISSION_TYPE]
               [--required_queue REQUIRED_QUEUE]

Build hysds_io and job_spec json for all notebooks in notebook_pges/

optional arguments:
  -h, --help            show this help message and exit
  --submission_type SUBMISSION_TYPE
                        individual (1 job regardless of query)or iteration (N
                        jobs for however many records recorded by the
                        Elasticsesrch query)
  --required_queue REQUIRED_QUEUE
                        (REQUIRED) default queue required for job
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
