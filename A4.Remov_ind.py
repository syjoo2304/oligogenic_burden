import os
import glob

# Define the path to the directory containing the VCF files
PATH = '/home/syjoo/test/Control_HL/Control'

def load_ids(file_path):
    """
    Load IDs from a file, one ID per line.
    """
    with open(file_path, 'r') as f:
        return [line.strip().split('\t')[0] for line in f]

def process_vcf_files(path, ids_to_remove):
    """
    Process VCF files by removing specified individuals.

    Parameters:
        path (str): Directory containing VCF files.
        ids_to_remove (list): List of IDs to be removed.
    """
    # Get a list of VCF files in the directory
    vcf_files = [file for file in os.listdir(path) if file.endswith(".plink.vcf")]

    for vcf_file in vcf_files:
        print(f"Processing {vcf_file}...")
        name = vcf_file.split('.plink.vcf')[0]
        
        if name == 'Total_3_f':
            print(f"Removing individuals from {name}...")
            remove_cmd = (
                f"vcftools {' '.join(f'--remove-indv {id}' for id in ids_to_remove)} "
                f"--vcf {os.path.join(path, vcf_file)} --recode --out {os.path.join(path, name)}.remov_sample.vcf"
            )
            os.system(remove_cmd)

def main():
    # File paths
    king_file = 'Total_3.king.kin0'
    solved_file = 'YUHL_Solved.txt'

    # Load IDs from files
    try:
        with open(king_file, 'r') as f:
            f.readline()  # Skip header
            ids_from_king = [line.strip().split('\t')[1] for line in f if line.strip().split('\t')[1] != 'N058']
    except FileNotFoundError:
        print(f"Error: File '{king_file}' not found.")
        return

    ids_from_solved = load_ids(solved_file)
    predefined_ids = [
        'TN1512D1217_1_YUHL3-11', 'YUHL-31-32', 'YUHL-1-11', '102-11_1', 'YUHL166-21', 
        'YUHL338-12', 'YUHL350-12', 'YUHL-36-11', 'YUHL398-12', 'YUHL421-12', 
        'YUHL_208-12', 'YUHL_312-31', 'YUHL_48_12', 'YVHL_153-22', 's23', 
        'sample_544-12', 'YUHL256-12', 'YUHL325-22', 'YUHL326-11', 'YUHL_339-22', 
        'YUHL_72_31', 'yuhl_194-11'
    ]

    # Combine all IDs into a single set
    total_ids_to_remove = set(ids_from_king + ids_from_solved + predefined_ids)
    print(f"Total IDs to remove: {len(total_ids_to_remove)}")
    print(total_ids_to_remove)

    # Process VCF files
    process_vcf_files(PATH, total_ids_to_remove)

if __name__ == "__main__":
    main()
