##################################################
##################################################
##################################################
# functions for use with pipeline_dada2.py
##################################################
##################################################
##################################################


def seq2id(seqtable, outfile_map, outfile_table):
    '''
    assign a unique identifier to each unique
    sequence in dada2 output
    '''
    inf = open(seqtable)
    header = inf.readline()
    c = 1
    out_map = open(outfile_map, "w")
    out_map.write("id\tsequence\n")
    out_table = open(outfile_table, "w")
    out_table.write(header)
    for line in inf.readlines():
        data = line[:-1].split("\t")
        seq = data[0]
        identifier = "ASV" + str(c)
        c += 1
        out_map.write("\t".join([identifier, seq]) + "\n")
        out_table.write("\t".join([identifier, "\t".join(data[1:])]) + "\n")
    out_map.close()
    out_table.close()
        
##################################################
##################################################
##################################################

def makeDefinitiveAbundanceFile(id2seq, seq2taxonomy, id2abundance, outfile):
    '''
    make a definitive table of abundances of the form:
    ASVXXX:p__phylum;c__class;o__order;f__family;g__genus;s__species    21
    ...
    '''
    inf_id2seq = open(id2seq)
    inf_id2seq.readline()
    inf_seq2taxonomy = open(seq2taxonomy)
    inf_seq2taxonomy.readline()
    inf_id2abundance = open(id2abundance)
    header = inf_id2abundance.readline()
    
    id2seq_dict = {}
    seq2taxonomy_dict = {}

    for line in inf_id2seq.readlines():
        data = line[:-1].split("\t")
        id2seq_dict[data[0]] = data[1]

    for line in inf_seq2taxonomy.readlines():
        data = line[:-1].split("\t")
        # from phylum level
        taxonomy = data[2:]
        taxonomy[0] = "p__" + taxonomy[0]
        taxonomy[1] = "c__" + taxonomy[1]
        taxonomy[2] = "o__" + taxonomy[2]
        taxonomy[3] = "f__" + taxonomy[3]
        taxonomy[4] = "g__" + taxonomy[4]
        taxonomy[5] = "s__" + taxonomy[5]
        taxonomy = ";".join(taxonomy)
        
        seq2taxonomy_dict[data[0]] = taxonomy

    # iterate over abundance file and create
    # new names
    outfile = open(outfile, "w")
    outfile.write(header)
    for line in inf_id2abundance.readlines():
        data = line[:-1].split("\t")
        identifier = data[0]
        seq = id2seq_dict[identifier]
        taxonomy = seq2taxonomy_dict[seq]
        newid = ":".join([identifier, taxonomy])
        outfile.write("\t".join([newid] + data[1:]) + "\n")
    outfile.close()
    
