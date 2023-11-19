// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// Pseudo code
// -----------
//   n = R0
//   m = R1
//   i = 0
//   total = 0
//   R2 = total (0)
// LOOP
//   if (m - i == 0) then goto STOP
//   total = total + n
//   i++
//   goto LOOP
// END
//   R2 = total

   // n = R0
   @R0
   D=M
   @n
   M=D

   // m = R1
   @R1
   D=M
   @m
   M=D

   // i = 0
   @0
   D=A
   @i
   M=D

   // total = 0
   @0
   D=A
   @total
   M=D

   // R2 = total (0)
   @total
   D=M
   @R2
   M=D

(LOOP)
   // if (m - i == 0) then goto STOP
   @m
   D=M
   @i
   D=D-M
   @STOP
   D;JEQ

   // total = total + n
   @n
   D=M
   @total
   //D=D+M
   //M=D
   M=D+M

   // i++
   @i
   M=M+1

   // goto LOOP
   @LOOP
   0;JMP

(STOP)
   // R2 = total
   @total
   D=M
   @R2
   M=D

(END)
   @END
   0;JMP
