# Creating your first widget component

There are three learning objectives in this tutorial:

1. Create a widget component in the existing plugin project.
2. Modify the widget component to display the results from the completed algorithm component
3. Deploy the widget component

## Generating a widget component

Widgets are stored in the **template_plugin/widgets** folder. Use [**ai-verify-plugin gw**](../plugins/widget/Plugin_Tool.md#generate-widget-alias-gw) to generate your widget.

Run the following command to generate a new widget and create a dependency to the algorithm component created earlier.

```bash
cd template_plugin/widgets
ai-verify-plugin gw "mywidget" --name "My Widget" --description "A Widget" --dep "Algorithm,your_first_algorithm_component"
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
      "cid": "your_first_algorithm_component"
    }
  ],
  "mockdata": [
    {
      "type": "Algorithm",
      "cid": "your_first_algorithm_component",
      "datapath": "your_first_algorithm_component.sample.json"
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
export const cid = "your_first_algorithm_component"

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

After generating and implementing the plugin and components, run the [**ai-verify-plugin zip**](../plugins/widget/Plugin_Tool.md#zip) command to create a deployable zip. This zip file can be uploaded to the AI Verify Portal using the Plugin Manager. 

```bash
# Make sure you are in the root of the plugin directory (e.g., ./myplugin)
$ ai-verify-plugin zip .
```
