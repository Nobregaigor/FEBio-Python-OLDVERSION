# Example: Add property

The command ADD_PROPERTY is used to add a selection of properties to one or more .feb files. It is important to notice that all properties must be a valid and direct child of the febio_spec root in a .feb file, otherwise, the function will not word correctly. Moreover, properties must be written in xml format and extension.

##### Good example:

```xml
	<Output>
		<plotfile type="febio">
			<var type="displacement"/>
			<var type="stress"/>
			<var type="strain energy density"/>
			<var type="fiber vector"/>
			<var type="relative volume"/>
			<var type="elasticity"/>
		</plotfile>
		<logfile>
		<element_data data="sx;sy;sz;sxy;sxz;syz" file="stress.txt"> </element_data>
			<node_data data="x;y;z" delim=", " file="position_node_out.txt"/>
			<node_data data="ux;uy;uz" delim=", " file="displacement_node_out.txt"/>
			</logfile>
	</Output>
```

##### Bad example:

```xml
		<plotfile type="febio">
			<var type="displacement"/>
			<var type="stress"/>
			<var type="strain energy density"/>
			<var type="fiber vector"/>
			<var type="relative volume"/>
			<var type="elasticity"/>
		</plotfile>
```

This function requires the following inputs:

* FEB_FILE (RA).
* INPUT_FILE (RA).
* INPUT_FOLDER (RA).
* PROPERTIES_FOLDER (O).
* OUTPUT_FOLDER (O).
* SELECTED_PROPERTIES (O).

The first three inputs are Alternative Requirements accepted by the function. The user can select and use one of them and the program will prooceed accordingly. However, if two or more inputs are provided, the program will select based on the following hierarchy ```INPUT_FILE <  FEB_FILE < INPUT_FOLDER```. In this example, we will use a simple .feb file, therefore, we can use any of the first two inputs:

The properties folder must be a directory which includes the valid properties that we will be adding to our raw .feb. These files must be named with the property attribute only. For instance, if we want to add an "Output" section, a file named "output.xml" containg the output information must be included in the property folder directory. In addition, the user has the option to include the value for this input in the config.json file rather than manually providing this input everytime the function is executed.

Moreover, the SELECTED_PROPERTIES must be a string containing the name of the properties to be added to .feb, if the user want's to select only a few of them, otherwise, the user can use the value "all". All properties must be separated by "-". 

Lastly, the output folder provides the program a directory to write the modified feb file.

##### Providing values at command execution:

```bash
  ./main run --ADD_PROPERTIES --INPUT_FILE "path/to/input/file" --PROPERTIES_FOLDER "path/to/properties/dir" --SELECTED_PROPERTIES "output" --INPUT_FILE "path/to/output/file"
```

##### Providing value at config file:

```bash
  ./main run --ADD_PROPERTIES --INPUT_FILE "path/to/input/file" 
```
```json
  "INPUT_DEFAULTS": {
    "ADD_PROPERTIES": {
        "PROPERTIES_FOLDER": "properties",
        "OUTPUT_FOLDER": "with_properties",
        "SELECTED_PROPERTIES": "all"
    },
  }
```

After executing this command, the output content will be added to the .feb file.





