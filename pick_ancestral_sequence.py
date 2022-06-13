#%%
import typer

#%%
def main(tree_path: str, alignment: str, mpx_sequences: str, output: str):
    from Bio import Phylo, Seq, SeqIO
    from treetime import TreeAnc
    tree = Phylo.read(tree_path, "newick")
    tree.root_with_outgroup("NC_003663.2","KY369926.1")

    tt = TreeAnc(tree, alignment, fill_overhangs=False)

    tree_dict = tt.get_tree_dict()
    td = {}
    for sequence in tree_dict:
        td[sequence.id] = sequence.seq

    mpx_sequences = SeqIO.to_dict(SeqIO.parse(mpx_sequences, "fasta"))
    mpx_terminals = []
    for terminal in tree.get_terminals():
        if terminal.name in mpx_sequences.keys():
            mpx_terminals.append(terminal)

    ancestor_name = tt.tree.common_ancestor(mpx_terminals).name

    anc = str(td[ancestor_name])
    coord = str(td['NC_063383'])

    output_list = []
    for (ref,coord) in zip(anc,coord):
        if coord != "-":
            if ref == "-":
                output_list.append(coord)
            else:
                output_list.append(ref)
    output_seq = "".join(output_list)
    # %%
    SeqIO.write(SeqIO.SeqRecord(Seq.Seq(output_seq), id="ref_in_coord", description="Reference sequence in coord.fasta coordinates"), output, "fasta")

if __name__ == "__main__":
    typer.run(main)