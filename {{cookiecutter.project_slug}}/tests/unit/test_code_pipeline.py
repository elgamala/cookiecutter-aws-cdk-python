import pytest
from expects import expect

from cdk_expects_matcher.CdkMatchers import have_resource, ANY_VALUE
import tests.utils.base_test_case as tc


@pytest.fixture(scope="class")
def code_pipeline(request):
    request.cls.cfn_template = tc.BaseTestCase.load_stack_template('CICDPipeline')


@pytest.mark.usefixtures('synth', 'code_pipeline')
class TestCodePipeline(tc.BaseTestCase):

    def test_code_commit_existence(self):
        expect(self.cfn_template).to(have_resource(self.code_commit_repo, {
            "RepositoryName": "{{ cookiecutter.project_slug }}",
            "Tags": [
                {
                    "Key": "CDK/StackClass",
                    "Value": "CICDPipeline"
                },
                {
                    "Key": "Project",
                    "Value": "{{ cookiecutter.project_name }}"
                }
            ]
        }))

    def test_code_pipeline_existence(self):
        expect(self.cfn_template).to(have_resource(self.code_pipeline, {
            "Stages": [
                {
                    "Name": "Source"
                },
                {
                    "Name": "CDK-Tests"
                },
                {
                    "Name": "Security-Checks"
                },
                {
                    "Name": "CDK-Bootstrap"
                },
                {
                    "Name": "CDK-Deploy"
                }
            ],
            "Name": "{{ cookiecutter.project_name }}-CDKPipeline"
        }))
