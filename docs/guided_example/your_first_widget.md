# Creating your First Widget Component

There are three learning objectives in this tutorial:

1. Create a widget component in the existing plugin project.
2. Modify the widget component to display the results from the completed algorithm component
3. Deploy the widget component

## Generating a widget component

Widgets are stored in the **my_plugin/widgets** folder. Use [**ai-verify-plugin gw**](../plugins/Plugin_Tool.md#generate-widget-alias-gw) to generate your widget.

Run the following command to generate a new widget and create a dependency to the algorithm component created earlier.

```bash
ai-verify-plugin gw "my_widget" --name "My Widget" --description "My first widget" --dep "Algorithm,my_algorithm"
```

Verify that the directory ```widgets``` exists in your current directory with the files for the widgets generated inside.

```bash
ls widgets
```

Open the file `my_widget.meta.json` under the ```widgets``` folder and check that the properties are set correctly as shown below:

```JSON
{
  "cid": "my_widget",
  "widgetSize": {
    "minW": 1,
    "minH": 1,
    "maxW": 12,
    "maxH": 36
  },
  "name": "My Widget",
  "description": "My first widget",
  "dependencies": [
    {
      "cid": "my_algorithm"
    }
  ],
  "mockdata": [
    {
      "type": "Algorithm",
      "cid": "my_algorithm",
      "datapath": "my_algorithm.sample.json"
    }
  ]
}
```
## Editing sample file

Open and edit `my_algorithm.sample.json` with a valid sample output from the algorithm or input block. This sample data will be passed to the MDX component props in the project canvas, and allows the MDX to display data based on sample input.

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

## Editing MDX

Open and edit `my_widget.mdx` to implement the MDX content.

```Javascript
export const cid = "my_algorithm"

{props.getResults(cid)?(
  <>
    <b>JSON output of algorithm</b>
    <div style={{ maxHeight:"100px", overflow:"auto" }}>{JSON.stringify(props.getResults(cid))}</div>
  </>
):(
  <div>No data</div>
)}
```

Once you are done with the widget creation, you can proceed to [deploy your plugin](./deploy_your_plugin.md).
