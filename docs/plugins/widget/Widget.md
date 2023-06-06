# Widget

Each widget consists of at least two files, a meta file describing the widget and the [MDX](https://mdxjs.com/) file for the widget. The files should be located under **widgets** folder of the plugin root directory, and file names should follow this format:

* \<widget cid\>.meta.json
* \<widget cid\>.mdx

Assuming you have created a widget with cid "sample-widget", then there should be the following files under the **widgets** folder:

* sample-widget.meta.json
* sample-widget.mdx

## Widget Meta Data

During installation, the Plugin Manager will search for and validate the widget meta data accounding to the schema [ai-verify.widget.schema.json](../schemas/ai-verify.widget.schema.json) schema definitions.

| Propreties | Type | Required | Description |
| ---------- | ---- | -------- | ----------- |
| cid | string, must match pattern `^[a-zA-Z0-9][a-zA-Z0-9-._]*$` | Yes | Unique identififer for the widget within the plugin. |
| name | string | Yes | Widget name. |
| description | string | No | Widget description. |
| widgetSize | object | Yes | Describe the widget size in terms of canvas grid units. See [Widget Size Object Schema](#widget-size-object-schema) for the schema of the widgetSize object.
| properties | array | No | List of widget properties. See [Widget Property Schema](#widget-property-schema). |
| tags | array of string | No | List of tags for this widget. Used for search and filtering of the widget |
| dependencies | array | No | List of input blocks and/or algorithms that this widget depends on. See [Widget Dependency Schema](#widget-dependency-schema). |
| mockdata | array | No | List of sample data that is provided to the widget in the canvas page. See [Widget Mock Data Schema](#widget-mock-data-schema). |

**Note**: The widget meta data does not contain a gid property as it is automatically inferred and referenced using the format

> \<plugin gid\>:\<widget cid\>

### Widget Size Object Schema

The **widgetSize** property defines the minimum and maximum size of the widget. It is defined in the grid units that is used for the project canvas. When the template designer drags a widget onto the canvas, the default size of the widget is the minimum width and height defined.

| Propreties | Type | Required | Description |
| ---------- | ---- | -------- | ----------- |
| minW | interger, range 1-12 | Yes | Minimum widget width. |
| minH | interger, range 1-36 | Yes | Minimum widget height. |
| maxW | interger, range 1-12 | Yes | Maximum widget width. |
| maxH | interger, range 1-36 | Yes | Maximum widget height. |

### Widget Property Schema

The widget properties allows widget developers to define properties that affects the look and/or behaviour of the widget. Example of properties are color, textual information, etc. Each property should have a default value that is used if the property has no input. The template designers can change the properties of a widget by right clicking the widget in the canvas page to bring up the propery dialog. Each property value can be a string input or selected from the canvas *Global Properties*.

| Propreties | Type | Required | Description |
| ---------- | ---- | -------- | ----------- |
| key | string | Yes | Property key. |
| helper | string | Yes | Helper text for the property. |
| default | string | No | Default value for the property. |

### Widget Dependency Schema

Widget dependencies define the list of input blocks or algorithms that the widget depends on.

| Propreties | Type | Required | Description |
| ---------- | ---- | -------- | ----------- |
| cid | string | Yes | CID of the component dependency. |
| gid | string | No | GID of the plugin which the component dependency resides in. Not required if the component dependency resides in the same plugin as this widget |
| version | string | No | Version of the component dependency. If version is not specified, then no version check will be performed |

The *version* property is optional. If no version is specified, then the portal dependency check will NOT do version checking. It is recommended to specify the dependency version if referencing a component in other plugins.

If the widget defines an input block dependency, the data that user entered in the AI Verify Portal's User Input page can be accessed from the widget MDX through MDX props `props.getIBData` method.

If the widget defines an algorithm dependency, the results that is output by the algorithm will be provided to the widget MDX as MDX props `props.getResults` method.

### Widget Mock Data Schema

Widget mock data provides mock data to the widget at the canvas page. If no mock data is provided, then no data will be provided to the widget at canvas page and the widget MDX should handle this condition.

| Propreties | Type | Required | Description |
| ---------- | ---- | -------- | ----------- |
| type | string, enum ["Algorithm", "InputBlock"] | Yes | Type of sample data |
| cid | string | Yes | CID of the component dependency |
| gid | string | No | GID of the plugin which the component dependency resides in. Not required if the component dependency resides in the same plugin as this widget |
| datapath | string | yes | File path containing the mock data in JSON format, e.g. mockdata.json. The file should be located within the **widgets** folder. |

### Example 

```
{
  "cid": "sample-widget",
  "name": "Sample Widget",
  "description": "This is a sample widget",
  "tags": ["sample"],
  "properties": [
    {
      "key": "title",
      "helper": "Enter the widget title to be displayed at the top of the widget",
      "default": ""
    }
  ],
  "widgetSize": {
    "minW": 1,
    "minH": 1,
    "maxW": 12,
    "maxH": 36
  },
  "dependencies": [
    {
      "cid": "fairness_metrics_toolbox_for_classification",
    },
    {
      "cid": "fairness_tree"
    }
  ],
  "mockdata": [
    {
      "type": "Algorithm",
      "cid": "fairness_metrics_toolbox_for_classification",
      "datapath": "fmt.output.sample.json" 
    },
    {
      "type": "InputBlock",
      "cid": "fairness_tree",
      "datapath": "fairness_tree.sample.json"
    }
  ]
}
```

## Widget MDX

Each widget must contain a valid [MDX](MDX_Guide.md) that will be rendered as a widget in an AI Verify report. During creation or update of an AI Verify project, the user can drag and drop a widget onto a project canvas, which will be eventually rendered as part of a report.

The widget [dependencies](#widget-dependency-schema) informs the sytem what are the algorithms and/or input blocks that the widget depends on. The system then determine what are the algorithms and input blocks to run based on the dependency info. 

The widget MDX are loaded as React components and the component properties are passed and accessed as [**props**](https://mdxjs.com/docs/using-mdx/#props) global variable. 

### Widget Props

| Propreties | Type | Description |
| ---------- | ---- | ----------- |
| inputBlockData | object | Object containing the user input data saved, accessed by its gid `props.inputBlockData[gid]`. |
| result | object | Object containing the output from an algorithm, accessed by its gid `props.result[gid]`. |
| properties | object | Object containing the widget properties entered in the canvas page. |
| container | object | Object containing the widget container information, see [Widget Container](#widget-container) |
| getContainerObserver(callback) | function | Function to create an observer to retrieve the the widget container size, see [Widget Container Observer](#widget-container-observer) |
| getResults(cid, gid=null) | function | Function to return result of an algorithm identified by cid. If gid of the algorithm is not specified, the function assumes same plugin gid as the widget. |
| getIBData(cid, gid=null) | function | Function to return data of an input block identified by cid. If gid of the input block is not specified, the function assumes same plugin gid as the widget. |
| getTest(cid, gid=null) | function | Function to return test result information (if successful), see [Test Result Information](#test-result-information) |
| meta | object | Object containing widget meta data. |
| report | object | Object containing report information, see [Report](#report) |
| modelAndDatasets | object | Object containing model and dataset information used to run the test (See [Models and Datasets](#models-and-datasets)) |

Example MDX to print out some of the widget props:
```
export const cid = "some_algo_cid"

<div>
  <pre>{JSON.stringify(props.modelAndDatasets,null,2)}</pre>
  <pre>{JSON.stringify(props.report,null,2)}</pre>
  <pre>{JSON.stringify(props.getTest(cid),null,2)}</pre>
  <pre>{JSON.stringify(props.getResults(cid),null,2)}</pre>
</div>
```

#### Widget Container Observer

To retrieve the size of the widget container, call the following getContainerObserver function. The callback function passes the container width and height in pixel.

```
props.getContainerObserver((width, height) => {
  // Do something with the constainer width and height
})
```

#### Test Result Information

| Propreties | Type | Description |
| ---------- | ---- | ----------- |
| timeStart | string | ISO data string of start time of test run |
| timeTaken | number | Time to complete test in seconds |
| testArguments | object | Test arguments |

#### Report

| Propreties | Type | Description |
| ---------- | ---- | ----------- |
| timeStart | date | Date and time of when the report starts generation. |
| timeTaken | number | Total time taken (in seconds) to run all the tests and generate report. |
| totalTestTimeTaken | number | Total time taken (in seconds) to run all the tests. |

#### Models and Datasets

| Propreties | Type | Description |
| ---------- | ---- | ----------- |
| testDataset | object | Object containing test dataset information, see [Dataset Object Schema](#dataset-object-schema) for information on dataset fields |
| model | object | Object containing model information |
| groundTruthDataset | object | Object containing ground truth dataset information, see [Dataset Object Schema](#dataset-object-schema) for information on dataset fields |
| groundTruthColumn | string | Ground truth feature name |

##### Dataset Object Schema

| Propreties | Type | Description |
| ---------- | ---- | ----------- |
| filename | string | File name of dataset |
| name | string | Name of dataset |
| size | string | Size of dataset |
| description | string | Dataset description |
| type | string | Dataset type (File, Folder) |
| dataFormat | string | Dataset data format |

##### AI Model Object Schema

| Propreties | Type | Description |
| ---------- | ---- | ----------- |
| name | string | Name of model |
| description | string | model description |
| size | string | Size of model |
| type | string | Model access type (File, Folder, Pipeline, API) |
| modelType | string | Model type (Classification, Regression) |
| modelFormat | string | Model format |
