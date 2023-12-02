# Generate bit-format diagrams for an instruction set

```
python isa_gen.py InstructionBitFormats.json
for diag in gen/*diag; do
    packetdiag --no-transparency --font ubuntu.mono-bold.ttf $diag;
done
```