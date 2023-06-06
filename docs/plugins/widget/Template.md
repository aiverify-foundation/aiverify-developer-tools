# Template

Each input block consists of at least two files located under the **templates** folder, which follows the following naming convention:

* \<template cid\>.meta.json
* \<template cid\>.data.mdx

## Template Meta Data

During installation, the Plugin Manager will search for and validate the input block meta data according to the schema [ai-verify.template.schema.json](../../schemas/ai-verify.template.schema.json) schema definitions.

| Propreties | Type | Required | Description |
| ---------- | ---- | -------- | ----------- |
| cid | string, must match pattern `^[a-zA-Z0-9][a-zA-Z0-9-._]*$` | Yes | Unique identifier for the template within the plugin. |
| name | string | Yes | Template name. |
| description | string | No | Template description. |
| author | string | No | Template author |

## Exporting a Template Plugin

For now, the easiest way to create a template component is to export the template as plugin at the AI Verify Project page. This will download a zip file that contains a plugin containing the template data. To add the template component to an existing plugin project, simply copy the **templates** folder in the plugin zip to the target plugin folder. 
