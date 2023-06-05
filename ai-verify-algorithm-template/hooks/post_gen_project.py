import os.path
import shutil
import json

# Get the current project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_templates_folder() -> None:
    """
    Removes folder that provides source codes for different plugin types
    """
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, "templates"))


def remove_json_empty_lines() -> None:
    """
    Remove empty lines in generated file
    """
    # Opening JSON file
    json_filename = os.path.join(
        PROJECT_DIRECTORY, "{{cookiecutter.project_slug}}.meta.json"
    )
    json_file = open(json_filename)

    # returns JSON object as a dictionary
    data = json.load(json_file)

    # Close file
    json_file.close()

    # Writing the json back to file
    with open(json_filename, "w") as outfile:
        outfile.write(json.dumps(data, indent=4))


def main():
    # Remove templates folder in the generated folder
    remove_templates_folder()

    # Remove empty lines in meta.json
    remove_json_empty_lines()


if __name__ == "__main__":
    main()
