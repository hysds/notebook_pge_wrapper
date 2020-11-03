# Notebook PGE Wrapper

### Related projects:
* [Papermill Project](https://github.com/nteract/papermill)
* [container-builder (HySDS)](https://github.com/hysds/container-builder)

### Dependencies:
* papermill>=2.2.0 (2.2.0 added `inspect_notebook`)

<p>
The scripts here will help end users generate hysds-io.json and job-spec.json for Jupyter notebooks

`DockerBuildPGEParamsGenerator` has all the methods 
* `generate_hysdsio` to generate `hysds-io.json.*`
* `generate_job_spec` to generate `job-spec.json.*`

The `main.py` script will iterate over all `.ipynb` files in your repo's `notebook_pges/` directory and generate a 
`hysds_io` and `job_spec` and place it in `docker/`

```
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
</p>


### Related issues:
* `hysds_io` and `job_specs` has values that are needed for job specification on execution
    * [Open Github issue (Papermill)](https://github.com/nteract/papermill/issues/547)
    * If the notebook can have a cell tagged with `specifications` we can re-use the existing functionality in
    `inspect_notebook` and use those values to populate `hysds_io.json` and `job_spec.json`
