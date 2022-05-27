import h5py
import sys
import json
import numpy as np

def simplify_classname(classname):
    return classname.split("'")[1]

class H5pyCli:
    def __init__(self, h5Filename):
        self.h5Filename = h5Filename
        self.f = h5py.File(sys.argv[1], 'r')
        self.dir = []
        self.ver = "0.1"
        self.run()

    def get_pwd(self):
        if len(self.dir) == 0:
            return ""
        else:
            dirs = []
            for i in range(len(self.dir)):
                dirs.append(self.dir[i].name)
            pwd = "/".join(dirs)
            for i in range(1000):
                pwd = pwd.replace("//","/")
            return pwd

    def get_curr_obj(self):
        if len(self.dir) == 0:
            return self.f
        else:
            return self.dir[-1]

    def ls(self, params):
        errors = ['ls: %s: No such attribute, dataset or group']
        currObj = self.get_curr_obj()

        lsType = 'g'
        if len(params) > 0:
            if params[0] in currObj:
                currObj = currObj[params[0]]
            elif params[0] in currObj.attrs.keys():
                currObj = currObj.attrs[params[0]]
                lsType = 'a'
            else:
                print(errors[0] % params[0])
                return

        currClassname = simplify_classname(str(type(currObj)))
        if currClassname == 'h5py._hl.dataset.Dataset':
            lsType = 'd'

        if lsType == 'g':
            print(".")
            print("..")
            keys = list(currObj.keys())
            for i in range(len(keys)):
                ob = currObj[keys[i]]
                classname = simplify_classname(str(type(ob)))
                if classname == "h5py._hl.group.Group":
                    print("g: %s" % keys[i])
                else:
                    print("d:", ob.name, classname)
            if "attrs" in dir(currObj):
               attrKeys = list(currObj.attrs.keys())
               for i in range(len(attrKeys)):
                   print("a: %s" % attrKeys[i])
        elif lsType == 'a':
            print("%s %10d" % (params[0], len(currObj)))
        elif lsType == 'd':
            print("d: %s %s" % (params[0], str(currObj.shape)))
   
    def cd(self, params):
        errors = ['cd: %s: No such group']
        currObj = self.get_curr_obj()
        if params[0] == ".":
            pass
        elif params[0] == "..":
            if len(self.dir) > 0:
                del self.dir[-1]
        else:
            keys = list(currObj.keys())
            groups = []
            for i in range(len(keys)):
                ob = currObj[keys[i]]
                classname = simplify_classname(str(type(ob)))
                if classname == "h5py._hl.group.Group":
                    groups.append(keys[i])
            if params[0] in groups:
                self.dir.append(currObj[params[0]])
            else:
                print(errors[0] % params[0])

    def cat(self, params):
        errors = ['cat: %s: No such attribute']
        currObj = self.get_curr_obj()
        outputFilename = ""
        if len(params)>1:
            op = "".join(params[1:]).strip()
            if op[0] == ">":
                outputFilename = op[1:]

        if len(params) > 0:
            if params[0] in currObj:
                currObj = currObj[params[0]]
                classname = simplify_classname(str(type(currObj)))
                if classname == "h5py._hl.dataset.Dataset":
                    if outputFilename != "":
                        np.savez(outputFilename, data=np.array(currObj))
                    else:
                        print(np.array(currObj))
                else:
                    print(errors[0] % params[0])
            elif params[0] in currObj.attrs.keys():
                currObj = currObj.attrs[params[0]]
                if outputFilename != "":
                    with open(outputFilename, "w") as f:
                        f.write(currObj)
                else:
                    print(currObj)
            else:
                print(errors[0] % params[0])

    def pwd(self):
        print(self.get_pwd())

    def run(self):
        print("h5py-cli v%s" % self.ver)
        print("author: Hu, Ying-Hao (hyinghao@hotmail.com)")
        print("filename: %s" % self.h5Filename)
        while True:
            PS = "%s$ " % self.get_pwd()
            cmd = input(PS)
            firstCmd = cmd.strip().lower().split(" ")[0]
            params = cmd.strip().split(" ")[1:]
            if firstCmd == "exit":
                break
            elif firstCmd == "ls":
                self.ls(params)
            elif firstCmd == "pwd":
                self.pwd()
            elif firstCmd == "cd":
                self.cd(params)
            elif firstCmd == "cat":
                self.cat(params)
            else:
                print("h5py-cli: %s: command not found" % firstCmd)


if __name__ == "__main__":
    hc = H5pyCli(sys.argv[1])
