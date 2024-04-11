# Variable Assigner

The Variable Assigner node serves as a hub for collecting branch outputs within the workflow, ensuring that regardless of which branch is taken, the output can be referenced by a single variable. The output can subsequently be manipulated by nodes downstream.

<figure><img src="../../../.gitbook/assets/output (3).png" alt=""><figcaption></figcaption></figure>

Variable Assigner supports multiple types of output variables including `String`,`Number`, `Object`, and `Array`. Given the specified output type, you may add input variables from the dropdown list of variables to the node. The list of variables is derived from previous branch outputs and autofiltered based on the specified type.

<figure><img src="../../../.gitbook/assets/output (4).png" alt="" width="375"><figcaption></figcaption></figure>

Variable Assigner gives a single `output` variable of the specified type for downstream use.
