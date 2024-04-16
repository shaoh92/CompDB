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
            is_hydride_migration_TS = False
            condition0_C_H = False
            condition1_M_H = False
            condition2_M_C = False
            condition3_C_M_H_angle = False

        for carbon_index in carbon_indices:
            for h_index in hydrogen_indices:
                pos1 = conf.GetAtomPosition(carbon_index)
                pos2 = conf.GetAtomPosition(h_index)
                distance = pos1.Distance(pos2)
                if 1.10 <= distance <= 1.50:
                    condition0_C_H = True
                    print(f"Condition 0 met with carbon index {carbon_index} and H index {h_index}")
                    break

        for tm_index in transition_metal_indices:
            for h_index in hydrogen_indices:
                pos1 = conf.GetAtomPosition(tm_index)
                pos2 = conf.GetAtomPosition(h_index)
                distance = pos1.Distance(pos2)
                if 1.55 <= distance <= 1.75:
                    condition1_M_H = True
                    saved_h_index = h_index  # Save the hydrogen index
                    saved_tm_index = tm_index  # Save the transition metal index
                    print(f"Condition 1 met with TM index {tm_index} and H index {h_index}")
                    break
            if condition1_M_H:  # Check condition1_M_H here
                for carbon_index in carbon_indices:
                    pos1 = conf.GetAtomPosition(tm_index)
                    pos2 = conf.GetAtomPosition(carbon_index)
                    distance = pos1.Distance(pos2)
                    if 2.10 <= distance <= 2.25:
                        condition2_M_C = True
                        saved_carbon_index = carbon_index  # Save the carbon index
                        print(f"Condition 2 met with TM index {tm_index} and C index {carbon_index}")  # Debug print
                        break
            if condition0_C_H and condition1_M_H and condition2_M_C:  # Check both conditions here
                tm_index = saved_tm_index
                h_index = saved_h_index
                carbon_index = saved_carbon_index
                # Calculate the angle in radians
                angle_rad = rdMolTransforms.GetAngleRad(conf, carbon_index, tm_index, h_index)
                # Convert to degrees
                angle_deg = math.degrees(angle_rad)  
                if 70 <= angle_deg <= 100:
                    condition3_C_M_H_angle = True
                    print(f"Condition 3 met with angle {angle_deg}")  # Debug print
                    break  # Break out of the loop over transition_metal_indices

        if condition0_C_H and condition1_M_H and condition2_M_C and condition3_C_M_H_angle:
            is_hydride_migration_TS = True
            print(f"The molecule {filename} is a hydride-migration-TS.")  # This should be printed if everything is correct
            # Copy the .mol file to the new directory
            try:
                shutil.copy(file_path, new_directory_path)
                #print(f"Successfully copied {filename} to {new_directory_path}.")
            except Exception as e:
                print(f"Failed to copy {filename} to {new_directory_path}. Error: {e}")

