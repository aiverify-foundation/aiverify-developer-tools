{% if cookiecutter.algo_model_support == "Regression" %}
{% include 'templates/tests/test_algo_regression' %}
{% else %}
{% include 'templates/tests/test_algo_classification' %}
{% endif %}