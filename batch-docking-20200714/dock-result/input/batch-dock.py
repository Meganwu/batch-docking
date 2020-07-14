#!/usr/bin/env python
#
#
#
#  Author  Nian Wu   data: 2020-7-14
# 
#  It's a script to do a batch process for docking. If you utilize autodock to implement batch_dock, while vina to implement batch_vina.  

if __name__ == '__main__':
    import sys
    import getopt
    import os
    from subprocess import call
    py_path = sys.executable

    def batch_dock(receptor,ligand,npts="60,60,60",gridcenter="-1.903,6.296,13.409"):
        pdb_recep=receptor   #pdb file
        pdb_ligand=ligand    #pdb file
        n_recep=pdb_recep.split('.')[0]
        n_recep_qt=n_recep+'.pdbqt'
        n_lig=pdb_ligand.split('.')[0]
        n_lig_qt=n_lig+'.pdbqt'
        namegpf=n_lig+'_'+n_recep+'.gpf'
        namedpf=n_lig+'_'+n_recep+'.dpf'
        os.system('pythonsh prepare_ligand4.py -l %s' % pdb_ligand)
        os.system('pythonsh prepare_receptor4.py -r %s' % pdb_recep)
        os.system('pythonsh prepare_gpf4.py -l %s -r  %s -p npts=%s -p gridcenter=%s -o %s' % (n_lig_qt, n_recep_qt, npts, gridcenter, namegpf))
        os.system('pythonsh prepare_dpf4.py -l %s -r  %s -o %s' % (n_lig_qt, n_recep_qt, namedpf))
        os.system('autogrid4 -p %s' % namegpf)
        os.system('autodock4 -p %s' % namedpf)

    def batch_vina(receptor,ligand,confile):
        pdb_recep=receptor   #pdb file
        pdb_ligand=ligand    #pdb file
        grid_parameter=confile   # .conf file
        n_recep=pdb_recep.split('.')[0]
        n_recep_qt=n_recep+'.pdbqt'
        n_lig=pdb_ligand.split('.')[0]
        n_lig_qt=n_lig+'.pdbqt'
        out_qt=n_lig+n_recep+'.pdbqt'
        out_txt=n_lig+n_recep+'-out.txt'
        os.system('pythonsh prepare_ligand4.py -l %s' % pdb_ligand)
        os.system('pythonsh prepare_receptor4.py -r %s' % pdb_recep)
        os.system('vina --config %s --ligand %s --out result-vina-final/%s --log result-vina-final/%s' % (grid_parameter, n_lig_qt, out_qt, out_txt))
        cmd="""energy=`grep "   1    "  result-vina-final/%s`; 
               a=%s;
               echo $a  $energy >> energy.txt;""" % (out_txt, n_lig)
        call(cmd, shell=True)

    def usage():
        "Print helpful, accurate usage statement to stdout."
        print ("""Print: -P "dock"  or  "vina" """)
        print ("""Usage: python batch_dock.py -P dock  -r receptor -l ligand -n "60,60,60"  -g "-1.903,6.296,13.409" """)
        print ("Usage: python batch_dock.py -P vina  -r receptor -l ligand -c confile")
        print ("Print: Description of command...")
        print ("Print: -r   receptor_filename ")
        print ("Print:  supported file types include pdb,mol2,pdbq,pdbqs,pdbqt, possibly pqr,cif")
        print ("Print:  -l   ligand_filename ")
        print ("""Print -n   number of grids along the x, y, z direction of box, example: "60,60,60" """)
        print ("""Print -g   gridcenter, example: "-1, -2, -3" """)
        print ("Print  -c   .conf file for vina")



# process command arguments
    try:
        opt_list, args = getopt.getopt(sys.argv[1:], 'r:l:n:g:c:P:')

    except getopt.GetoptError as msg:
        print ('batch_dock.py: %s' % msg)
        usage()
        sys.exit(2)

#'r:vo:A:Cp:U:eMh'
    for o, a in opt_list:
        if o in ('-P', '--P'):
            program = a       #    P "dock" or "vina"
        if o in ('-r', '--r'):
            receptor = a      #    print 'set receptor_filename to ', a
        if o in ('-l', '--l'):
            ligand = a        #    print 'set ligand_filename to ', a
        if o in ('-n', '--n'):
            npts = a          #    print 'set npts to (multiply 0.375 angstrom)', a
        if o in ('-g', '--g'):
            gridcenter = a    #    print 'set gridcenter to ', a
        if o in ('-c', '--c'):
            grid_parameter = a
         

    list=os.listdir('.')
    ligands=[i for i in list if i.split('.')[-1]=='pdb']
    ligands.remove(receptor)
    os.system('mkdir result-vina-final')
    if program=="dock":
      for i in  ligands:
         batch_dock(receptor, i, npts, gridcenter)
    if program=="vina":
      for i in  ligands:
         batch_vina(receptor, i, grid_parameter) 








# To execute  this command type:
# python batch-dock.py -P dock  -r crbn.pdb  -n "60,60,60"   -g "-1.903,6.296,13.409" 
# python batch-dock.py -r crbn.pdb -c crbn.conf  -P vina

