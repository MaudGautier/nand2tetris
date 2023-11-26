from hack_assembler import HackAssembler

if __name__ == "__main__":
    # Without symbols
    assembler = HackAssembler(file_name="projects/06/add/Add.asm")
    assembler.assemble()
    assembler = HackAssembler(file_name="projects/06/max/MaxL.asm")
    assembler.assemble()
    assembler = HackAssembler(file_name="projects/06/rect/RectL.asm")
    assembler.assemble()
    assembler = HackAssembler(file_name="projects/06/pong/PongL.asm")
    assembler.assemble()

    # With symbols
    assembler = HackAssembler(file_name="projects/06/max/Max.asm")
    assembler.assemble()
    assembler = HackAssembler(file_name="projects/06/rect/Rect.asm")
    assembler.assemble()
    assembler = HackAssembler(file_name="projects/06/pong/Pong.asm")
    assembler.assemble()

    print("All files have been assembled !")
