from io import StringIO
import re

def CifChopper(fhandle, PFamStart, PFamEnd):
    """
    Convert a structure in mmCIF format to PDB format, and cuts the structure
    ------
    This function has been created by adjusting the code available in 
    https://f1000research.com/articles/7-1961
    """
    _a = "{:6s}{:5d} {:<4s}{:1s}{:3s} {:1s}{:4d}{:1s}   {:8.3f}{:8.3f}{:8.3f}"
    _a += "{:6.2f}{:6.2f}      {:<4s}{:<2s}{:2s}\n"

    in_section, read_atom = False, False

    label_pos = 0
    labels = {}
    empty = set(('.', '?'))

    prev_model = None
    atom_num = 0
    serial = 0  # do not read serial numbers from mmCIF. Wrong in multi-models.

    model_data = []  # store atom data to account for multi-model files
    for line in fhandle:
        if line.startswith('loop_'):  # start of section
            in_section = True

        elif line.startswith('#'):  # end of section
            in_section = False
            read_atom = False

        elif in_section and line.startswith('_atom_site.'):  # ATOM/HETATM
            read_atom = True
            labels[line.strip()] = label_pos
            label_pos += 1

        elif read_atom and line.startswith(('ATOM', 'HETATM')):  # convert
            fields = re.findall(r'[^"\s]\S*|".+?"', line)  # find enclosed ''

            # Pick fields, giving preference to auth to match PDBs
            # http://mmcif.wwpdb.org/docs/pdb_to_pdbx_correspondences.html
            model_no = fields[labels.get('_atom_site.pdbx_PDB_model_num')]
            if prev_model != model_no:  # first line will trigger
                prev_model = model_no
                model_data.append([])
                serial = 0

            record = fields[labels.get('_atom_site.group_PDB')]

            # serial = int(fields[labels.get('_atom_site.id')])
            serial += 1

            fid = labels.get('_atom_site.auth_atom_id')
            if fid is None:
                fid = labels.get('_atom_site.label_atom_id')
            atname = fields[fid]

            element = fields[labels.get('_atom_site.type_symbol')]
            if element in empty:
                element = ' '

            # handle atom name
            if atname[0] == '"' and atname[-1] == '"':
                atname = atname[1:-1]

            if len(atname) < 4 and atname[0].isalpha() and len(element) < 2:
                atname = ' ' + atname  # pad

            altloc = fields[labels.get('_atom_site.label_alt_id')]
            if altloc in empty:
                altloc = ' '

            fid = labels.get('_atom_site.auth_comp_id')
            if fid is None:
                fid = labels.get('_atom_site.label_comp_id')
            resname = fields[fid]

            fid = labels.get('_atom_site.auth_asym_id')
            if fid is None:
                fid = labels.get('_atom_site.label_asym_id')
            chainid = fields[fid]

            fid = labels.get('_atom_site.auth_seq_id')
            if fid is None:
                fid = labels.get('_atom_site.label_seq_id')
            resnum = int(fields[fid])
       
            if resnum > PFamEnd:
                break

            icode = fields[labels.get('_atom_site.pdbx_PDB_ins_code')]
            if icode in empty:
                icode = ' '

            x = float(fields[labels.get('_atom_site.Cartn_x')])
            y = float(fields[labels.get('_atom_site.Cartn_y')])
            z = float(fields[labels.get('_atom_site.Cartn_z')])
            occ = float(fields[labels.get('_atom_site.occupancy')])
            bfactor = float(fields[labels.get('_atom_site.B_iso_or_equiv')])

            charge = fields[labels.get('_atom_site.pdbx_formal_charge')]
            try:
                charge = charge
            except ValueError:
                charge = '  '

            segid = chainid

            atom_line = _a.format(record, serial, atname, altloc, resname,
                                  chainid, resnum, icode, x, y, z, occ, bfactor,
                                  segid, element, charge)

            atom_num += 1

            # Check if structure is too large
            if resnum>= PFamStart:
                model_data[-1].append(atom_line)

    # Check if multi-model
    model_data[-1].append("{:<80s}\n".format("END"))
    
    return "".join(model_data[0] )
