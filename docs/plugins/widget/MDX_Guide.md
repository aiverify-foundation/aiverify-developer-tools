# MDX Simple Guide

MDX is a superset of markdown that allows developers to use JDX in the markdown content. It allows developers to write [Markdown](https://commonmark.org/) with embedded components through [JSX](https://facebook.github.io/jsx/). You can learn more about MDX in the [MDX Site](https://mdxjs.com/).

For AI Verify projects, [widgets](Widget.md) and [input blocks](InputBlock.md) use MDX to create dynamic React components that is loaded as part of canvas or user input prompts.

## MDX Props

MDX [props](https://mdxjs.com/docs/using-mdx/#props) is used to pass data from the parent container to the MDX content. The data is accessed through the global **props** variable. The following sections describe what data is passed to the widget and input block MDX.

### [Widget Props](Widget.md#widget-props)

Each widget MDX has the following properties:

* props.inputBlockData
* props.result
* props.properties
* props.container

**Note**: For inputBlockData and result properties, developer should handle cases where the result or input block data is not available and handle accordingly.

For example, to access the result of an algorithm.

```
export const algo_gid = "my-algoritm-gid"

{props.result[algo_gid]?(
  <>
    <b>JSON output of algorithm</b>
    <div style={{ maxHeight:"100px", overflow:"auto" }}>{JSON.stringify(props.result[algo_gid])}</div>
  </>
):(
  <div>No data</div>
)}
```

The following example display the width and height of the parent container.

```
<div style={{ widget:props.container.width, backgroundColor:"olive", color:"white" }}>
  Container size: width {props.container.width}px, height {props.container.height}px
</div>
```

### [Input Block Props](InputBlock.md#input-block-props)

Each input block MDX has the following properties:

* props.data
* props.onChangeData

## Markdown

MDX supports standard Markdown (see [cheatsheet](https://commonmark.org/help/)).

Some examples of markdown.

*Italic* and **bold** text with some `inline code`.
* Unordered list
1. Ordered List

## JSX

JSX provides support for reusable components in MDX.

For example, to use JSX markup directly:

```
<div>Hello World</div>
```

To create a JDX component in an MDX:

```
export const HelloWorld = () => (
  <div>Hello World again</div>
)

<HelloWorld />
```

It is also possible to *import* another MDX or component file.

For example, you can save the above HelloWorld component to a seperate "helloWorld.mdx" file and then import it using:

```
import { HelloWorld } from './helloWorld.mdx'
```

## HTML Form Elements for Input Block

Developers can use [HTML form elements](https://www.w3schools.com/html/html_form_elements.asp) to prompt and capture user input. Developers can use `props.onChangeData` to save the user data. Onchange, the saved data will be available in `props.data`.

Below is an example of a component that displays a simple form and save the form data onChange.

```
<div style={{ display:"flex", flexDirection:"column", marginBottom:"10px" }}>
  <label htmlFor="fname">First name:</label>
  <input type="text" id="fname" value={props.data["fname"]} onChange={(e)=>props.onChangeData("fname",e.target.value)} />
  <label htmlFor="lname">Last name:</label>
  <input type="text" id="lname" value={props.data["lname"]} onChange={(e)=>props.onChangeData("lname",e.target.value)} />
  <label htmlFor="bio">Bio:</label>
  <textarea rows="4" style={{ width:"100%", resize:"none" }} value={props.data["bio"]} onChange={(e)=>props.onChangeData("bio",e.target.value)} />
</div>
```

## AI Verify Shared Library

The [AI Verify Shared Library](https://github.com/IMDA-BTG/aiverify/tree/main/ai-verify-shared-library) provides some shared components that can be imported by MDX. See [Shared Library Documentation](Shared_Library.md).

### JSX Component Styling

To ensure consistent stylings for widgets, it is recommended that JSX components use the CSS classes as provided in the [AI Verify Shared Library Styles](https://github.com/IMDA-BTG/aiverify/tree/main/ai-verify-shared-library/packages/styles).

The following classnames provide different color schemas:

* c-primary
* c-secondary
* c-success
* c-info
* c-warning
* c-error

For example, to change header color:
```
<h4 class="c-primary">Primary Test Color</h4>
```

To style buttons:
```
<button class="aiv-button">My Button</button>
```

To use a different color for styled buttons:
```
<button class="aiv-button c-secondary">My Button</button>
```

### Example use of BarCharts

Below is an example of how to add a [BarChart](https://github.com/IMDA-BTG/aiverify/tree/main/ai-verify-shared-library/packages/charts#barchart) component from the [AI Verify Shared Charts Library](https://github.com/IMDA-BTG/aiverify/tree/main/ai-verify-shared-library/packages/charts).

```
import { BarChart } from 'ai-verify-shared-library/charts'

export const data01 = [
  {
    name: 'Page A',
    uv: 4000,
    pv: 2400,
    amt: 2400,
  },
  {
    name: 'Page B',
    uv: 3000,
    pv: 1398,
    amt: 2210,
  },
  {
    name: 'Page C',
    uv: 2000,
    pv: 9800,
    amt: 2290,
  },
  {
    name: 'Page D',
    uv: 2780,
    pv: 3908,
    amt: 2000,
  },
  {
    name: 'Page E',
    uv: 1890,
    pv: 4800,
    amt: 2181,
  },
  {
    name: 'Page F',
    uv: 2390,
    pv: 3800,
    amt: 2500,
  },
  {
    name: 'Page G',
    uv: 3490,
    pv: 4300,
    amt: 2100,
  },
];

<div style={{ width:props.container.width, height:"220px", padding:"10px" }}>
  <BarChart
    data={data01}
    xAxisDataKey="name"
    bars={[{ dataKey:"uv" }, { dataKey:"pv" }, { dataKey:"amt" }]}
  />
</div>
```

### Example use of Decision Tree

The [AI Verify Shared Library DecisionTree](https://github.com/IMDA-BTG/aiverify/tree/main/ai-verify-shared-library/packages/graph) allows user to build their own decision tree.

You can find an example of Decision Tree Input Block from the [Fairness Metrics Toolbox for Classification](https://github.com/IMDA-BTG/aiverify/tree/main/stock-plugins/aiverify.stock.fairness-metrics-toolbox-for-classification) plugin.
An example use of the **DecisionTree** component can be found in the implementation for the [AI Verify Fairness Tree](https://github.com/IMDA-BTG/aiverify/blob/main/stock-plugins/aiverify.stock.fairness-metrics-toolbox-for-classification/inputs/fairness_tree.mdx) is found under the *inputs* folder.


