# Deploy Your Plugin

Now that you have created your plugin component(s), it is time to package it into a single plugin for deployment.

If you are following the guided example, you should have the following components completed and packaged in its own respective folders:

1. my_algorithm component
2. my_widget component

## Combine the plugin components

The **my_plugin** directory should mimic the same plugin structure. The algorithms directory should contain algorithms, with each one in its own respective folder. The widget components will be stored in the widgets directory.

![plugin structure](../images/plugin_structure.png)

In this guided example, the algorithms directory will have the folder *my_algorithm*. The widgets directory will contain *my_widget.meta.json*, *my_widget.mdx*, and *my_algorithm.sample.json*.

## Edit Plugin Details (Optional)

You may wish to edit *plugin.meta.json* to change the plugin details.

```py title="plugin.meta.json" linenums="1" hl_lines="2 3 4 5 6"
{
  "gid": "my_plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "My First Plugin",
  "author": "AI Verify"
}
```

## Deploy your Plugin

You can package your plugin using the [`ai-verify-plugin zip`](../plugins/Plugin_Tool.md#zip) command.

```bash
# Execute this command under the my_plugin directory
ai-verify-plugin zip
```

!!! note
    A new folder `dist` will be created. This folder is where the packaged `.zip` file will be created and placed.

Verify that the zip file ```my_plugin-1.0.0.zip``` exists in your `dist` directory:

The resulting plugin is packaged as a `zip` file, which can be used to share with other developers who are interested in using your plugin. Users and developers can then upload the zip file onto AI Verify through the plugin manager and use it in the report.

## Uploading the plugin

To upload the plugin, start the frontend portal of AI Verify. You will need to install AI Verify if you have not done so. The instructions to install and run AI Verify from source code can be found in the [User Guide](https://imda-btg.github.io/aiverify/getting-started/source-code-setup/).

1. Once the portal is started up, visit the portal at [http://localhost:3000/home](http://localhost:3000/home). In the homepage, click on "Plugins" to visit the Plugin Manager page:
   ![aiv_homepage](../images/aiv_home_page.png)

2. In the **Plugin Manager page**, click on "INSTALL PLUGIN" at the top right and select ```my_plugin-0.1.0.zip```, then click on "INSTALL" :
   ![install_plugin](../images/install_plugin.png)

   
3. The following prompt should appear to inform you that the plugin has been installed successfully: 

      ![plugin_installed_successfully](../images/plugin_installed_successfully.png)

4. You should see your plugin in the list of installed plugins:
   ![plugin_manager_page](../images/plugin_manager_page.png)

## Generating the Report

1. It is time to run the plugin. In the homepage, click on "Create New Project":
   ![aiv_homepage](../images/aiv_home_page.png)
2. Fill in the project details and click "Next" on the top right:
    ![project_details](../images/project_details.png)
3. On the **Design Report** page, drag your widget from the left panel to the canvas:
   ![canvas](../images/canvas.png)
   Since the widget is a **dynamic height** widget, the widget height will expand dynamically to fill to the bottom of the canvas. When you're ready, click "Next" on the top right.
4. On the **Select the Datasets and AI Model to be tested** page, select and upload the dataset, ground truth dataset and model. You can use the dataset provided in the template or download from [here](https://github.com/IMDA-BTG/aiverify/tree/main/examples). Refer to the following table for reference.

      | Data, Model, and Test Arguments | Selected Dataset / Model / Test Arguments |
      | ---- | ---------- |
      | Testing Dataset | ```sample_bc_credit_data.sav``` |
      | Ground Truth Dataset | ```sample_bc_credit_data.sav```, Ground Truth: ```default``` |
      | AI Model | ```sample_bc_credit_data.sav``` | 
      | Test Arguments | ```gender``` |

5. During model upload, choose ```Upload AI Model``` to the AI model file and click "Next".
   ![upload_model](../images/upload_model.png)
6. Click "OPEN" at the "My Algorithm" box and type `gender` for the feature name.
7. Click "OPEN" at the "My Input Block" box and enter your first and last name. The end result should look like this.
   ![data_and_model_selection](../images/data_and_model_selection.png) 
8. When you are ready, click on "Next" on the top right. Click on "PROCEED" when prompted:
   ![confirm_generate_report](../images/confirm_generate_report.png) 
9. You should see the logs of what is happening in the backend and when your report has been generated, you should see the "Test Completed" prompt in the top right. Click on "VIEW REPORT" to see your report:
   ![generated_report](../images/generated_report.png) 
10. Your report will be displayed as a PDF file.
   ![report](../images/report.png) 
   Congratulations! You have generated your first report. 