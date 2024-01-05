# Nand2Tetris

This repo contains my solutions to the Nand2Tetris project.

## Some notes on each module

### Module 1 — Boolean Logic

**Goal:**
Implement all elementary chips (= logic gates).

**Learnings:**

- Any boolean function can be represented using an expression containing `NAND` operations => From a `NAND` gate, we can
  compute everything.
- For this module: the `NAND` chip is given. We can implement all other chips using only this `NAND` chip, plus any
  other chip implemented from there.
- Each chip has a unique specification ("what": interface, abstraction) but often, several implementations ("how") are
  possible.
- Each chip can be implemented using the Hardware Description Language (HDL). This is a declarative language. Each file
  describes both the interface of the chip and its parts (how it is implemented).
- Some chips:
    - `Mux` = multiplexer — multiplexes a signal: from two inputs (`a` and `b`), outputs only one based on the selection
      bit (`sel`)
    - `DMux` = demultiplexer — de-multiplexes a signal: from a single input (`in`), outputs two (`a` and `b`) based on
      the selection bit (`sel`)
    - `[CHIP]16` = a 16-bit chip — applies the chip's logic onto each 16 bits of the input individually (returns 16-bit
      signal(s)), i.e. as if 16 chips apply the logic onto each bit in parallel.
    - `[CHIP]8Way` = an 8-way chip — applies the chip's logic onto the combination of all 8 input signals (returns a
      single signal), i.e. as if 7 chips apply the logic onto each pair of inputs sequentially.

**Usage:**

Test the implementation by launching the HardwareSimulator emulator:

```
tools/HardwareSimulator.sh
```

### Module 2 — Boolean Arithmetic

**Goal:**
Implement an Arithmetic Logic Unit (ALU) chip.

**Learnings:**

- `Half adder` chip — when the carry so far is 0, we sum `a` and `b` and output the `sum` and `carry` of the next bit on
  the left.
- `Full adder` chip — when the carry so far is 1, we sum `a`, `b` and `carry` (`c`) and output the sum and carry of the
  next bit on the left.
- `Multi-bit adder` chip — connects 15 full adders + 1 half adder for the rightmost bit. Note: overflow is ignored.
- The typical way to represent negative number `-x` is `2^n - x`.
- The `ALU` chip = Arithmetic Logic Unit — computes a function of the two inputs and outputs the result.
- Our Hack ALU has:
    - 2 inputs: `x` and `y`
    - 1 output: `out`
    - 6 control bits:
        - `zx` and `nx` to preset `x` (zero or negate)
        - `zy` and `ny` to preset `y` (zero or negate)
        - `f` to select between computing a `+` or a `&` operation between `x` and `y`
        - `no` to post-set the output `out` (negate it)
    - 2 output bits:
        - `zr` (states whether the output `out` is zero)
        - `nr` (states whether the output `out` is negative)

**Usage:**

Test the implementation by launching the HardwareSimulator emulator:

```
tools/HardwareSimulator.sh
```

### Module 3 — Sequential Logic

**Goal:**
Implement memory (which requires to remember state over time).

**Learnings:**

- The clock breaks the physical, continuous time into discrete timestamps (1 per cycle). The physical signal does not
  change instantly => we divide time into discrete timestamps so that we can look at what we have _after_ these
  changes (i.e. when the physical signal is stable).
- For this module: the `FPP` chip ("clocked data Flip-Flop") is given. It shifts the previous input to current output by
  1 time step.
- The `1-bit register` chip "remembers" a bit forever (until it is requested to load a new value). It can be implemented
  using a `Mux` chip (to define if we load the `in` value, or keep the previous output of time `t-1`) and a `DFF` chip (
  to shift the previous input to current output by 1 time step).
- A `multi-bit register` — composed of multiple 1-bit registers to remember multi-bit data.
- The `RAM` unit = Random Access Memory — a sequence of `n` addressable registers with addresses `0` to `n-1`. It is
  implemented by de-multiplexing the `input` signal, storing it in the correct register (based on the selector bit
  giving the register's address), and re-multiplexing the content of each register based on the selector bit to know
  which to output.
- At any given point in time, only _one_ register in the RAM is selected (via a selector whose number of bits
  is `log_2 n`). The RAM is called "Random Access Memory" because, irrespective of the RAM size, each register can be
  accessed at random in the same access time.
- The `PC` chip = `Program Counter` — used to keep track of which instruction should be executed next => supports 3
  primitive operations: `reset` (fetch the first instruction), `next` (fetch the next instruction) and go to (fetch
  instruction `n`).
- Since the output of the ALU is always routed to some sort of memory (RAM, register...), we have to ensure that the
  length of a clock cycle is longer than the time it takes to travel from the farthest chip. This guarantees that, by
  the time the sequential chip updates its state, the input it receives from the ALU is valid.

**Usage:**

Test the implementation by launching the HardwareSimulator emulator:

```
tools/HardwareSimulator.sh
```

### Module 4 — Machine Language

**Goal:**
Implement programs in machine language.

**Learnings:**

- Machine language = the most important interface in the world of computer science. It specifies:
    - what are the supported operations;
    - what they operate on;
    - how the program is controlled;
    - ...
- Each machine language instruction corresponds to one operation in the hardware => Hardware and machine language are
  very tightly coupled.
- Compiler = program that transforms high-level code into low-level code (machine language).
- Assembler = program that transforms machine language/machine assembly from symbols to binary code.
- Direct correspondence (1-1) between symbols (mnemonics) and binary code.
- Machine language elements:
    - Machine operations — correspond to what is implemented in hardware (arithmetic, logical and flow control
      operations);
    - Solution to the fact that addressing is expensive: Memory hierarchy = few memories that are close to the CPU and
      fast, more numerous ones that are bigger and longer to reach;
    - Registers are used either to store data, or to store addresses of other registers. Input and output devices
      connected to registers => gives access to input and output;
    - Flow control: usually executed in sequence, but sometimes need to jump to other instruction.
- The Hack Computer:
    - Data memory (RAM) — a sequence of 16-bit registers
    - Instruction memory (ROM) — a sequence of 16-bit registers
    - CPU — performs 16-bit operations
- The Hack Machine Language:
    - 2 sets of instructions:
        - A-instruction (`@21`) — sets the A register to the given value (`RAM[21]` is the selected RAM register);
        - C-instruction (`dest = comp ; jump`) — sets the result of `comp` into the `dest` , and then jump to `jump`.
    - 3 registers recognized:
        - D register (in CPU) — holds a 16-bit value that represents data;
        - A register (in CPU) — holds a 16-bit value that represents either address or data;
        - M register (in RAM) — represents the 16-bit RAM register addressed by the A register.
    - Control:
        - The ROM is loaded with a Hack program;
        - The reset button is pushed;
        - The program starts running.
- To make the machine language readable: use symbols (which then need to be translated into non-symbolic machine
  language, itself then translated into binary code).

**Usage:**

Test the implementation by launching the CPU emulator:

```
tools/CPUEmulator.sh
```

### Module 5 — Computer Architecture

**Goal:**
Build the Hack Computer.

**Learnings:**

- To implement the `Memory` chip:
    - De-multiplex the input to find which memory element is selected (RAM, screen, keyboard);
    - Set the inputted value in the corresponding register (depending on the selector bit previously decoded);
    - Multiplex the signal to output the value of the correct register.
- To implement the `CPU` chip:
    - Read the instructions (= decode A-instruction and C-instruction from the Hack Machine Language) to know how to set
      the control bits of the `ALU` chip.
    - Decode the jump part of the C-instruction to know how to set the control bits of the `PC` chip.
- To implement the Hack computer: use a `ROM` chip, a `Memory` chip and a `CPU` chip.
- Machine language is very tightly coupled to hardware.
- Everything is self-contained: there is only a `reset` button to start/restart the program. Once the reset button has
  been pushed, the computer works by itself: the CPU is linked to Memory and reads or writes from/to it constantly, and
  the PC allows to fetch the next instruction from the ROM.
- There is a memory map for each distinct I/O device => treated as a portion of the memory (=> no need to know all the
  complexity)

**Usage:**

Test the implementation by launching the HardwareSimulator emulator:

```
tools/HardwareSimulator.sh
```

### Module 6 — Assembler

**Goal:**
Write an assembler (in a high-level langauge) to translate assembly language into binary machine language.

**Learnings:**

- Machine language = Binary machine language (instructions expressed in binary code).
- Assembly language = Symbolic machine language (instructions expressed using human-friendly mnemonics).
- Assembler = An agent that carries out the translation from assembly to machine language (first software layer above
  the hardware). It basically does text processing/string processing to translate assembly code to machine code.
- The overall Hack assembly logic is:
    - Parse the instruction = break it down into its underlying fields;
    - For A-instructions: translate the decimal value into a binary value;
    - For C-instructions: generate the corresponding binary code for each field, and assemble them into a complete
      16-bit instruction;
    - Write the 16-bit instruction to the output file.
- Grammar = Specifications of the language.
- Parser = Reads the instruction and break it down into its subfields.
- Dealing with symbols is much more challenging than the rest (parsing, converting to binary code and assembling)

**Usage:**

```
# Run assembler on files
python projects/06/hack_assembler/main.py
```

Generate comparison files by running them with the built-in emulator `tools/Assembler.sh` and saving them
under `[FILE_NAME].comp.hack`.
Then compare with the one generated by the implemented HackAssembler (`[FILE_NAME].hack`) either directly on the
emulator, or `diff projects/06/add/Add.hack projects/06/add/Add.comp.hack` (or via test script to come).

Tests can also be run automatically by running:

```
python projects/06/hack_assembler/tests/auto_test.py
```
