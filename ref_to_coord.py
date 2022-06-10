#%%
from Bio import SeqIO
from Bio import SeqRecord
from Bio import Seq

#%%
sequences =  SeqIO.to_dict(SeqIO.parse("alignment/joint_aligned.fasta", "fasta"))
sequences
# %%
output_list = []
for (ref,coord) in zip(str(sequences["ref"].seq),str(sequences["coord"].seq)):
    if coord != "-":
        if ref == "-":
            output_list.append(coord)
        else:
            output_list.append(ref)
# %%
output_seq = "".join(output_list)
# %%
SeqIO.write(SeqIO.SeqRecord(Seq.Seq(output_seq), id="ref_in_coord", description="Reference sequence in coord.fasta coordinates"), "output/ref_to_coord.fasta", "fasta")

# %%
