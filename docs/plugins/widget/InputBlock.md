# Input Block

Each input block consists of at least three files located under the **inputs** folder, which follows the following naming convention:

* \<input block cid\>.meta.json
* \<input block cid\>.mdx
* \<input block cid\>.ts

Assuming you have created a input block with cid "sample-input-block", then there should be the following files under the **inputs** folder:

* sample-input-block.meta.json
* sample-input-block.mdx
* sample-input-block.ts

## Input Block Meta Data

During installation, the Plugin Manager will search for and validate the input block meta data accounding to the schema [ai-verify.inputBlock.schema.json](../schemas/ai-verify.inputBlock.schema.json) schema definitions.

| Propreties | Type | Required | Description |
| ---------- | ---- | -------- | ----------- |
| cid | string, must match pattern `^[a-zA-Z0-9][a-zA-Z0-9-._]*$` | Yes | Unique identififer for the input block within the plugin. |
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

For each input block, there should be a summary file **\<input block cid\>.ts** that is imported by the AI Verify portal. The script MUST implement and export the following methods.

```
/**
 * Return summary of data
 */
export function summary(data: any): string {
  ...
}

/**
 * Return progress in percentage (0-100). 100% will be refected as completed in the Input Progress list.
 */
export function progress(data: any): number {
  ...
}

/**
 * Return whether the data is valid. If data validation is not required, just return true.
 */
export function validate(data: any): boolean {
  ...
}
```

Developers should implement the methods as defined to provide meaningful summary and track progress of the input block completion. The validate method tells the portal whether the input block data is valid.
