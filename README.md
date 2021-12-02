# biodb
Common bioinformatics database construction


## 1.taxonomy （Substance classification database）
* Download the database
```
wget -c https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz
tar -zxvf new_taxdump.tar.gz
lineage2tax.py fullnamelineage.dmp >species.taxonomy
get_taxid.py rankedlineage.dmp --kingdom Bacteria >Bacteria.taxid

```


## 2.Rfam
* Download the database
```
wget -c https://ftp.ebi.ac.uk/pub/databases/Rfam/14.6/Rfam.cm.gz
wget -c https://ftp.ebi.ac.uk/pub/databases/Rfam/14.6/rfam2go/rfam2go
wget -c https://ftp.ebi.ac.uk/pub/databases/Rfam/14.6/database_files/family.txt.gz
zcat family.txt.gz |awk -F '\t' '{print $1"\t"$2"\t"$4"\t"$19"\t"$30}' >family.txt
gunzip Rfam.cm.gz
cmpress Rfam.cm
```
## 3. Refseq
* Download the database

```


```

## 4.rebase
* R：编码限制性核酸内切酶
* M：编码限制性甲基化酶
* S：编码限制性酶和甲基化酶的协同表达
* Download the database
http://rebase.neb.com/rebase/rebase.html
http://rebase.neb.com//rebase.seqs.html
```
wget -c ftp://ftp.neb.com/pub/rebase/protein_seqs.txt
```

## 5.TIGRFAMs
```
https://ftp.ncbi.nlm.nih.gov/hmm/TIGRFAMs/
```


## kraken
[kraken-db](https://benlangmead.github.io/aws-indexes/k2)
```
wget -c https://genome-idx.s3.amazonaws.com/kraken/k2_viral_20210517.tar.gz

```

## KEGG
* [KEGG](https://www.kegg.jp/)数据连接
* [ko00001.keg](https://www.kegg.jp/brite/ko00001)
```
https://www.kegg.jp/entry/ko:K23120
```
## COG
The way python reads COG files:open(file, encoding='ISO 8859-1')
* [cog]
* [cog-20.fa.gz](https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/cog-20.fa.gz)
* [cog-20.def.tab](https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/cog-20.def.tab)
* [fun-20.tab](https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/fun-20.tab)
* [cog-20.cog.csv](https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/cog-20.cog.csv)
```
rename_cogid.py cog-20.fa -c cog-20.cog.csv >cog.fasta
diamond makedb --in cog.fasta -d cog


#----------------------
#individuation
grep_id.py all.CAZy.out -i ${sample}.id >${sample}.CAZy.out
cazyproc.py ${sample}.CAZy.out --activ CAZy.activities.txt \
  --subfam CAZy.subfam.txt -o ${sample}.cazy_classify.tsv >${sample}.cazy.tsv
plot_cazy.py ${sample}.cazy_classify.tsv -p ${sample}
get_cazy_tax.py ${sample}.cazy.tsv --tax NR_anno_tax.txt >${sample}.CAZy_tax.tsv

```
## CAZy
* [CAZy](http://www.cazy.org/)
* [CAZydb](https://bcb.unl.edu/dbCAN2/download/Databases/)
* [SLH](https://www.ebi.ac.uk/interpro/entry/IPR001119)
* [Cohesin](https://www.ebi.ac.uk/interpro/entry/IPR002102)
* [DBCAN-PUL](https://bcb.unl.edu/dbcan_pul/Webserver/static/DBCAN-PUL/):polysaccharide utilization loci
* [PUL](https://bcb.unl.edu/dbcan_pul/Webserver/static/DBCAN-PUL/PUL.faa)
```
deal_with_cazy.py IPR002102.fasta -d IPR001119.tsv >CAZy.add.fasta
```
