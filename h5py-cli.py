#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
'''
H5pyCli
Author: Hu, Ying-Hao (hyinghao@hotmail.com)
Version: 0.2
Last modification date: 2022-05-28

Copyright 2022 Hu, Ying-Hao

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''

import h5py
import sys
import json
import numpy as np


class H5pyCli:

    def __init__(self, h5_filename):
        self.h5_filename = h5_filename
        self.f = h5py.File(sys.argv[1], 'r')
        self.dirs = []
        self.ver = "0.2"
        self.run()

    def simplify_classname(self, classname):
        return classname.split("'")[1]

    def get_pwd(self):
        if len(self.dirs) == 0:
            return "/"
        else:
            dirs = []
            for i in range(len(self.dirs)):
                dirs.append(self.dirs[i].name)
            

            # pwd = "/".join(dirs)
            # double / is confusing, just remove them
            #for i in range(1000):
            #    pwd = pwd.replace("//","/")
            pwd = dirs[-1]
            return pwd

    def get_curr_obj(self):
        if len(self.dirs) == 0:
            return self.f
        else:
            return self.dirs[-1]

    def ls(self, params):
        errors = ['ls: %s: No such attribute, dataset or group']
        curr_obj = self.get_curr_obj()

        ls_type = 'g'
        if len(params) > 0:
            if params[0] in curr_obj:
                curr_obj = curr_obj[params[0]]
            elif params[0] in curr_obj.attrs.keys():
                curr_obj = curr_obj.attrs[params[0]]
                ls_type = 'a'
            else:
                print(errors[0] % params[0])
                return

        curr_classname = self.simplify_classname(str(type(curr_obj)))
        if curr_classname == 'h5py._hl.dataset.Dataset':
            ls_type = 'd'

        if ls_type == 'g':
            print(".")
            print("..")
            keys = list(curr_obj.keys())
            for i in range(len(keys)):
                ob = curr_obj[keys[i]]
                classname = self.simplify_classname(str(type(ob)))
                if classname == "h5py._hl.group.Group":
                    print("g: %s" % keys[i])
                else:
                    print("d:", ob.name, classname)
            if "attrs" in dir(curr_obj):
               attr_keys = list(curr_obj.attrs.keys())
               for i in range(len(attr_keys)):
                   print("a: %s" % attr_keys[i])
        elif ls_type == 'a':
            print("%s %10d" % (params[0], len(curr_obj)))
        elif ls_type == 'd':
            print("d: %s %s" % (params[0], str(curr_obj.shape)))
   
    def cd(self, params):
        errors = ['cd: %s: No such group']
        if len(params) ==0:
            return
        curr_obj = self.get_curr_obj()
        if params[0] == ".":
            pass
        elif params[0] == "..":
            if len(self.dirs) > 0:
                del self.dirs[-1]
        else:
            keys = list(curr_obj.keys())
            groups = []
            for i in range(len(keys)):
                ob = curr_obj[keys[i]]
                classname = self.simplify_classname(str(type(ob)))
                if classname == "h5py._hl.group.Group":
                    groups.append(keys[i])
            if params[0] in groups:
                self.dirs.append(curr_obj[params[0]])
            else:
                print(errors[0] % params[0])

    def cat(self, params):
        errors = ['cat: %s: No such attribute']
        curr_obj = self.get_curr_obj()
        output_filename = ""
        if len(params)>1:
            op = "".join(params[1:]).strip()
            if op[0] == ">":
                output_filename = op[1:]

        if len(params) > 0:
            if params[0] in curr_obj:
                curr_obj = curr_obj[params[0]]
                classname = self.simplify_classname(str(type(curr_obj)))
                if classname == "h5py._hl.dataset.Dataset":
                    if output_filename != "":
                        np.savez(output_filename, data=np.array(curr_obj))
                    else:
                        print(np.array(curr_obj))
                else:
                    print(errors[0] % params[0])
            elif params[0] in curr_obj.attrs.keys():
                curr_obj = curr_obj.attrs[params[0]]
                if output_filename != "":
                    with open(output_filename, "w") as f:
                        f.write(curr_obj)
                else:
                    print(curr_obj)
            else:
                print(errors[0] % params[0])

    def pwd(self, params):
        print(self.get_pwd())

    def help(self, params):
        self.software_info()
        print('''
This command line interface mainly handles attribute, group and dataset of the hdf5 file. 
Following commands are defined internally.  Type `help' to see this list.

 cd [group]
    change directory/group
 cat [attr|dataset]
    display the specific attribute or dataset
 cat [attr|dataset] > [filename]
    save the specific attribute or dataset to an output file
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
''')

    def filename(self, params):
        print("filename: %s" % self.h5_filename)

    def software_info(self):
        print("h5py-cli v%s" % self.ver)
        self.filename([])

    def exit(self, params):
        sys.exit(0)

    def input(self):
        ps = "%s$ " % self.get_pwd()
        cmd = input(ps)
        # ugly implementation
        for i in range(100):
            cmd = cmd.replace(">"," > ")
            cmd = cmd.replace("  ", " ").replace("  "," ")
        return cmd

    def run(self):
        self.software_info()
        while True:
            cmd = self.input()
            cmd_name = cmd.strip().lower().split(" ")[0]
            params = cmd.strip().split(" ")[1:]

            # use reflection to replace the original if-else structure
            if cmd_name in ["cat", "cd", "help", "exit", "filename", "ls", "pwd"]:
                exec("self.%s(params)" % cmd_name)
            else:
                print("h5py-cli: %s: command not found" % cmd_name)

if __name__ == "__main__":
    hc = H5pyCli(sys.argv[1])

