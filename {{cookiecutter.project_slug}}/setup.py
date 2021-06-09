#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

aws_cdk_version="{{ cookiecutter.aws_cdk_version }}"

requirements = [
    f"aws-cdk.core{aws_cdk_version}",
    f"aws-cdk.aws_iam{aws_cdk_version}",
    f"aws-cdk.aws_s3{aws_cdk_version}",
    f"aws-cdk.aws_codecommit{aws_cdk_version}",
    f"aws-cdk.aws_ssm{aws_cdk_version}",
    f"aws-cdk.aws_codepipeline{aws_cdk_version}",
    f"aws-cdk.aws_codepipeline_actions{aws_cdk_version}",
    f"aws-cdk.aws_codebuild{aws_cdk_version}",
    f"aws-cdk.aws_ec2{aws_cdk_version}",
    f"aws-cdk.aws_backup{aws_cdk_version}",
    "cdk-expects-matcher>=0.1.0",
    "GitPython",
    "checkov>=2.0.173"
]

test_requirements = ['pytest>=3']

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    python_requires='>=3.6',
    package_dir={"": "cdk"},
    packages=find_packages(where="cdk"),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Architects',
        'Intended Audience :: DevOps Engineers',
        'Topic :: AWS CDK',
        'Topic :: Infrastructure as code',
        'Topic :: IaC'
{%- if cookiecutter.open_source_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="{{ cookiecutter.project_short_description }}",
    install_requires=requirements,
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='{{ cookiecutter.project_slug }}',
    name='{{ cookiecutter.project_slug }}',
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
    version='{{ cookiecutter.version }}',
    zip_safe=False,
)
