# h5py-cli

This script helps to explore H5 file structure and content with interactive command line interface. The commands in the script are designed similar to linux command.

Usage: `python3 h5py-cli.py <h5 filename>`

```
This command line interface mainly handles attribute, group and dataset of the hdf5 file.
Following commands are defined internally.  Type `help' to see this list.

 cat [attr|dataset]
    display the specific attribute or dataset
 cat [attr|dataset] > [filename]
    save the specific attribute or dataset to an output file
 cd [group]
    change directory/group
 exit
    exit to the operating system
 filename
    show the current filename
 help
    display this screen
 ls
    list the entries of current group, data type prefix:
    a: attribute, g: group, d: dataset
 ls [attr|group|dataset]
    list a specific group, attribute or dataset
 pwd
    print working group
 ```
 
 
# Installing
`h5py`, `numpy` are required.

# License
Apache 2.0 license
