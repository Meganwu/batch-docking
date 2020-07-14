# batch-docking

The batch-dock.py is a script for batch processing of docking based on autodock and vina softwares, written by Nian Wu, on 14th, July, 2020.

The commands can be implemented to obtain results in examples.
#  autodock example
python batch-dock.py -P dock  -r crbn.pdb  -n "60,60,60"   -g "-1.903,6.296,13.409" 
#  dock-vina example
python batch-dock.py -r crbn.pdb -c crbn.conf  -P vina
