# Tutorial to using the Nuvolos Collector and Grader tool

This is a quick guide to using the Nuvolos Collector in combination with the `otter-grader` package.

## Setting up an otter test project

In order to test functionality of the Nuvolos Assign-Grade-Handback workflow, we suggest to take the following steps.

1. Obtain the otter tutorial

To get the otter tutorial, open a JupyterLab terminal and hit
```
wget https://otter-grader.readthedocs.io/en/latest/_static/tutorial.zip
```

2. Modify `demo.ipynb`

The `demo.ipynb` file that is provided by `otter` is not completely compatible with Nuvolos. The reason is that the demo assumes that the environment has a window system - this is not true in Nuvolos. In order to fix this issue, instead of

```
%matplotlib inline
```

Make sure to have:
```
import matplotlib
matplotlib.use('Agg')
```

3. Run `otter assign`

Following the tutorial steps, you need to run

```
otter assign demo.ipynb dist --v1
```
Which creates a `dist` directory in which you have the necessary files for grading and sharing.

4. Create an Assignment on Nuvolos

Grab the file `dist/student/demo.ipynb` and put it in a folder someplace where you would share it as an assignment. For example we will assumed that the files is moved to `/files/assignment_1`.

* Stage the folder `assignment_1` on the Nuvolos UI.
* Create an assignment from the folder. 
    * We assume henceforth that you named the assignment `first_assignment`. 
* Set a deadline.

5. Collect student hand-ins

Once the students started handing in, you will find handins under `/files/assignment-review/...`. After the deadline passes, no further hand-ins are possible which means that the assignment is ready to be collected. We assume that you have named your as

To collect, you need to type the following command in the terminal:

```
nvcollect collect --assignment_name "first_assignment" --assignment_folder assignment_1 --target_folder /files/test_collect
```

This tells the collect tool to gather from all students whatever is contained in the `assignment_1` folder in the first assignment and the collected files should be placed under `/files/test_collect`.

The directory structure will be as such:

```
/files/test_collect
+-- nvcollect_manifest.json
+-- single_user_inst_<code1>
|   +-- ...
+-- single_user_inst_<code2>
|   +-- ...

```

6. Grade hand-ins

##
