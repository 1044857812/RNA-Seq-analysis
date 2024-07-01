# RNA-Seq
Analysis code for transcriptome data

## Data processing

### 1.QC

    fastp -w 8 -i sample1/sample1_r1.fq.gz -I sample1/sample1_r2.fq.gz -o QC/sample1/sample1_R1.clean.fq.gz -O QC/sample1/sample1_R2.clean.fq.gz --html QC/sample1/sample1.html --json QC/sample1/sample1.json

### 2.Mapping

    hisat2 --rg-id=sample1 --rg SM:sample1 --rg LB:PE100 --rg PL:ILLUMINA --rg PU:PE100 -p 8 --dta --summary-file mapping/sample1.stat --new-summary -x genome.index -1 sample1/sample1_r1.fq.gz -2 sample1/sample1_r2.fq.gz | sambamba view -t 8 -f bam -S /dev/stdin | sambamba sort --tmpdir=tmp/ -t 8 -l 6 /dev/stdin -o mapping/sample1_sorted.bam

### 3.quantify

    stringtie mapping/sample1_sorted.bam -p 8 pe -o quantify/sample1.gtf -A quantify/sample1.fpkm_tracking -G Anno.gtf

### 4.merge gene expression matrix

    python3 scripts/merge.py -i quantify/ -f ./merged_FPKM.txt -t ./merged_TPM.txt



