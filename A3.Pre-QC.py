
import os

def preQC(i):
    """
    Performs a series of preprocessing and filtering steps on the given VCF file.
    
    Parameters:
        i (str): The input VCF file path.
    """
    try:
        # Filtering step 01 -- variant quality score
        os.system(f'bcftools norm -m -any {i} -o norm.vcf.gz')
        os.system('bcftools view -i "QUAL >=100 & F_PASS(GQ>20) > 0.95" norm.vcf.gz > norm2.vcf.gz')
        
        # Merging step -- If VCFs are already merged (YUHL+Control), skip this step
        # os.system('vcf-merge ' + " ".join(ID) + ' |bgzip -c > Total.vcf.gz')
        
        # Filtering step 02 -- Only multiallelic variants allowed
        os.system('bcftools view --max-alleles 2 norm2.vcf.gz > Total2.vcf.gz')
        
        # Filtering step 03 -- geno, HWE (Hardy-Weinberg Equilibrium)
        os.system('/home/syjoo/program/plink2 --vcf Total2.vcf.gz --geno 0.05 --hwe 0.001 --out Total.plink --make-bed --const-fid')
        
        # Pre-filtering step 01 -- kinship
        os.system('/home/syjoo/program/plink2 --bfile Total.plink --make-king-table --king-table-filter 0.084 --out Total.king')
        
        # Pre-filtering step 02 -- Exporting PLINK format output to VCF
        os.system('/home/syjoo/program/plink2 --bfile Total.plink --out YUHL.plink --recode vcf')
        
        # Pre-filtering step 03 -- Adjusting VCF header due to incompatibility between PLINK2 and VCFtools 1.4
        os.system('sed "s/^##fileformat=VCFv4.3/##fileformat=VCFv4.2/" YUHL.plink.vcf > YUHL.plink2.vcf')
        
        # Filtering step 04 -- Kinship
        #os.system('python A.Remov_ind.py')
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Input prompt for the user to specify the file
    i = input("Enter the path to the VCF file: ").strip()
    
    # Check if the file exists before proceeding
    if not os.path.isfile(i):
        print(f"Error: File '{i}' does not exist. Please provide a valid file path.")
        return
    
    # Run the preQC function
    preQC(i)

if __name__ == "__main__":
    main()
