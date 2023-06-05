# AI Verify Plugin

The AI Verify plugins allows contributors to developer their own plugins, that can be installed into AI Verify portal and used to extend the functionality of the portal.

## Terminology
This section defines the terminology used.

| Term | Definition |
| ---- | ---------- |
| plugin | AI Verify plugin that can be installed using the AI Verify portal. |
| component | Each AI Verify plugin consists of one or more components and can be used to extend the functionality of the system. The types of components are described in the table [below](#ai-verify-components). |
| gid | Global Identifier. All plugins requires a unique global identifier that is used to identify the plugin. See [Global Identifier (GID)](#global-identifier-gid). |
| cid | Component ID. Unique ID that identifies the component within the plugin. See [Component Identifier (CID)](#component-identifier-cid) |

## Plugin Structure

The diagram below describes the folders and files that may be found under each plugin.
![Plugin Structure Image](images/Plugin-Structure.png?raw=true)

Each of the component type folder can contain one or more components.

For algorithms, each algorithm has its own subfolder under the **algorithms** folder named with the algorithm id. For example, algorithmA should have a sub-folder called "algorithmA" under the algorithms folder.

For widgets, input blocks and templates, each instance of the components should be saved under the component folder; and the filenames of the component should correspond to the component cid. For example, widgetA should have the following files under the widgets folder.
* widgetA.meta.json
* widgetA.mdx

## AI Verify Components

The different components that can be found in a plugin is described in the table below. Please refer to the linked article for more information on the component schemas and required files.

| Component Type | Component Type Folder | Description |
| -------------- | ------------- | ----------- | 
| Algorithm | algorithms | Algorithm components add new test algorithms to the system. |
| [Input Block](InputBlock.md) | inputs | Loaded as a dialog box at the project User Input page ot prompt user to input data |
| [Widget](Widget.md) | widgets | Used in canvas to display information to user and printed as part of report. |
| [Template](Template.md) | templates | Project templates that, when installed, can be used at creation of new projects to load a pre-defined canvas |


## Plugin Package

The plugin package is a **zip** file containing the plugin meta file (plugin.meta.json) and at least one components type folder containing at least one component. The file and folder structure of a plugin is described in the plugin structure [diagram](#plugin-structure).

### Global Identifier (GID)

The GID identifies the plugin and MUST be globally unique, i.e. no two plugin should have the same GID. The format of the GID must match the following pattern:

> ^[a-zA-Z0-9][a-zA-Z0-9-._]*$

Note that the first character of the GID must be an alphanumeric character. It is recommended to use a tool like UUID Version 4 generator to generate the GID.

### Component Identifier (CID)

The CID identifies a plugin component and MUST be unique within the plugin. The format of the GID must match the follow pattern:

> ^[a-zA-Z0-9][a-zA-Z0-9-._]*$

# Plugin Meta Data

The **plugin.meta.json** file is required for all plugins. During installation, the Plugin Manager will scan the root plugin folder for the file and validates the file according to the [ai-verify.plugin.schema.json](../schemas/ai-verify.plugin.schema.json) schema definition.

| Propreties | Type | Required | Description |
| ---------- | ---- | -------- | ----------- |
| gid | string, must match pattern `^[a-zA-Z0-9][a-zA-Z0-9-._]*$` | Yes | Unique global identifier to identify the plugin. |
| version | string | Yes | Plugin version, should follow [Semantic Versioning](https://semver.org/) format. |
| name | string | Yes | Plugin name |
| author | string | No | Author of the plugin |
| description | string | No | Description of the plugin |
| url | string | No | URL to the plugin web page if available |

## Example
```
{
  "gid": "e6402035-7294-4b69-ace1-68a0442f0194",
  "name": "Sample Plugin",
  "version": "1.0.0",
  "author": "Acme Corporation",
  "description": "This is a sample plugin",
  "url": "https://acme.com/sampleplugin/"
}
```

