#!/bin/sh

# Variables
TMP_DIR="[path_to_output]/TMP"
OUTPUT_DIR="[path_to_output]"
THREADS=8
MEMORY="64g"
MAX_JOBS=4  # Number of parallel jobs
REF="[path_to_ref]/Homo_sapiens_assembly19.fasta"
sample_name="early"
#Please refer to the example file: "Proband.txt". 
proband="Proband.txt"

# Load required modules
module load gatk

# Create output directory if it doesn't exist
mkdir -p "${TMP_DIR}"

# Function to run GATK HaplotypeCaller for a given chromosome
run_dbimport() {

    local CHROMOSOME=$1
    local OUTPUT_VCF="${OUTPUT_DIR}/output_chr${CHROMOSOME}.vcf"
    
    echo "Processing chromosome: ${CHROMOSOME}"

    gatk --java-options "-Xmx${MEMORY}" GenomicsDBImport \
         --batch-size 50 --tmp-dir "${TMP_DIR}" \
         --intervals "chr${CHROMOSOME}" \
         --sample-name-map "${proband}" \
         --genomicsdb-workspace-path "chr${CHROMOSOME}"

    gatk --java-options "-Xmx${MEMORY}" GenotypeGVCFs \
         --tmp-dir "${TMP_DIR}" \
         -R "${REF}" \
         -V gendb://"chr${CHROMOSOME}" -O "chr${CHROMOSOME}".Genotype.vcf

    if [ $? -eq 0 ]; then
        echo "Successfully finished chromosome: ${CHROMOSOME}"
    else
        echo "Error processing chromosome: ${CHROMOSOME}" >&2
    fi
}

export -f run_dbimport  # Export function to be used in xargs
export OUTPUT_DIR
export TMP_DIR
export THREADS
export MEMORY
export sample_name
export REF
export proband

# List of chromosomes
# List of chromosomes
CHROMOSOMES=$(seq 1 22)
##to fix the primary error, block the command below, temporally
#CHROMOSOMES="${CHROMOSOMES} X Y"

## Run parallel jobs using xargs, limiting to MAX_JOBS at a time
echo "${CHROMOSOMES}" | tr ' ' '\n' | xargs -n 1 -P ${MAX_JOBS} -I {} bash -c 'run_dbimport "$@"' _ {}

## Generate the list of input VCF files (chr1 to chr19, chrX, chrY)
ls ${OUTPUT_DIR}/chr{1..22}.Genotype.vcf ${OUTPUT_DIR}/chrX.Genotype.vcf ${OUTPUT_DIR}/chrY.Genotype.vcf > ${OUTPUT_DIR}/sample_list.txt

## Run the GATK MergeVcfs command
gatk --java-options "-Xmx${MEMORY}" \
    MergeVcfs \
    --INPUT ${OUTPUT_DIR}/sample_list.txt \
    --OUTPUT ${OUTPUT_DIR}/${sample_name}.merged.vcf

## Step 2: Sort the merged VCF file by chromosome
gatk --java-options "-Xmx${MEMORY}" \
    SortVcf \
    --INPUT ${OUTPUT_DIR}/${sample_name}.merged.vcf \
    --OUTPUT ${OUTPUT_DIR}/${sample_name}.sorted.vcf
