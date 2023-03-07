# generate makefile contents
def genMakefile(id: str, compiler: str, flags: str) -> str:
    newline = "\n"
    tab = "\t"
    file = ""

    # compiler
    file += "CC=" + compiler + newline

    # compiler default flags
    # no optimisation options: -O0 -fsanitize=address -fno-tree-vectorize
    file += "CFLAGS= -g" + newline

    # compiler optional optimisation flags
    file += "OFLAGS= " + flags + newline

    file += newline

    # src directory
    file += "SRCDIR=src" + newline

    # object directory
    file += "ODIR=obj/obj_" + id + newline

    # output directory
    file += "OUTDIR=output" + newline

    # executable directory
    file += "EXECDIR=exec" + newline

    file += newline

    # libraries
    file += "LIBS= -lm" + newline

    file += newline

    # dependencies (header)
    file += "DEPS= coord.h" + newline

    file += newline

    # src code
    file += "SRC= MD.c control.c util.c" + newline

    file += newline

    # object files
    file += "_OBJ= $(SRC:.c=.o)" + newline
    file += "OBJ= $(patsubst %,$(ODIR)/%,$(_OBJ))" + newline

    file += newline

    # executables
    file += "EXECUTABLES= $(EXECDIR)/MD_" + f"{id:02}" + newline

    # input data
    file += "DATA= $(SRCDIR)/input.dat" + newline

    file += newline

    #  `make all` will build all executables
    file += "all: $(EXECUTABLES)" + newline

    file += newline

    # generate executables from object files
    file += "$(EXECUTABLES): $(OBJ)" + newline
    file += tab + "@mkdir -p $(@D)" + newline
    file += tab + "$(CC) $(CFLAGS) $(OFLAGS) -o $@ $^ $(LIBS)" + newline

    file += newline

    # generate object files
    file += "$(ODIR)/%.o: $(SRCDIR)/%.c $(SRCDIR)/$(DEPS)" + newline
    file += tab + "@mkdir -p $(@D)" + newline
    file += tab + "$(CC) -c -o $@ $<" + newline

    file += newline

    # run executable
    file += "run: output" + newline
    file += f"output: $(EXECUTABLES) $(DATA)" + newline
    file += tab + f"cd $(EXECDIR) && ./MD_{id:02} 100 ../$(DATA) {id}" + newline

    file += newline

    # clean
    file += ".PHONY: clean test" + newline
    file += "clean:" + newline
    file += (
        tab
        + "rm -f $(ODIR)/*.o $(EXECUTABLES) "
        + f"$(EXECDIR)/output_{id:02}.dat*"
        + newline
    )

    # test
    file += "test:" + newline
    file += tab + f'echo "test {id:02}" >> ./test/test.txt' + newline

    file += (
        tab
        + f"./test/diff-output ./src/output.dat010 ./$(EXECDIR)/output_{id:02}.dat010 >> ./test/test.txt"
        + newline
    )
    file += (
        tab
        + f"./test/diff-output ./src/output.dat020 ./$(EXECDIR)/output_{id:02}.dat020 >> ./test/test.txt"
        + newline
    )
    file += (
        tab
        + f"./test/diff-output ./src/output.dat030 ./$(EXECDIR)/output_{id:02}.dat030 >> ./test/test.txt"
        + newline
    )
    file += (
        tab
        + f"./test/diff-output ./src/output.dat040 ./$(EXECDIR)/output_{id:02}.dat040 >> ./test/test.txt"
        + newline
    )
    file += (
        tab
        + f"./test/diff-output ./src/output.dat050 ./$(EXECDIR)/output_{id:02}.dat050 >> ./test/test.txt"
        + newline
    )

    return file


def main():
    # read flat text file
    with open("flags.txt", "r") as infile:
        flags = infile.read().split("\n")

    for i, flag in enumerate(flags):
        print(flag)
        makefile = genMakefile(str(i), "gcc", flag)
        with open(f"Makefile_{i}", "w") as outfile:
            outfile.write(makefile)
        print(f"makefile for flag: {flag} is generated")


if __name__ == "__main__":
    print("run")
    main()
