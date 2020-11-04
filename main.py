import os
import json
import argparse

from notebook_pge_wrapper.nb_spec_generator import DockerBuildPGEParamsGenerator


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build hysds_io and job_spec json for all notebooks in notebook_pges/')
    parser.add_argument('--submission_type', type=str, default='individual',
                        help='individual (1 job regardless of query)'
                             'or iteration (N jobs for however many records recorded by the Elasticsesrch query)')
    parser.add_argument('--required_queue', type=str, help='(REQUIRED) default queue required for job')
    args = parser.parse_args()
    submission_type = args.submission_type or 'individual'
    required_queue = args.required_queue or 'factotum-job_worker-small'

    """
    1. iterate through notebook_pges/ directory
    2. for every .ipynb
        2a. generate job_spec and hysds_io json file
        2b. save them in the docker/ directory
    """

    docker_pge_generator = DockerBuildPGEParamsGenerator()
    nb_directory = 'notebook_pges'

    # TODO:
    # specification values (time_limit, disk_usage, submission_type) are hard coded (for now)
    # opened a Github issue to allow for inspection of notebook cell that's tagged with something else (not parameters)
    # https://github.com/nteract/papermill/issues/547

    if not os.path.exists('docker'):
        print('docker directory should already exist, please check your repo')
        os.mkdir('docker')

    for nb in os.listdir(nb_directory):  # iterate through notebook_pges/ directory
        if not nb.endswith('.ipynb'):
            print('%s is not a notebook, skipping...' % nb)
            continue

        nb_split = nb.split('.')
        root_name = nb_split[0]

        nb_path = os.path.join('notebook_pges', nb)

        # generate hysds_io
        # copying hysds_io.json to docker/
        hysdsio = docker_pge_generator.generate_hysdsio(nb_name=nb_path,
                                                        sub_type=submission_type)
        hysdsio_file = 'hysds-io.json.%s' % root_name
        hysdsio_file_location = os.path.join('docker', hysdsio_file)

        with open(hysdsio_file_location, 'w+') as f:
            json.dump(hysdsio, f, indent=2)
        print('generated %s' % hysdsio_file_location)

        # generate job_specs
        # copying job_specs.json to docker/
        job_spec = docker_pge_generator.generate_job_spec(nb_name=nb_path, required_queue=required_queue)
        job_spec_file = 'job-spec.json.%s' % root_name
        job_spec_file_location = os.path.join('docker', job_spec_file)

        with open(job_spec_file_location, 'w+') as f:
            json.dump(job_spec, f, indent=2)
        print('generated %s' % job_spec_file_location)
