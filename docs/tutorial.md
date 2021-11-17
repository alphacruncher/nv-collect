# Tutorial to using the Nuvolos Collector and Grader tool

This is a quick guide to using the Nuvolos Collector in combination with the `otter-grader` package.

## Setting up an otter test project

In order to test functionality of the Nuvolos Assign-Grade-Handback workflow, we suggest to take the following steps.

1. Obtain the otter tutorial

To get the otter tutorial, open a JupyterLab terminal and hit
```
wget https://otter-grader.readthedocs.io/en/latest/_static/tutorial.zip
unzip tutorial.zip
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

In order to grade hand-ins we need to use the `autograder.zip` file generated in Step 3. To grade all collected assignments:

```
nvcollect otter-grade --source_folder /files/test_collect --autograder_location /files/otter-test/dist/autograder/autograder.zip --relative_path demo.ipynb
```

Observe the following:

* `source_folder` is the same folder as provided as `target_folder` to the collection command.
* You have to provide the absolute path of the `autograder.zip` file that belongs to the particular notebook file you want to grade.
* The `relative_path` parameter tells the tool where to look for in each student submission directory for the notebook file that needs to be graded.

As an outcome of the grading, you get the following new items in the `source_folder`:
* A `grade.json` file which contains exhaustive information about the evaluation of the tests.
* A `grade.csv` file which contains the score of each student.
* A `grade.csv` file in each student folder  which contains the score of the student.

7. Handing back

You might want to add additional artifacts to each students folders (either manually or programmatically). Once you are done with this, you can push back the results of the grading with the command

```
nvcollect handback --source_folder /files/test_collect
```

* Notice that the `source_folder` here is the same folder to which we collected and then in which the grading process ran.

