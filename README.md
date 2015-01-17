# mae221
Python with Pithy for Princeton University's MAE 221 Thermodynamics

January 2015

This repo includes two Python scripts I used for the class's final power plant design analysis project.

The script 'jhyates_finalproject' simulates the power plant, with thirteen initial input states (two temperatures, seven pressures, and four mass flow fractions). It calculates thermodynamic properties and the conomic feasibility of such a plant, based on assumptions made in class. It also yields three plots: T-s (Entropy vs. Temperature), P-v (Specific Volume vs. Pressure), and P-h (Enthalpy vs. Pressure) diagrams for the various states of the water control volume within the power plant cycle. The script 'jhyates_fdpfunction' has similar functionality in that it calculates the thermodynamic properties of the given power plant cycle, but is meant to see the sensitivity of those properties to varying inputs. It's much more rough; you have to get in there and modify the input variables and the ranges over which they can vary in value manually. However, it did its job for the assignment. The script produces plots of heat transfer in and out of the cycle, work into the cycle, and the thermal efficiency and backwork ratio of the cycle. A set of these plots for the current set of inputs, for the interested, is located at http://imgur.com/a/HmfQd.