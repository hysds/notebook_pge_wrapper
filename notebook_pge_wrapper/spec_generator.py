import os
import json
import traceback
import argparse

import papermill


"""
# https://wiki.jpl.nasa.gov/pages/viewpage.action?spaceKey=hysds&title=Job+and+HySDS-IO+Specifications
text: A text srtring, will be kept as text
number: A real number
date: A date in ISO format. Will be treated as a "text" field for passing into the container.
datetime: A date with time in YYYY-MM-DDTHH:mm:SS.SSS format. Will be treated as a "text" field.
boolean: true or false in a drop down
enum:  On of a set of options in a drop down.
       Note: must specify "enumerables" field to specify the list of possible options. These will be "text" types in
       the enumerables set.

email: An e-mail address, will be treated as "text"
textarea: Same as text, but displayed larger with the textarea HTML tag
container_version: A version of an existing container registered in the Mozart API. Must define "version_substring"
                   field.
jobspec_version: A version of an existing job-sepcification registered in the Mozart API.
                 Must define "version_substring" field.
hysdsio_version: A version of an existing hysdsio version registered in the current UI.
                 Must define "version_substring" field.
region: Auto-populated from the facet view leaflet tool.
"""

__DEFAULT_DISK_USAGE = '1GB'
__DEFAULT_TIME_LIMIT = 3600
__DEFAULT_SOFT_TIME_LIMIT = 3600

COMPONENT = 'tosca'  # default to

__TEXT = 'text'
__NUMBER = 'number'
__DATE = 'date'
__DATETIME = 'datetime'
__BOOLEAN = 'boolean'
# __ENUM = 'enum'
# __NOTE = 'note'
__EMAIL = 'email'
__TEXT_AREA = 'textarea'
# __CONTAINER_VERSION = 'container_version'
# __JOBSPEC_VERSION = 'jobspec_version'
# __REGION = 'region'
__LIST = 'list'
__DICT = 'dict'

__MAPPER = {
    'str': __TEXT,
    'string': __TEXT,
    'text': __TEXT,
    'float': __NUMBER,
    'num': __NUMBER,
    'int': __NUMBER,
    'integer': __NUMBER,
    'date': __DATE,
    'date_time': __DATETIME,
    'datetime': __DATETIME,
    'bool': __BOOLEAN,
    'boolean': __BOOLEAN,
    'email': __EMAIL,
    'textarea': __TEXT_AREA,
    'list': __LIST,
    'array': __LIST,
    'arr': __LIST,
    'dict': __DICT,
    'obj': __DICT,
    'object': __DICT
}


def _get_hysdsio_param_type(t):
    """
    maps input to hysdsio type (using __MAPPER)
    :param t: str
    :return: str
    """
    # TODO: may need to include List and Dict type, maybe use str.startswith()?
    t_lower = t.lower()
    return __MAPPER.get(t_lower, __TEXT)


def _generate_hysdsio_params(nb_name):  # private method
    nb_params = papermill.inspect_notebook(nb_name)
    params = []

    for k, p in nb_params.items():
        if k.startswith('hysds_'):
            continue

        param_type = p['inferred_type_name']
        description = p['help']
        default_value = p['default']

        hysdsio_param = {
            'name': k,
            'from': 'submitter',
            'type': _get_hysdsio_param_type(param_type)
        }
        if description:
            hysdsio_param['description'] = description
        if default_value:
            try:
                hysdsio_param['default'] = json.loads(default_value)
            except Exception as e:
                print(e)
                hysdsio_param['default'] = default_value

        params.append(hysdsio_param)
    return params


def extract_hysds_specs(nb_name):
    nb_params = papermill.inspect_notebook(nb_name)

    hysds_specs = {}
    for k, p in nb_params.items():
        if not k.startswith('hysds_'):
            continue

        k = k.replace('hysds_', '')
        default_value = p['default']
        try:
            hysds_specs[k] = json.loads(default_value)
        except (json.JSONDecodeError, Exception) as e:
            print(default_value, e)
            traceback.print_exc()
            p['default'] = default_value[1:-1]
    return hysds_specs


def generate_hysdsio(job_label=None, sub_type=None, nb_name=None):
    """
    example: {
        "label":"HySDS job label (hysdsio)",
        "component":"tosca",
        "submission_type":"individual",
        "params": [{...}]
    }
    :param job_label: str, job label for hysds_io
    :param sub_type: {iteration, individual}
                     individual (1 job regardless of query)
                     or iteration (N jobs for however many records recorded by the Elasticsesrch query)
    :param nb_name: str, path + notebook name
    :return: Dict[str, <any>]
    """
    if not sub_type:
        raise RuntimeError("sub_type (submission_type) required for hysdsio generation")
    if not nb_name:
        raise RuntimeError("Jupyter notebook not supplied")

    sub_type = sub_type if sub_type in {'iteration', 'individual'} else None

    hysdsio_params = _generate_hysdsio_params(nb_name)
    hysds_io = {
        'submission_type': sub_type,
        'params': hysdsio_params,
        'component': COMPONENT  # don't see a reason to create a notebook PGE for mozart
    }
    if job_label:
        hysds_io['label'] = job_label
    return hysds_io


def generate_job_spec(time_limit=__DEFAULT_TIME_LIMIT, soft_time_limit=__DEFAULT_SOFT_TIME_LIMIT,
                      disk_usage=__DEFAULT_DISK_USAGE, required_queue=None, nb=None, command=None):
    """
    example: {
        "required_queues":["system-jobs-queue"],
        "command":"/path/to/papermill_wrapper.py $HOME/hello_world.ipynb",
        "disk_usage":"3GB",
        "soft_time_limit": 86400,
        "time_limit": 86700,
        "params" : [...]
    }
    :param time_limit: int
    :param soft_time_limit: int
    :param disk_usage: str (KB, MB, GB) ex. 10GB
    :param required_queue: str or List[str]
    :param nb: str, path of Jupyter notebook
    :param command: str, command field in job_specs json
    :return: Dict[str, <any>]
    """
    if required_queue is None:
        raise RuntimeError("required_queue not provided")
    if not nb:
        raise RuntimeError("Jupyter notebook not supplied")

    if isinstance(required_queue, str):
        required_queue = [required_queue]

    nb_params = papermill.inspect_notebook(nb)
    params = []

    for key in nb_params:
        if key.startswith('hysds_'):
            continue

        params.append({
            'name': key,
            'destination': 'context'
        })

    output_job_spec = {
        'command': command or 'notebook-pge-wrapper execute %s' % nb,
        'time_limit': time_limit,
        'soft_time_limit': soft_time_limit,
        'disk_usage': disk_usage,
        'required_queues': required_queue,
        'imported_worker_files': {
            "$HOME/.aws": "/home/ops/.aws"
        },
        'params': params
    }
    return output_job_spec


def generate_spec_files(nb):
    nb_split = nb.split('.')
    root_name = nb_split[0]

    nb_path = os.path.join('notebook_pges', nb)

    # extracting hysds_io and job_specs from notebook
    hysds_specs = extract_hysds_specs(nb_path)

    time_limit = hysds_specs.get('time_limit')
    soft_time_limit = hysds_specs.get('soft_time_limit')
    disk_usage = hysds_specs.get('disk_usage')
    submission_type = hysds_specs.get('submission_type', 'individual')
    required_queue = hysds_specs.get('required_queue', 'factotum-job_worker-small')
    label = hysds_specs.get('label')
    command = hysds_specs.get('command')

    # generate hysds_io, copying hysds_io.json to docker/
    hysdsio = generate_hysdsio(nb_name=nb_path, sub_type=submission_type, job_label=label)
    hysdsio_file = 'hysds-io.json.%s' % root_name
    hysdsio_file_location = os.path.join('docker', hysdsio_file)

    with open(hysdsio_file_location, 'w+') as f:
        json.dump(hysdsio, f, indent=2)
    print('generated %s' % hysdsio_file_location)

    # generate job_specs, copying job_specs.json to docker/
    job_spec = generate_job_spec(nb=nb_path, soft_time_limit=soft_time_limit, time_limit=time_limit,
                                 required_queue=required_queue, disk_usage=disk_usage)
    job_spec_file = 'job-spec.json.%s' % root_name
    job_spec_file_location = os.path.join('docker', job_spec_file)

    with open(job_spec_file_location, 'w+') as f:
        json.dump(job_spec, f, indent=2)
    print('generated %s' % job_spec_file_location)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build hysds_io and job_spec json for a Jupyter notebook')
    parser.add_argument('--notebook', type=str, required=True,
                        help='(REQUIRED) Path for Jupyter notebook needed to generate hysdsio parameters')
    parser.add_argument('--time_limit', type=int, default=__DEFAULT_TIME_LIMIT,
                        help='hard time limit (secs) for running job (default 3600)')
    parser.add_argument('--soft_time_limit', type=int,
                        help='soft time limit (secs) for running job (default value from --time_limit)')
    parser.add_argument('--disk_usage', type=str, default=__DEFAULT_DISK_USAGE,
                        help='disk usage (KB, MB, GB) memory needed to run job (default 1GB)')
    parser.add_argument('--required_queue', type=str, required=True,
                        help='(REQUIRED) default queue required for job')
    parser.add_argument('--label', type=str, help='description for hysdsio json')
    parser.add_argument('--submission_type', type=str, default='individual',
                        help='individual (1 job regardless of query)'
                             'or iteration (N jobs for however many records recorded by the Elasticsesrch query)')
    args = parser.parse_args()

    notebook_flag = args.notebook
    time_limit_flag = args.time_limit
    soft_time_limit_flag = args.soft_time_limit or time_limit_flag
    disk_usage_flag = args.disk_usage
    required_queue_flag = args.required_queue
    label_flag = args.label
    submission_type_flag = args.submission_type if args.submission_type in {'individual', 'iteration'} else 'individual'

    # docker_pge_generator = DockerBuildPGEParamsGenerator()
    hysdsio = generate_hysdsio(job_label=label_flag, sub_type=submission_type_flag, nb_name=notebook_flag)
    print('hysdsio json: %s\n' % json.dumps(hysdsio, indent=2))

    job_specification = generate_job_spec(time_limit=time_limit_flag, soft_time_limit=soft_time_limit_flag,
                                          disk_usage=disk_usage_flag, required_queue=required_queue_flag,
                                          nb=notebook_flag)
    print('job_spec json: %s\n' % json.dumps(job_specification, indent=2))
