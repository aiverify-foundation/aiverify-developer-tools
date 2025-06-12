from pathlib import Path

import pytest
from {{cookiecutter.project_slug}}.algo_init import AlgoInit
from aiverify_test_engine.plugins.enums.model_type import ModelType

{% if cookiecutter.algo_model_support == "Both" %}
regression_non_pipeline = {
    "data_path": str("tests/user_defined_files/data/sample_reg_donation_data.sav"),
    "model_path": str(
        "tests/user_defined_files/model/sample_reg_donation_sklearn_linear.LinearRegression.sav"
    ),
    "ground_truth_path": str("tests/user_defined_files/data/sample_reg_donation_data.sav"),
    "run_pipeline": False,
    "model_type": ModelType.REGRESSION,
    "ground_truth": "donation",
}
binary_classification_pipeline = {
    "data_path": str(
        "tests/user_defined_files/data/sample_bc_pipeline_credit_data.sav"
    ),
    "model_path": str("tests/user_defined_files/model/sample_bc_credit_sklearn_linear.LogisticRegression.sav"),
    "ground_truth_path": str(
        "tests/user_defined_files/data/sample_bc_pipeline_credit_ytest_data.sav"
    ),
    "run_pipeline": False,
    "model_type": ModelType.CLASSIFICATION,
    "ground_truth": "default",
}
{% elif cookiecutter.algo_model_support == "Regression" %}
regression_non_pipeline = {
    "data_path": str("tests/user_defined_files/data/sample_reg_donation_data.sav"),
    "model_path": str(
        "tests/user_defined_files/model/sample_reg_donation_sklearn_linear.LinearRegression.sav"
    ),
    "ground_truth_path": str("tests/user_defined_files/data/sample_reg_donation_data.sav"),
    "run_pipeline": False,
    "model_type": ModelType.REGRESSION,
    "ground_truth": "donation",
}
{% elif cookiecutter.algo_model_support == "Classification" %}
binary_classification_pipeline = {
    "data_path": str(
        "tests/user_defined_files/data/sample_bc_pipeline_credit_data.sav"
    ),
    "model_path": str("tests/user_defined_files/model/sample_bc_credit_sklearn_linear.LogisticRegression.sav"),
    "ground_truth_path": str(
        "tests/user_defined_files/data/sample_bc_pipeline_credit_ytest_data.sav"
    ),
    "run_pipeline": False,
    "model_type": ModelType.CLASSIFICATION,
    "ground_truth": "default",
}
{% endif %}


@pytest.mark.parametrize(
    "data_set",
    [
        {% if cookiecutter.algo_model_support == "Both" %}
        regression_non_pipeline,
        binary_classification_pipeline,
        {% elif cookiecutter.algo_model_support == "Regression" %}
        regression_non_pipeline,
        {% elif cookiecutter.algo_model_support == "Classification" %}
        binary_classification_pipeline,
        {% endif %}
    ],
)
def test_plugin(data_set):
    # Create an instance of PluginTest with defined paths and arguments and Run.
    core_modules_path = ""
    plugin_test = AlgoInit(
        data_set["run_pipeline"],
        core_modules_path,
        data_set["data_path"],
        data_set["model_path"],
        data_set["ground_truth_path"],
        data_set["ground_truth"],
        data_set["model_type"],
    )
    plugin_test.run()

    json_file_path = Path.cwd() / "output" / "results.json"
    assert json_file_path.exists()
