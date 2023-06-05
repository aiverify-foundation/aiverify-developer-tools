# In-Depth Reference

## Understanding Your Installed Packages

### zip
`zip` is a package which compresses and packages a directory into a `.zip` file. We will be using `zip` to package the algorithm plugin into a distributable package.<br/>
To install the package:
``` 
sudo apt install -y zip
```

### jq
`jq` is a package which does JSON processing. We will be using `jq` to extract fields from a JSON configuration file. <br>
To install the package:
```
sudo apt install -y jq
```

### Cookiecutter
`Cookiecutter` is a command-line utility Python package that helps with creating projects from project templates. We will be using `Cookiecutter` to create the algorithm project from our predefined template. <br>
To install Cookiecutter using <b>pip or pip3</b>:
```
pip install cookiecutter
```
You can try creating your own Cookiecutter template. Refer to [tutorial](https://cookiecutter.readthedocs.io/en/stable/tutorials/tutorial1.html) for more information.




