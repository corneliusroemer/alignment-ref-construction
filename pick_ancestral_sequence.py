#%%
from Bio import Phylo, Seq, SeqIO
from treetime import TreeAnc

#%%
tree = Phylo.read("build/tree.nwk", "newick")
tree.root_with_outgroup("NC_003663.2","KY369926.1")
# Phylo.draw(tree)
#%%
tt = TreeAnc(tree, "build/aligned.fasta", fill_overhangs=False)
# %%
tree_dict = tt.get_tree_dict()
#%%
td = {}
for sequence in tree_dict:
    td[sequence.id] = sequence.seq
td
#%%
mpx_sequences = SeqIO.to_dict(SeqIO.parse("input/mpx/mpx_assortment.fasta", "fasta"))
# %%
mpx_terminals = []
for terminal in tree.get_terminals():
    if terminal.name in mpx_sequences.keys():
        mpx_terminals.append(terminal)


ancestor_name = tt.tree.common_ancestor(mpx_terminals)

#%%
anc = str(td['NODE_0000004'])
coord = str(td['NC_063383'])

# %%
output_list = []
for (ref,coord) in zip(anc,coord):
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
