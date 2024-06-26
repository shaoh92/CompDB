import os
import shutil
from rdkit import Chem, rdBase
from rdkit.Chem import rdMolTransforms
import math

# Disable RDKit warnings
rdBase.DisableLog('rdApp.warning')
rdBase.DisableLog('rdApp.error')

# Function to check if an atom is a transition metal
def is_transition_metal(atom):
    atomic_num = atom.GetAtomicNum()
    return 21 <= atomic_num <= 30 or 39 <= atomic_num <= 48 or 57 <= atomic_num <= 80 or 89 <= atomic_num <= 112

# Specify the directory containing the .mol files
directory_path = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates\\cs0c00111_si_001-coord'

# Create a new directory for hydride-migration-TS .mol files
new_directory_path = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates\\hydride-migration-TS'
os.makedirs(new_directory_path, exist_ok=True)

# Process each .mol file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".mol"):
    #if filename.endswith("TS2.mol"): # For testing with a specific file
        file_path = os.path.join(directory_path, filename)
        mol = Chem.MolFromMolFile(file_path, removeHs=False)

        if mol is not None:
            transition_metal_indices = [atom.GetIdx() for atom in mol.GetAtoms() if is_transition_metal(atom)] # Get indices of transition metal atoms
            hydrogen_indices = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'H'] # Get indices of hydrogen atoms
            carbon_indices = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'C']  # Get indices of carbon atoms

            conf = mol.GetConformer()
#Successfully improted the .mol file and got the indices of transition metal, hydrogen and carbon atoms.
                
        #Getting the index of transition metal in this molecule and save it in TM_index. 
        TM_index = None
        for atom in mol.GetAtoms():
            if is_transition_metal(atom):
                atom_index = atom.GetIdx()
                atom_type = atom.GetSymbol()
                #print(f"Atom index: {atom_index}, Atom type: {atom_type}") # Debug print
        
                if TM_index is None:
                    TM_index = atom_index  
                    #print(f"TM index: {TM_index}") # Debug print

        #Getting the index of the metal hydride in this molecule 
        M_hydride_index = None
        for h_index in hydrogen_indices:
            pos1 = conf.GetAtomPosition(TM_index)
            pos2 = conf.GetAtomPosition(h_index)
            distance = pos1.Distance(pos2)
            if 1.55 <= distance <= 1.75:
                saved_h_index = h_index  # Save the hydrogen index
                #print(f"M-H_distance: {distance}") # Debug print
                #print(f"h index: {h_index}") # Debug print
            # Get the bond between the hydrogen atom and the transition metal atom
                if M_hydride_index is None:
                    M_hydride_index = saved_h_index
                    #print(f"M_hydride index: {M_hydride_index}") # Debug print 

        # Define a list of transition metals
        transition_metals = ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
        
        # Getting the index of the M_carbon in this molecule 
        M_carbon_index = None
        for atom in mol.GetAtoms():
            if atom.GetSymbol() == 'C':
                # Check if the carbon atom is bonded to a transition metal
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() in transition_metals:
                        M_carbon_index = atom.GetIdx()
                        break
        
                # If M_carbon_index is found, break the loop
                if M_carbon_index is not None:
                    break
        #print(f"M_carbon index: {M_carbon_index}") # Debug print

        # Getting the index of the H_carbon in this molecule 
        H_carbon_index = None
        for atom in mol.GetAtoms():
            if atom.GetSymbol() == 'C':
                # Check if the carbon atom is bonded to a hydrogen atom and M_carbon
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() == 'H':
                        bond_length = rdMolTransforms.GetBondLength(conf, atom.GetIdx(), neighbor.GetIdx())
                        if 1.10 <= bond_length <= 1.80:
                            for second_neighbor in atom.GetNeighbors():
                                if second_neighbor.GetIdx() == M_carbon_index:
                                    H_carbon_index = atom.GetIdx()
                                    break

                # If H_carbon_index is found, break the loop
                if H_carbon_index is not None:
                    break

        # Print the H_carbon_index
        #print(f"H_carbon index: {H_carbon_index}")
                    
        # Check if all indices are not None
        if TM_index is None or M_hydride_index is None or H_carbon_index is None or M_carbon_index is None:
            print("One or more indices are None. Skipping this molecule.")
        else:
            # Your conditions go here
            print(f"TM index: {TM_index}, M_hydride index: {M_hydride_index}, H_carbon index: {H_carbon_index}, M_carbon index: {M_carbon_index}")            
#Successfully obtained the indices of the four atoms involved in the hydride migration TS. Tested with TS2.mol file.

        is_hydride_migration_TS = False
        condition1_M_C_C = False
        condition2_C_C_H = False
        condition3_C_H_M = False
        condition4_H_M_C = False
        angle_rad = 0
        angle_deg = 0

        # Check condition 1: is the M_C_C bond angle between 60 and 120 degrees?
        if TM_index is None or M_hydride_index is None or H_carbon_index is None or M_carbon_index is None:
            print("One or more indices are None. Skipping this molecule.")
        else:
            angle_rad = rdMolTransforms.GetAngleRad(conf, TM_index, M_carbon_index, H_carbon_index)
            #print(f"Angle: {angle_rad}") # Debug print
        # Convert to degrees
            angle_deg = math.degrees(angle_rad)  
        #print(f"Angle in degrees: {angle_deg}") # Debug print
            if 60 <= angle_deg <= 120:
                condition1_M_C_C = True
                #print(f"Condition 1 met with angle {angle_deg}")  # Debug print

        # Check condition 2: is the C_C_H bond angle between 60 and 120 degrees?
        if TM_index is None or M_hydride_index is None or H_carbon_index is None or M_carbon_index is None:
            print("One or more indices are None. Skipping this molecule.")
        else:
            angle_rad = rdMolTransforms.GetAngleRad(conf, M_carbon_index, H_carbon_index, M_hydride_index)
            #print(f"Angle: {angle_rad}") # Debug print
        # Convert to degrees
            angle_deg = math.degrees(angle_rad)  
        #print(f"Angle in degrees: {angle_deg}") # Debug print
            if 60 <= angle_deg <= 120:
                condition2_C_C_H = True
                #print(f"Condition 2 met with angle {angle_deg}")  # Debug print

        # Check condition 3: is the C_H_M bond angle between 60 and 120 degrees?
        if TM_index is None or M_hydride_index is None or H_carbon_index is None or M_carbon_index is None:
            print("One or more indices are None. Skipping this molecule.")
        else:        
            angle_rad = rdMolTransforms.GetAngleRad(conf, H_carbon_index, M_hydride_index, TM_index)
            angle_deg = math.degrees(angle_rad)  
            #print(f"Angle in degrees: {angle_deg}") # Debug print
            if 60 <= angle_deg <= 120:
                condition3_C_H_M = True
                #print(f"Condition 3 met with angle {angle_deg}")  # Debug print

        # Check condition 4: is the H_M-C bond angle between 60 and 120 degrees?
        if TM_index is None or M_hydride_index is None or H_carbon_index is None or M_carbon_index is None:
            print("One or more indices are None. Skipping this molecule.")
        else:
            angle_rad = rdMolTransforms.GetAngleRad(conf, M_hydride_index, TM_index, M_carbon_index)
            angle_deg = math.degrees(angle_rad)  
            #print(f"Angle in degrees: {angle_deg}") # Debug print
        if 60 <= angle_deg <= 120 or angle_deg == None:
            condition4_H_M_C = True
            #print(f"Condition 4 met with angle {angle_deg}")  # Debug print

        # Check if all conditions are met
        if condition1_M_C_C and condition2_C_C_H and condition3_C_H_M and condition4_H_M_C:
            is_hydride_migration_TS = True
        else:
            is_hydride_migration_TS = False

        print(f"Is {filename} a hydride migration TS? {is_hydride_migration_TS}")

        # if condition0_C_H and condition1_M_H and condition2_M_C and condition3_C_M_H_angle:
        #     is_hydride_migration_TS = True
        #     print(f"The molecule {filename} is a hydride-migration-TS.")  # This should be printed if everything is correct
        #     # Copy the .mol file to the new directory
        #     try:
        #         shutil.copy(file_path, new_directory_path)
        #         #print(f"Successfully copied {filename} to {new_directory_path}.")
        #     except Exception as e:
        #         print(f"Failed to copy {filename} to {new_directory_path}. Error: {e}")

