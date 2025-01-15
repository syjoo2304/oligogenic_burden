#!/bin/sh

# Set reference paths and tools
REF="/home/syjoo/REF/Human/hg19/hg19_vgatk/v0/Homo_sapiens_assembly19.fasta"
PICARD="/opt/picard/2.25.6/build/libs/picard.jar"
DBSNP="/home/syjoo/REF/Human/hg19/hg19_vgatk/v0/Homo_sapiens_assembly19.dbsnp138.vcf"

# Function to process one sample
batch1_gatk() {
    local sample_name=$1
    local fastq1="${sample_name}_1.fastq.gz"
    local fastq2="${sample_name}_2.fastq.gz"

    echo "Step 1-1/3: BWA and samtools"
    bwa mem -M -t 2 \
        -R "@RG\tID:YUHL\tSM:${sample_name}\tLB:HiSeq\tPL:ILLUMINA" \
        "$REF" \
        "$fastq1" \
        "$fastq2" | \
    samtools view -b -h -o "${sample_name}.bam" -

    echo "Step 1-2/3: SortSam"
    java -Xmx7g -jar "$PICARD" SortSam \
        I="${sample_name}.bam" \
        O="${sample_name}.sort.bam" \
        VALIDATION_STRINGENCY=LENIENT \
        SORT_ORDER=coordinate \
        MAX_RECORDS_IN_RAM=3000000 \
        CREATE_INDEX=true

    echo "Step 1-3/3: MarkDuplicates"
    java -Xmx7g -jar "$PICARD" MarkDuplicates \
        I="${sample_name}.sort.bam" \
        O="${sample_name}.sort.dup.bam" \
        METRICS_FILE="${sample_name}.marked_dup_metrics.txt"

    echo "Step 2-1/2: BaseRecalibrator"
    gatk --java-options "-Xmx7g" BaseRecalibrator \
        -I "${sample_name}.sort.dup.bam" \
        -R "$REF" \
        --known-sites "$DBSNP" \
        -O "${sample_name}.recal_data.table"

    echo "Step 2-2/2: Apply BQSR"
    gatk --java-options "-Xmx7g" ApplyBQSR \
        -I "${sample_name}.sort.dup.bam" \
        -R "$REF" \
        --bqsr-recal-file "${sample_name}.recal_data.table" \
        -O "${sample_name}.sort.dup.bqsr.bam"

    echo "Step 3-1/1: Variant calling by HaplotypeCaller"
    gatk --java-options "-Xmx7g" HaplotypeCaller \
        -I "${sample_name}.sort.dup.bqsr.bam" \
        -R "$REF" \
        -ERC GVCF \
        -O "${sample_name}.g.vcf.gz"

}

# Process all _1.fastq.gz files in the current directory
for fq1 in *_1.fastq.gz; do
    sample_name=$(basename "$fq1" _1.fastq.gz)
    echo "## Processing: $sample_name"
    batch1_gatk "$sample_name"
done
