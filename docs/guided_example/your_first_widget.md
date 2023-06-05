# Creating your first widget component

There are three learning objectives in this tutorial:

1. Create a widget component in the plugin project.
2. Modify the widget component to display the results from the algorithm component
3. Deploy the widget component

First, let's create a new algorithm project.

## Generating the project

Use the [**ai-verify-plugin gp**](Plugin_Tool.md#generate-plugin-alias-gp) command to generate a plugin project.

To generate a plugin, run the following command with `gid` specified as `my-plugin`

```Javascript
$ ai-verify-plugin gp "myplugin" --name "My Plugin"
```

Once the plugin has been generate, run `cd` to change the directory to the plugin. For example,

```bash
$ cd myplugin
```

## Generating a widget component

Use [**ai-verify-plugin gw**](../plugins/widget/Plugin_Tool.md#generate-widget-alias-gw) to generate your widget.

Run the following command to generate a new widget and create a dependency to the algorithm component created earlier.

```bash
$ ai-verify-plugin gw "mywidget" --name "My Widget" --description "A Widget" --dep "Algorithm,your_first_algorithm_plugin"
```

Open the file `mywidget.meta.json` and check that the properties are set correctly as shown below:

```JSON
{
  "cid": "mywidget",
  "widgetSize": {
    "minW": 1,
    "minH": 1,
    "maxW": 12,
    "maxH": 36
  },
  "name": "My Widget",
  "description": "A Widget",
  "dependencies": [
    {
      "cid": "your_first_algorithm_plugin"
    }
  ],
  "mockdata": [
    {
      "type": "Algorithm",
      "cid": "your_first_algorithm_plugin",
      "datapath": "your_first_algorithm_plugin.sample.json"
    }
  ]
}
```
### Editing sample file

Open and edit `your_first_algorithm.sample.json` with a valid sample output from the algorithm or input block. This sample data will be passed to the MDX component props in the project canvas, and allows the MDX to display data based on sample input.

```JSON
{"my_expected_results": [
      33280.0,
      40000.0,
      70000.0,
      50000.0,
      50000.0,
      40000.0,
      50000.0,
      0.0,
      90000.0,
      35000.0,
      80000.0,
      50000.0
  ]    
}
```

### Editing MDX

Open and edit `mywidget.mdx` to implement the MDX content.

```Javascript
export const cid = "your_first_algorithm_plugin"

{props.getResults[cid]?(
  <>
    <b>JSON output of algorithm</b>
    <div style={{ maxHeight:"100px", overflow:"auto" }}>{JSON.stringify(props.getResults(cid))}</div>
  </>
):(
  <div>No data</div>
)}
```

## Deploying Widget Components

After generating and implementing the plugin and components, run the [**ai-verify-plugin zip**](../plugins/widget/Plugin_Tool.md#zip) command to create a deployable zip. This zip file can be uploded to the AI Verify Portal using the Plugin Manager. 

```bash
# Make sure you are in the root of the plugin directory (e.g., ./myplugin)
$ ai-verify-plugin zip .
```
