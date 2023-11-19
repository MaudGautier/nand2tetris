// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// Pseudo code
// -----------
//    start_screen = SCREEN
//    end_screen = SCREEN + 8192 (i.e. 512*256/16)
//    max_i = 8192 (i.e. 512*256/16)
// TEST_KBD
//    initialize i (i=0)
//    if (KBD != 0) then goto BLACKEN
//    (else if (KBD == 0) then goto WHITEN)
// BLACKEN_LOOP
//    // PSEUDO
//    // for (i=start_screen; i<end_screen; i++) {
//    //     RAM[i] = -1
//    // }
//    if (i == max_i) then goto TEST_KBD
//    RAM[i] = -1
//    i++
//    goto BLACKEN_LOOP

// WHITEN_LOOP
//    // PSEUDO
//    // for (i=start_screen; i<end_screen; i++) {
//    //     RAM[i] = 0
//    // }
//    if (i == max_i) then goto TEST_KBD
//    RAM[i] = 0
//    i++
//    goto WHITEN_LOOP


   //  start_screen = SCREEN
   @SCREEN
   D=A
   @start_screen
   M=D

   //  end_screen = SCREEN + 8192 (i.e. 512*256/16)
   // max_i = 8192 (i.e. 512*256/16)
   @8192
   D=A
   @max_i
   M=D

(TEST_KBD)
   // initialize i
   @i
   M=0

   //  if (KBD != 0) then goto BLACKEN
   @KBD
   D=M
   @BLACKEN_LOOP
   D;JNE

   //  (else if (KBD == 0) then goto WHITEN)
   @KBD
   D=M
   @WHITEN_LOOP
   D;JEQ

(BLACKEN_LOOP)
   // if (i == max_i) then goto TEST_KBD
   @max_i
   D=M
   @i
   D=D-M
   @TEST_KBD
   D;JEQ

   // RAM[i] = -1
   @start_screen
   D=M
   @i
   A=D+M
   M=-1

   // i++
   @i
   M=M+1

   // goto BLACKEN_LOOP
   @BLACKEN_LOOP
   0;JMP

(WHITEN_LOOP)
   // if (i == max_i) then goto TEST_KBD
   @max_i
   D=M
   @i
   D=D-M
   @TEST_KBD
   D;JEQ

   // RAM[i] = 0
   @start_screen
   D=M
   @i
   A=D+M
   M=0

   // i++
   @i
   M=M+1

   // goto WHITEN_LOOP
   @WHITEN_LOOP
   0;JMP
