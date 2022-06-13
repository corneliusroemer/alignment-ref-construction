
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

rule pick_ancestral_sequence:
    input:
        tree = rules.tree.output,
        alignment = rules.align_fastas.output,
        mpx_sequences = "input/mpx/mpx_assortment.fasta",
    output: "output/ref_to_coord.fasta"
    shell: """
        python pick_ancestral_sequence.py \
            {input.tree} \
            {input.alignment} \
            {input.mpx_sequences} \
            {output}
        """
