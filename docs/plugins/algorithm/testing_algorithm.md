# Testing Your Algorithm 
When you run your algorithm, certain tests are carried out:

### Running the Data, Model and Ground Truth Files<br>
You will require at least the data and model files to run your algorithm. The files will be read. If the data and/or model cannot be supported, there will be an error message and the algorithm will not be run.
<br>

### Validating the Input Arguments
The algorithm's input argument(s) will be validated against the schema you have defined in `input.schema.json`. This is to ensure that the input argument(s) have the right format and data type.
<br>

### Validating the Generated Output
After running the algorithm, the generated results will be validated against the schema you have defined in `output.schema.json`. This is to ensure that the generated results from the algorithm have the right format and data type.
<br>