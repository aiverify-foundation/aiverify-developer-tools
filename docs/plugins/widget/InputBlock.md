# Input Block

Each input block consists of at least three files located under the **inputs** folder, which follows the following naming convention:

* \<input block cid\>.meta.json
* \<input block cid\>.mdx
* \<input block cid\>.summary.mdx

Assuming you have created a input block with cid "sample-input-block", then there should be the following files under the **inputs** folder:

* sample-input-block.meta.json
* sample-input-block.mdx
* sample-input-block.summary.mdx

## Input Block Meta Data

During installation, the Plugin Manager will search for and validate the input block meta data according to the schema [ai-verify.inputBlock.schema.json](../../schemas/ai-verify.inputBlock.schema.json) schema definitions.

| Propreties | Type | Required | Description |
| ---------- | ---- | -------- | ----------- |
| cid | string, must match pattern `^[a-zA-Z0-9][a-zA-Z0-9-._]*$` | Yes | Unique identifier for the input block within the plugin. |
| name | string | Yes | Input block name. |
| description | string | No | Input block description. |
| group | string | No | Input blocks that have the same group name will be grouped together in the user input page |
| width | string, enum ["xs", "sm", "md", "lg", "xl"] | No | Defines the width of the input block dialog box in the user input page. If not set, the width will default to "md" |
| fullScreen | boolean | No | Whether the dialog box in the input block should be in fullscreen mode. If this is set to true, the width property is not used |

**Note**: The input block meta data does not contain a gid property as it is automatically inferred and referenced using the format

> \<plugin gid\>:\<input block cid\>

### Example

```
{
  "cid": "sample-input-block",
  "name": "Sample Input Block",
  "description": "This is a sample input block",
  "group": "Sample Group",
  "width": "md",
  "fullScreen": false
}
```

## Input Block MDX

The input blocks are launched as dialog in the user input page, with the width of the dialog box depending on the **width** property in the [meta data](#input-block-meta-data). 

The MDX are loaded as React components and the component properties are passed and accessed as [**props**](https://mdxjs.com/docs/using-mdx/#props) global variable. 

### Input Block Props

| Propreties | Type | Description |
| ---------- | ---- | ----------- |
| data | object | Key-Value Object containing the user input data saved |
| onChangeData | (key: string, value: any) => void | Function to save user data, e.g. `props.onChangeData("mykey","Hello World")` |

## Input Block Summary Typescript

For each input block, there should be a summary file **\<input block cid\>.ts** that is imported by the AI Verify portal. The script MUST implement and export the following methods. For Example,

```
{/* Return summary of data */}
export const summary = (data) => {
	// TODO: replace below code with meaningful summary of data.
  if (!data)
    return "No data";
  return JSON.stringify(data || {})
}

{/* Return progress in percentage (0-100) */}
export const progress = (data) => {
	// TODO: replace below code with percentage of user completion.
  if (!data)
    return 0;
  const totalKeys = 3;
  const numKeys = Object.values(data).filter(v => {
    if (typeof (v) === "string" || Array.isArray(v)) {
      return v.length > 0;
    } else {
      return true;
    }
  }).length;
  return Math.round((numKeys / totalKeys) * 100);
}

{/* Validate data. */}
export const validate = (data) => {
  // TODO: replace below code with data validation. 
  return progress(data) == 100;
}
```

Developers should implement the methods as defined to provide meaningful summary and track progress of the input block completion. The `validate` method tells the portal whether the input block data is valid.

If the input block summary `validate` function return false, then the portal will not allow report generation until the input block data validate success. If the input block does not require the data to be validated before generating report, then developer should return true for this function.
