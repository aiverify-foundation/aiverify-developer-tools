# Create your first Widget and Input Block Plugin

This guide shows you how you can develop a widget and input block plugin using the [AI Verify Plugin Tool](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-developers-documentation/-/blob/main/docs/frontend_docs/Plugin_Tool.md).

## Introduction

In AI Verify, plugins are used to extend the basic suite of tests provided. Plugins can consist of algorithms, widgets, and input blocks and they work together as follows:

**Algorithm** <br>
An algorithm is the core of technical AI testing where it reads in the dataset, model, ground truth, and test arguments to compute results using the AI Verify Test Engine. Results computed by algorithms can be displayed on the report generated through the use of widgets. 

**Input blocks** <br>
Input blocks captures and processes user input data. Each block is loaded as a dialog box in the User Input Page. It is designed to allow for more flexibility and better user experience in capturing user input and also supports 'lightweight processing' of user input data without requiring the use of AI Verify Test Engine. User input data captured by input blocks can be displayed on the report generated through the use of widgets.

**Widgets** <br>
Widgets are modular components that users can use to design their report. Widgets can display 'fixed' content set by the widget developers or 'dynamic' content based on its algorithm/ input block dependencies. Widget developers can leverage on the suite of charts provided by [AI Verify Shared Library](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-developers-documentation/-/blob/main/docs/frontend_docs/Shared_Library.md) to visualise results from algorithms or user input data captured by input blocks.

>** Algorithms, widgets and input blocks do not have to be in the same plugin project to work together. The relationship between each algorithm, input block, and widget is determined by the dependencies defined in the widget's meta.schema file. This will be covered later on in this guide [here](###Creating-a-new-Widget)

This guide will focus on the development of input blocks and widgets. The development of algorithms will require additional dependencies and is covered in the [Algorithm Plugin Guide](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-developers-documentation/-/blob/main/docs/plugins/create-algorithm-plugins/first-algorithm-plugin.md).

## Prerequisites

Ensure that the following packages are installed before proceeding with this tutorial.

- [Ubuntu 22.04.2 LTS (Jammy Jellyfish)](https://releases.ubuntu.com/jammy/) <br>
This Linux platform is recommended for our plugin development to ensure the perfect plugin creation experience.

- Node.js or nvm (in order to install -g without sudo)


## Getting Started

The AI Verify Plugin Tool helps to develop and scaffold the plugin project directly from the command line.

For more information on the tool, refer to [AI Verify Plugin Tool Documentation](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-developers-documentation/-/blob/main/docs/frontend_docs/Plugin_Tool.md)

### Installing the AI Verify Plugin Tool

Run the following commands to install the tool.
```
git clone git@gitlab.com:imda_dsl/t2po/ai-verify/ai-verify-portal/ai-verify-plugin.git
cd ai-verify-plugin
npm install -g
npm install
```

### Creating a new Plugin Project

Let's create a new plugin project for the widget and input block that we are going to develop.

We will be using the [**ai-verify-plugin gp**](Plugin_Tool.md#generate-plugin-alias-gp) command to generate a new plugin project.

First, cd to navigate to the desired directory for your plugins. To generate a plugin named "My Plugin" with with gid "my-plugin-123", run the command:
```
ai-verify-plugin gp "my-plugin-123" --name "My Plugin"
```

If you would like a random gid to be generated for your plugin, run the following command instead.
```
ai-verify-plugin gp --name "My Plugin"
```
A new plugin directory named after its gid should be created.

## Building the Input Block

### Creating a new Input Block

Now that you have created the plugin project which will hold the input block and widgets, let's use the [**ai-verify-plugin gib**](Plugin_Tool.md#generate-inputblock-alias-gib) to generate your first input block.

First, cd to your plugin's directory created, which is named after its gid.
```
cd my-plugin-123
```

To generate an input block named "My Input Block" with cid "my-input-block-123" and description "An input block", run the command:
```
ai-verify-plugin gib "my-input-block-123" --name "My Input Block" --description "An input block"
```
An **inputs** folder should be created in your plugin's directory.
There should be the following files under the folder:

* my-input-block-123.meta.json
* my-input-block-123.mdx
* my-input-block-123.ts

### Input Block Meta Data (\<cid>.meta.json)

my-input-block-123.meta.json is a JSON file that defines the following properties of the input block.

| Propreties | Type | Required | Description |
| ---------- | ---- | -------- | ----------- |
| cid | string, must match pattern `^[a-zA-Z0-9][a-zA-Z0-9-._]*$` | Yes | Unique identififer for the input block within the plugin. |
| name | string | Yes | Input block name. |
| description | string | No | Input block description. |
| group | string | No | Input blocks that have the same group name will be grouped together in the user input page |
| width | string, enum ["xs", "sm", "md", "lg", "xl"] | No | Defines the width of the input block dialog box in the user input page. If not set, the width will default to "md" |
| fullScreen | boolean | No | Whether the dialog box in the input block should be in fullscreen mode. If this is set to true, the width property is not used |

Using the AI Verify Plugin tool we have defined values for cid, name and description. Using your favourite IDE, you can edit the file to define other properties as such:
```
{
  "cid": "my-input-block-123",
  "name": "My Input Block",
  "description": "An input block",
  "group": "Sample Group",
  "width": "md",
  "fullScreen": false
}
```

### Input Block UI (\<cid>.mdx)

my-input-block-123.mdx is a MDX file that determines the UI of the input block. Input blocks can be a simple HTML form or a [Decision Tree Component](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-portal/ai-verify-shared-library/-/tree/main/packages/graph). 

The MDX files are loaded as React components and the component properties are passed and accessed as [**props**](https://mdxjs.com/docs/using-mdx/#props) global variable. 

In this guide, we will create your first input block to capture company information using a simple HTML form.

Open my-input-block-123.mdx on your IDE and replace the code with the following HTML form:
```
<div style={{ display:"flex", flexDirection:"column", marginBottom:"10px" }}>

  <label htmlFor="companyName">Company name:</label>
  <input type="text" id="companyName" value={props.data["companyName"]} onChange={(e)=>props.onChangeData("companyName",e.target.value)} />

  <label htmlFor="businessType">Business type:</label>
  <select id="businessType" value={props.data["businessType"]} onChange={(e)=>props.onChangeData("businessType",e.target.value)}>
    <option value="sp">Sole Proprietorship</option>
    <option value="p">Partnership</option>
    <option value="lp">Limited Partnership</option>
    <option value="llp">Limited Liability Partnership</option>
  </select>

  <label htmlFor="uen">Unique Entity Number (UEN):</label>
  <input type="number" id="uen" value={props.data["uen"]} onChange={(e)=>props.onChangeData("uen",e.target.value)} />

  <label htmlFor="businessDesc">Business Description:</label>
  <textarea rows="4" style={{ width:"100%", resize:"none" }} value={props.data["businessDesc"]} onChange={(e)=>props.onChangeData("businessDesc",e.target.value)} />

</div>
```
Each of these user input data can be referenced by their key defined
```
value={props.data["key"]}
```

### Input Block Methods (\<cid>.ts)

my-input-block-123.ts is a typescript file that defines the methods required by AI Verify for each input block. 

| Method | Parameters | Returns | Description |
| ---------- | ---- | -------- | ----------- |
| summary | data: any | string | Generates the summary of user input data to be reflected. \<insert image>|
| progress | data: any | number | Generates the percentage of user input completed. 100% will be reflected as completed. \<insert image>|
| validate | data: any | boolean | Validates user input data. Invalid user input data will trigger an error message and disallow report generation. \<insert image> |

**summary**

The company information collected can be summarised in this format.
```
<companyName>: <uen> (<businessType>)
E.g.: Mike's Bikes: 1234567A (Sole Proprietorship)
```
Let's modify the summary function in my-input-block-123.ts to generate the desired summary format.

The \<companyName>, \<uen> and \<businessType> can be accessed by their keys defined in the MDX file.
```
export function summary(data: any): string {
  if (!data)
    return "No data";
  return `${data["companyName"]}: ${data["uen"]} (${data["businessType"]})`
}
```

**progress**

Edit total keys to 4 since we have four fields: companyName, uen, businessType, businessDesc.

```
const totalKeys = 4;
```

**validate**

Input block will only be valid if all fields are filled. 

Congratulations! You have created your first input block. In order for this information to be presented in the report generated, we will need to create a widget for this plugin.

##### See Also (TODO)
* [Creating complex input blocks: functions and config](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-stock-plugins/aiverify.stock.process-checklist/-/blob/main/inputs/processChecklistSummary.ts)

## Building the Widget

### Creating a new Widget

Let's use the [**ai-verify-plugin gw**](Plugin_Tool.md#generate-widget-alias-gw) to generate your first widget.

First, cd to your plugin's directory created, which is named after its gid. 
```
cd my-plugin-123
```

To generate an widget named "My Widget" with cid "my-widget-123" and dependency on the the input block "my-input-block-123", run the command:
```
ai-verify-plugin gw "my-widget-123" --name "My Widget" --description "I'm a Widget" --dep "InputBlock,my-plugin-123:my-input-block-123"
```
A **widgets** folder should be created in your plugin's directory.
There should be the following files under the folder:

* my-input-block-123.sample.json
* my-widget-123.meta.json
* my-widget-123.mdx

##### See Also (TODO)
* [Algorithm dependencies]()

### Widget Meta Data (\<cid>.meta.json)

my-widget-123.meta.json is a JSON file that defines the following properties of the widget.

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

Using the AI Verify Plugin tool we have defined values for cid, name, description, dependencies, and also default values for widgetSize. From the input block dependency defined, mockdata value which contains the reference to the sample file is also auto-generated. Using your favourite IDE, you can edit the file to edit or define other properties as such:
```
{
  "cid": "my-widget-123",
  "widgetSize": {
    "minW": 1,
    "minH": 1,
    "maxW": 12,
    "maxH": 36
  },
  "name": "My Widget",
  "description": "I'm a Widget",
  "dependencies": [
    {
      "gid": "my-plugin-123:my-input-block-123"
    }
  ],
  "mockdata": [
    {
      "type": "InputBlock",
      "gid": "my-plugin-123:my-input-block-123",
      "datapath": "my-input-block-123.sample.json"
    }
  ],
  "tags": ["sample tag"],
  "properties": [
    {
      "key": "displayType",
      "helper": "Enter the type of company information to display (full/partial)",
      "default": "full"
    }
  ]
}
```

### Widget Mock Data (\<input-block-cid>.sample.json)

my-input-block-123.sample.json is a JSON file that provides mock data to the widget at the canvas page. This mock data should provide users a "sample preview" of how the widget should look like in the report generated.
> *If no mock data is provided, the [widget MDX]() should handle this condition.

Let's mock the the company information collected by the input block you just created. Replace the code in my-input-block-123.sample.json with the following:
```
{
  "companyName": "Mike's Bikes",
  "businessType": "sp",
  "uen": "1234567A",
  "businessDesc": "Mike's Bikes sells bikes that are light."
}

```

### Widget UI (\<cid>.mdx)

my-widget-123.mdx is a MDX file that determines the UI of the widget. Widgets can be simple markdown content, [styled JSX components](), or [Charts from the AI Verify Shared Library](). 

The widget MDX files are loaded as React components and the component properties are passed and accessed as [**props**](https://mdxjs.com/docs/using-mdx/#props) global variable. 

### Widget Props

| Propreties | Type | Description |
| ---------- | ---- | ----------- |
| inputBlockData | object | Object containing the user input data saved, accessed by its gid `props.inputBlockData[gid]`. *Input block gids are defined by \<plugin-gid>:\<input-block-cid>
| result | object | Object containing the output from an algorithm, accessed by its gid `props.result[gid]`. |
| properties | object | Object containing the widget properties entered in the canvas page. |
| container | object | Object containing the widget container information, see [Widget Container](#widget-container) |

For this guide, let's create a JSX component that displays the JSON output from the input block you created.

Replace the code in my-widget-123.mdx with the following:
```
export const ibgid = "my-plugin-123:my-input-block-123"

{(props.properties.displayType="full")?(
  <>
    <b>Full Company Info</b>
    <div style={{ maxHeight:"100px", overflow:"auto" }}>{JSON.stringify(props.inputBlockData[ibgid].companyName)}</div>
    <div style={{ maxHeight:"100px", overflow:"auto" }}>{JSON.stringify(props.inputBlockData[ibgid].businessType)}</div>
    <div style={{ maxHeight:"100px", overflow:"auto" }}>{JSON.stringify(props.inputBlockData[ibgid].uen)}</div>
    <div style={{ maxHeight:"100px", overflow:"auto" }}>{JSON.stringify(props.inputBlockData[ibgid].businessDesc)}</div>
  </>
):(
  <>
    <b>Partial Company Info</b>
    <div style={{ maxHeight:"100px", overflow:"auto" }}>{JSON.stringify(props.inputBlockData[ibgid].companyName)}</div>
    <div style={{ maxHeight:"100px", overflow:"auto" }}>{JSON.stringify(props.inputBlockData[ibgid].businessType)}</div>
  </>
)}
```


## Deploying the Plugin

After generating and implementing the plugin and components, navigate to the plugin directory and run the [**ai-verify-plugin zip**](Plugin_Tool.md#zip) command to create the plugin zip. 

```
cd my-plugin-123
ai-verify-plugin zip
```
This plugin zip file allows for easy sharing of AI Verify testing components with the community. To use the plugin you just created in an AI Verify project, simply install this zip file using AI Verify's Plugin Manager. You can also share this zip file with


<b>Congratulations!</b> You have successfully created your first input block and widget plugin!<br>
You should explore the capabilities of AI Verify plugins by checking these out:
* [Building Widgets that uses charts to display results from Algorithms]()
* [Building a Decision Tree Input Block]()
* [Building beautiful Input Block forms]()

------------------------------------------------------