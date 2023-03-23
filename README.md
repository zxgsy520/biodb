# biodb
Installation and analysis of common databases

## Requirements
* [Python](https://www.python.org/)
* Three-party python package
  * [matplotlib](https://matplotlib.org/)
  * [numpy](https://numpy.org/doc/stable/index.html)
## Installation
```
git clone https://github.com/zxgsy520/biodb.git
cd  biodb/bin    
chmod 755 *    #Linux system can be used directly
cd ../scripts
chmod 755 *   #Supports all systems but requires python and related packages
```
or
```
wget -c https://github.com/zxgsy520/biodb/archive/refs/heads/main.zip
unzip main.zip

```
## Options and usage
### Draw a circle graph locally
* [visualize](http://mkweb.bcgsc.ca/tableviewer/visualize/)
```
parse-table -conf parse-table.conf -file txt.tsv -segment_order=ascii,size_desc -placement_order=row,col -interpolate_type count -color_source row -transparency 1 -fade_transparency 0 -ribbon_layer_order=size_asc >parsed.txt
cat  parsed.txt |make-conf -dir data
circos -conf chord_circos.conf 
```
<p align="center">
  <img src="https://github.com/zxgsy520/biodb/blob/main/docs/order_chord.svg" width = "300" height = "300" alt="Species functional circle diagram"/>
</p>

## Database introduction

### 1.taxonomy （Substance classification database）
* Download the database
[taxonkit](https://github.com/shenwei356/taxonkit)
```
wget -c https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz
tar -zxvf new_taxdump.tar.gz
lineage2tax.py fullnamelineage.dmp >species.taxonomy
get_taxid.py rankedlineage.dmp --kingdom Bacteria >Bacteria.taxid
awk '{print $1}' species.taxonomy |sort -u >all.tax.id
#wget -c https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
#taxonkit list -j 4 --ids 10239 --data-dir ./taxonomy >Viruses.taxid
#blastdbcmd -db ../nr -dbtype "prot" -taxidlist Viruses.taxid -out Viruses.fa
#blastdbcmd -db ../nr -dbtype "prot" -taxidlist Viruses.taxid -out  viruses.fasta2_newtaxid -outfmt "%a %T"
```
* Generate taxonomy files for kraken annotations （生成分类注释文件）
```
taxonkit lineage all.tax.id --data-dir ./new_taxdump --threads 8 | awk '$2!=""' > lineage.txt
taxonkit reformat lineage.txt --format "k__{k}|p__{p}|c__{c}|o__{o}|f__{f}|g__{g}|s__{s}" --data-dir ./new_taxdump --threads 8 >kraken.temp_taxonomy 
 print_tax.py kraken.temp_taxonomy >kraken.taxonomy #提取第1和第3列，将真菌的Eukaryota替换为Fungi
```

### 2.Rfam
* Download the database
```
wget -c https://ftp.ebi.ac.uk/pub/databases/Rfam/14.6/Rfam.cm.gz
wget -c https://ftp.ebi.ac.uk/pub/databases/Rfam/14.6/rfam2go/rfam2go
wget -c https://ftp.ebi.ac.uk/pub/databases/Rfam/14.6/database_files/family.txt.gz
zcat family.txt.gz |awk -F '\t' '{print $1"\t"$2"\t"$4"\t"$19"\t"$30}' >family.txt
gunzip Rfam.cm.gz
cmpress Rfam.cm
```
### 3. Refseq
* Download the database
https://ftp.ncbi.nlm.nih.gov/blast/db/
```

```

### 4.rebase
* R：编码限制性核酸内切酶
* M：编码限制性甲基化酶
* S：编码限制性酶和甲基化酶的协同表达
* Download the database
http://rebase.neb.com/rebase/rebase.html
http://rebase.neb.com//rebase.seqs.html
```
wget -c ftp://ftp.neb.com/pub/rebase/protein_seqs.txt
```

### 5.TIGRFAMs
```
https://ftp.ncbi.nlm.nih.gov/hmm/TIGRFAMs/
```
### 6.Nr
```
wget -c https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz
mv nr.gz nr.fa.gz
gunzip nr.fa.gz
diamond makedb --in nr.fa --db nr --taxonmap prot.accession2taxid.gz --taxonnodes nodes.dmp --taxonnames names.dmp
```


### kraken
[kraken-db](https://benlangmead.github.io/aws-indexes/k2)
```
wget -c https://genome-idx.s3.amazonaws.com/kraken/k2_viral_20210517.tar.gz

```

### KEGG
* [KEGG](https://www.kegg.jp/)数据连接
* [ko00001.keg](https://www.kegg.jp/brite/ko00001)
* [mun00001.keg](https://www.kegg.jp/brite/mun00001.keg)
```
https://www.kegg.jp/entry/ko:K23120
```
### COG
The way python reads COG files:open(file, encoding='ISO 8859-1')
* [cog]
* [cog-20.fa.gz](https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/cog-20.fa.gz)
* [cog-20.def.tab](https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/cog-20.def.tab)
* [fun-20.tab](https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/fun-20.tab)
* [cog-20.cog.csv](https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/cog-20.cog.csv)
```
rename_cogid.py cog-20.fa -c cog-20.cog.csv >cog.fasta
diamond makedb --in cog.fasta -d cog

```

### CAZy
* [CAZy](http://www.cazy.org/)
* [CAZydb](https://bcb.unl.edu/dbCAN2/download/Databases/)
* [SLH](https://www.ebi.ac.uk/interpro/entry/IPR001119)
* [Cohesin](https://www.ebi.ac.uk/interpro/entry/IPR002102)
* [DBCAN-PUL](https://bcb.unl.edu/dbcan_pul/Webserver/static/DBCAN-PUL/):polysaccharide utilization loci
* [PUL](https://bcb.unl.edu/dbcan_pul/Webserver/static/DBCAN-PUL/PUL.faa)
```
deal_with_cazy.py IPR002102.fasta -d IPR001119.tsv >CAZy.add.fasta

#----------------------
#individuation
grep_id.py all.CAZy.out -i ${sample}.id >${sample}.CAZy.out
cazyproc.py ${sample}.CAZy.out --activ CAZy.activities.txt \
  --subfam CAZy.subfam.txt -o ${sample}.cazy_classify.tsv >${sample}.cazy.tsv
plot_cazy.py ${sample}.cazy_classify.tsv -p ${sample}
get_cazy_tax.py ${sample}.cazy.tsv --tax NR_anno_tax.txt >${sample}.CAZy_tax.tsv
stat_function_class.py ${sample}.CAZy_tax.tsv  --kingdom Bacteria --level p > ${sample}.phylum_stat_cazy_tax.tsv
tax2chord.py ${sample}.phylum_stat_cazy_tax.tsv --display 5 >${sample}.phylum_chord.tsv
```
### SwissProt
```
wget -c http://ftp.ebi.ac.uk/pub/databases/swissprot/release/uniprot_sprot.fasta.gz
```

### vogdb
* [vogdb](https://vogdb.org/)
* [vog_functional_categories.txt](http://fileshare.csb.univie.ac.at/vog/latest/vog_functional_categories.txt)
* [vog.lca.tsv.gz](http://fileshare.csb.univie.ac.at/vog/latest/vog.lca.tsv.gz)
* [vog.members.tsv.gz](http://fileshare.csb.univie.ac.at/vog/latest/vog.members.tsv.gz)
* [vog.annotations.tsv.gz](http://fileshare.csb.univie.ac.at/vog/latest/vog.annotations.tsv.gz)
* [vog.proteins.all.fa.gz](http://fileshare.csb.univie.ac.at/vog/latest/vog.faa.tar.gz)
```
./cat_vog_protein.py vog_protein/*.faa --annotations vog.annotations.tsv.gz >vogdb.fasta
or
./build_vogdb.py vog.proteins.all.fa >vogdb.fasta
```
