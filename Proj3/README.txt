Make sure you've downloaded minizinc and added to your PATH.

You may want to add the following command  to your .bashrc:
export PATH=${HOME}/MiniZincIDE-2.3.2-bundle-linux/bin:${PATH}
(assuming that MiniZincIDE-2.3.2.bundle-linux is in your home directory.)

The stub assumes that the bulk of the constraints and definitions is in
main.mzn and the printing of the results in prn.mzn, but you are free to choose
a different way of doing things.

---
Mikolas 15 November 2019
