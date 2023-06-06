# Understanding the Core Modules
The core modules are custom packages that support different types of models, model pipelines, serialized data and data. When you run your algorithm, we will read in your model and data files. We will then traverse the `test_engine_core_modules` directory and see if there are support packages to handle the model and data files. If there are, we will be able to process the data correctly.  

There are four categories of support for algorithms: 
<br>

### Model
Models are frameworks that are run by algorithms. 
<br>

Models currently supported:

- LightGBM
- scikit-learn
- XGBoost
<br>

### Model Pipeline
Model pipelines are models which apply a list of transforms and final estimator to the data.

Model pipelines currently supported:

- scikit-learn Pipeline

### Deserializer
Deserializers process serialized data and make them into readable objects. Model and data files can sometimes be passed in as a serialized file type (e.g. Joblib). A serialized file is not easily readable and modifiable by humans. If we have the right deserializer for the serialized file, it wil deserialize the file into an object like Pandas dataframe, which users are able to modify. 
<br>

Deserializers currently supported:

- Joblib
- Pickle
- TensorFlow
<br>

### Data Type
Data type refers to the type of data after it has been deserialized. If the data passed in does not require deserializing (e.g. the data file is `csv` file), the data type will be whatever is in the data file.<br>
Data types currently supported:

- Delimiter Data (includes colon, comma, pipe, semicolon, space, tab separated values)
- Pandas
<br>