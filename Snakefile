
rule join_fastas:
    input:
        cpx=directory("input/mpx"),
        mpx=directory("input/cpx")
    output: "build/joined.fasta"
    shell: "cat {input.cpx}/* {input.mpx}/*  > {output}"


rule align_fastas:
    input: rules.join_fastas.output
    output: "build/aligned.fasta"
    shell: "mafft --thread 10 --auto {input} > {output}"

rule tree:
    input: rules.align_fastas.output
    output: "build/tree.nwk"
    shell: """
        augur tree \
            --alignment {input} \
            --output {output}
        """

rule infer_ancestors:
    input: 
        tree = rules.tree.output,
        alignment = rules.align_fastas.output
    output: "build/ancestral_reconstruction/ancestral_sequences.fasta"
    shell: """
        treetime ancestral \
            --aln {input.alignment}\
            --tree {input.tree} \
            --keep-overhangs \
            --outdir build/ancestral_reconstruction
        """

rule tree_with_ancestors:
    input: rules.infer_ancestors.output
    output: "build/tree_with_ancestors.nwk"
    shell: """
        augur tree \
            --alignment {input} \
            --output {output}
        """

rule pick_ancestral_sequence:
    input:
        tree = rules.tree_with_ancestors.output,
        mpx_sequences = "input/mpx/mpx_assortment.fasta",
        ancestral = "build/ancestral_reconstruction/ancestral_sequences.fasta"
    output: "output/ref_to_coord.fasta"
    shell: """
        python pick_ancestral_sequence.py \
            --tree {input.tree} \
            --mpx_sequences {input.mpx_sequences} \
            --ancestral {input.ancestral} \
            --output {output}
        """
