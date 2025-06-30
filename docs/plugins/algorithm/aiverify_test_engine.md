# Understanding the AI Verify Test Engine
The [**AI Verify Test Engine**](https://github.com/aiverify-foundation/aiverify/tree/main/aiverify-test-engine) is a python module under **AI Verify** Github repository and provides core interfaces, converters, data, model and plugin managers to facilitate the development of tests for AI systems. 

AI Verify Test Engine is published to [PyPI](https://pypi.org/project/aiverify-test-engine/) and can be installed using `pip`.

| Installation Command                           | Description                                                                                                                                        |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pip install aiverify-test-engine`             | Installs only the core functionalites. Supports tabular data formats like CSV, as well as Pandas pickle and Joblib files, and Scikit-learn models. |
| `pip install aiverify-test-engine[dev]`        | Includes additional dependencies for development. Intended for developers who want to contribute to the project.                                   |
| `pip install aiverify-test-engine[tensorflow]` | Installs optional Tensorflow and Keras dependencies.                                                                                               |
| `pip install aiverify-test-engine[pytorch]`    | Installs optional PyTorch dependencies.                                                                                                            |
| `pip install aiverify-test-engine[gbm]`        | Installs XGBoost and LightGBM packages. Supports serializing models in these formats.                                                              |
| `pip install aiverify-test-engine[all]`        | Installs the core package along with all additional non development dependencies.                                                                  |


## Categories of Support
There are four categories of support for algorithms: 

### Model
Models are frameworks that are run by algorithms. 

Models currently supported:

- LightGBM
- Scikit-learn
- XGBoost
- PyTorch

### Model Pipeline
Model pipelines are models which apply a list of transforms and final estimator to the data.

Model pipelines currently supported:

- Scikit-learn
- PyTorch

### Deserializer
Deserializers process serialized data and make them into readable objects. Model and data files can sometimes be passed in as a serialized file type (e.g. Joblib). A serialized file is not easily readable and modifiable by humans. If we have the right deserializer for the serialized file, it wil deserialize the file into an object like Pandas dataframe, which users are able to modify. 

Deserializers currently supported:

- Delimiter
- Joblib
- Pickle
- TensorFlow
- Image

### Data Type
Data type refers to the type of data after it has been deserialized. If the data passed in does not require deserializing (e.g. the data file is `csv` file), the data type will be whatever is in the data file.

Data types currently supported:

- Delimiter (colon, comma, pipe, semicolon, space, tab separated values)
- Pandas
- Image (JPG, JPEG, PNG)


