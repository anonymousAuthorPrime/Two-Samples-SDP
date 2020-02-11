# Two-Samples-SDP
Code and Dual Variables for "More Revenue from Two Samples via Factor Revealing SDPs"

# Instructions to Run the Code
For the base case with n = 100, rho = 1.08, eps = 0.01, a machine with at least 200 GB memory is needed. Such machines can be found in AWS servers. The command then is:

```
python3.5 ./source/reserves.py -n 100 -rel 1.08 -iopt (i*) -mi 20000 -log
```

where (i*) corresponds to the hyperparameter of the optimization and can take values in [49, 99], otherwise the result will be infeasible as expected. After the execution the files that re descriped below will be produced and saved in "./source/log/mathematica" folder. The corresponding id in the beginning of the filenames will be printed in stdout at the end of the execution.

Instances with n <= 32 require less than 16 GB memory and can be used for checking the validity of the code.

# Instructions to Read Dual Certificates

The files in the "./DualCertificates" folder have the form.

```
(id)_(variable).dat
```

In this folder the (id) corresponds to the value of the hyperparameter i* and as we can see takes values from 49 to 98, because 99 is infeasible.

The term (variable) can take the following values. We are sorry that the _notation is different with the paper_ and hence confusing.

## Parameters:
**"b":** vector with the objective of the PRIMAL

**"w":** vector with the values of the finite sequence (rho^i)_i

## Primal Values:
**"x":** tensor with the primal solution. Remark! It has size (n + 3) choose 3, not n^3, as explained in the paper.

## Dual Values:
**"d1":** dual values for the constraints f_{i, j, k} >= 0

**"d2":** dual value for the constraint (sum)_{i, j, k} f_{i, j, k} = 1

**"iopt":** value of i* (sorry for the confusion with the paper where iopt is used for something else)

**"o":** dual values for optimality constraints

**"r":** dual values for regularity constraints

**"p":** dual values for psd constraints (see SCS for more details)

## Ad-Hoc Values
The tensor "x", for simplicity reasons has one more dimension, i.e. instead of characterizing the values in the intervals [rho^i, rho^(i + 1)] we use one more dimension. Then we need to add the constraint (sum)_{i, j} x_{0, i, j} = 0.

**"d3":** dual values for the aforementioned ad-hoc constraints.
