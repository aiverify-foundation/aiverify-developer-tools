# Testing Your Algorithm 
If the algorithm template is generated using `aiverify-plugin`, a default `test_e2e.py` and `test_algo.py` are generated to be run with [`pytest`](https://docs.pytest.org/en/stable/). You should modify the test files and update according to your test requirements.

To run the tests, execute the following commands under the algorithm directory.

```sh
pytest .
```

### Sample Test Data, Model and Ground Truth Files

You can use the sample test data and models files found [here](https://github.com/aiverify-foundation/aiverify/tree/main/stock-plugins/user_defined_files). As the algorithm inputs support reading of files from URL, you can pass in the URL of raw data files to be used in your tests.

### Validating the Input Arguments
The algorithm's input argument(s) will be validated against the schema you have defined in `input.schema.json`. This is to ensure that the input argument(s) have the right format and data type.

### Validating the Generated Output
After running the algorithm, the generated results will be validated against the schema you have defined in `output.schema.json`. This is to ensure that the generated results from the algorithm have the right format and data type.
