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
http://rebase.neb.com/rebase/rebase.html
http://rebase.neb.com//rebase.seqs.html
```
wget -c ftp://ftp.neb.com/pub/rebase/protein_seqs.txt

```

## 4.rebase
* Download the database
```
```