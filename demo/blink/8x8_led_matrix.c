/*
 * Example Code for an 8x8 LED Matrix
 *
 * Scrolls a message across an 8x8 LED Matrix
 */

#include <propeller.h>

#define GET_MASK(pin) (1UL << (pin))
#define propeller_set_outa_bits(bits) OUTA |= (bits)
#define propeller_clr_outa_bits(bits) OUTA &= ~(bits)
#define OUT_LOW(pin) (propeller_clr_outa_bits(GET_MASK(pin)))
#define OUT_HIGH(pin) (propeller_set_outa_bits(GET_MASK(pin)))
#define DIR_OUTPUT(pin) (propeller_set_dira_bits(GET_MASK(pin)))
#define propeller_set_dira_bits(bits) DIRA |= (bits)

static int int_max(int a, int b)
{
  b = a - b;
  a -= b & (b >> 31);
  return a;
}

#define propeller_waitcnt(a) waitcnt(a)
#define MIN_WAITCNT_WINDOW 381
#define propeller_get_clockfreq() CLKFREQ
#define propeller_get_cnt() CNT
#define BBOS_DELAY_MSEC(msec)                                           \
  propeller_waitcnt(int_max((propeller_get_clockfreq() / 1000) * msec - 3932, \
                            MIN_WAITCNT_WINDOW) +                       \
                    propeller_get_cnt())

/* Number of times to repeat each frame */
static int speed = 5;
/* Microseconds to leave each row on before moving to the next */
static int delay = 200;

/* The message to display. */
static char message[] = "BIONIC BUNNY INSIDE ";

//Variables used for scrolling (both start at 0
int idx = 0;  //this is the current charachter in the string being displayed
int offset = 0; //this is how many columns it is offset by

/*
 * An Array defining which pin each row is attached to (rows are common anode
 * (drive HIGH)).
 */
static int row_pins[] = {0,1, 2, 3, 4, 5, 6, 7};

/*
 * An Array defining which pin each column is attached to (columns are common
 * cathode (drive LOW)).
 */
static int col_pins[] = {8, 9,10, 11, 12, 13, 14, 15};

/* Constants defining each charachters position in an array of integer arrays */
enum {
  /* Letters */
  A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z,
  /* Punctuation */
  COL, DASH, BRA2, _, LINE, DOT,
  /* Extra Charchters */
  FULL, CHECK, B2, TEMP, SMILE, COLDOT
};

/*
 * The array used to hold a bitmap of the display (if you wish to do something
 * other than scrolling marque change the data in this variable then display).
 */
char data[] = {0, 0, 0, 0, 0, 0, 0, 0};

//The alphabet
//Each Charachter is an 8 x 7 bitmap where 1 is on and 0 if off
const int _A[] = {0x08, 0x14, 0x22, 0x41, 0x7F, 0x41, 0x41, 0x00};
const int _B[] = {0x7E, 0x21, 0x21, 0x3E, 0x21, 0x21, 0x7E, 0x00};
const int _C[] = {0x1F, 0x20, 0x40, 0x40, 0x40, 0x20, 0x1F, 0x00};
const int _D[] = {0x7c, 0x22, 0x21, 0x21, 0x21, 0x22, 0x7c, 0x00};
const int _E[] = {0x7F, 0x40, 0x40, 0x7c, 0x40, 0x40, 0x7F, 0x00};
const int _F[] = {0x7F, 0x40, 0x40, 0x7c, 0x40, 0x40, 0x40, 0x00};
const int _G[] = {0x1F, 0x20, 0x40, 0x4F, 0x41, 0x21, 0x1F, 0x00};
const int _H[] = {0x41, 0x41, 0x41, 0x7F, 0x41, 0x41, 0x41, 0x00};
const int _I[] = {0x7F, 0x08, 0x08, 0x08, 0x08, 0x08, 0x7F, 0x00};
const int _J[] = {0x0F, 0x01, 0x01, 0x01, 0x01, 0x41, 0x3E, 0x00};
const int _K[] = {0x43, 0x44, 0x48, 0x70, 0x48, 0x44, 0x43, 0x00};
const int _L[] = {0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x7F, 0x00};
const int _M[] = {0x76, 0x49, 0x49, 0x49, 0x49, 0x49, 0x49, 0x00};
const int _N[] = {0x41, 0x61, 0x51, 0x49, 0x45, 0x43, 0x41, 0x00};
const int _O[] = {0x1C, 0x22, 0x41, 0x49, 0x41, 0x22, 0x1C, 0x00};
const int _P[] = {0x7E, 0x21, 0x21, 0x3E, 0x20, 0x20, 0x20, 0x00};
const int _Q[] = {0x1C, 0x22, 0x41, 0x41, 0x45, 0x22, 0x1D, 0x00};
const int _R[] = {0x7E, 0x21, 0x21, 0x2e, 0x24, 0x22, 0x21, 0x00};
const int _S[] = {0x3F, 0x40, 0x40, 0x3E, 0x01, 0x01, 0x7E, 0x00};
const int _T[] = {0x7F, 0x08, 0x08, 0x08, 0x08, 0x08,  0x8, 0x00};
const int _U[] = {0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x3E, 0x00};
const int _V[] = {0x41, 0x41, 0x41, 0x41, 0x22, 0x14,  0x8, 0x00};
const int _W[] = {0x41, 0x49, 0x49, 0x49, 0x49, 0x49, 0x36, 0x00};
const int _X[] = {0x41, 0x22, 0x14,  0x8, 0x14, 0x22, 0x41, 0x00};
const int _Y[] = {0x41, 0x22, 0x14,  0x8,  0x8,  0x8,  0x8, 0x00};
const int _Z[] = {0x7F, 0x2, 0x4, 0x3E, 0x10, 0x20, 0x7F, 0x00};
const int _COL[] = {0x00, 0x18, 0x18, 0x00, 0x18, 0x18, 0x00, 0x00};
const int _DASH[] = {0x00, 0x00, 0x00, 0x3E, 0x00, 0x00, 0x00, 0x00};
const int _BRA2[] = {0x10,  0x8,  0x4,  0x4,  0x8, 0x10, 0x00, 0x00};
const int __[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
const int _FULL[] = {0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x00};
const int _CHECK[] = {0x55, 0x2A, 0x55, 0x2A, 0x55, 0x2A, 0x55, 0x00};
const int _B2[] = {0x3E, 0x1, 0x1, 0xF, 0x1, 0x41, 0x3E, 0x00};
const int _TEMP[] = {0x3, 0x1F, 0x3F, 0x7E, 0x7F, 0x1F, 0x3, 0x00};
const int _LINE[] = {0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x00};
const int _SMILE[] = {0x00, 0x64, 0x62, 0x19, 0x62, 0x64, 0x00, 0x00};
const int _DOT[] = {0x00, 0x00, 0x00, 0x00, 0x60, 0x60, 0x00, 0x00};
const int _COLDOT[] = {0x00, 0x30, 0x30, 0x00, 0x33, 0x33, 0x00, 0x00};

/*
 * Load the bitmap charachters into an array (each charachters position
 * corresponds to its previously defined idx (ie _A (a's bitmap) is at idx 0 and
 * A = 0 so letters[A] will return the 'A' bitmap).
 */
const int* letters[] = {
  _A,_B,_C,_D,_E,_F,_G,_H,_I,_J,_K,_L,_M,_N,_O,_P,_Q,_R, _S,_T,_U,_V,_W,_X,_Y,_Z,
  _COL,_DASH,_BRA2,__,
  _FULL, _CHECK, _B2, _TEMP, _LINE, _SMILE, _DOT, _COLDOT
};

/* Setup runs once when power is applied */
void setup()
{
  int i;
  /* Set the 16 pins used to control the array as OUTPUTs */
  for(i = 0; i < 8; i++){
    DIR_OUTPUT(row_pins[i]);
    DIR_OUTPUT(col_pins[i]);
  }
  _OUTA = 0xFF00;
}

//returns the idx of a given charachter
//for converting from a string to a lookup in our array of charachter bitmaps
int getChar(char charachter){
 int returnValue = Z;
 switch(charachter){
  case 'A': returnValue = A; break;
  case 'a': returnValue = A; break;
  case 'B': returnValue = B; break;
  case 'b': returnValue = B; break;
  case 'C': returnValue = C; break;
  case 'c': returnValue = C; break;
  case 'D': returnValue = D; break;
  case 'd': returnValue = D; break;
  case 'E': returnValue = E; break;
  case 'e': returnValue = E; break;
  case 'F': returnValue = F; break;
  case 'f': returnValue = F; break;
  case 'G': returnValue = G; break;
  case 'g': returnValue = G; break;
  case 'H': returnValue = H; break;
  case 'h': returnValue = H; break;
  case 'I': returnValue = I; break;
  case 'i': returnValue = I; break;
  case 'J': returnValue = J; break;
  case 'j': returnValue = J; break;
  case 'K': returnValue = K; break;
  case 'k': returnValue = K; break;
  case 'L': returnValue = L; break;
  case 'l': returnValue = L; break;
  case 'M': returnValue = M; break;
  case 'm': returnValue = M; break;
  case 'N': returnValue = N; break;
  case 'n': returnValue = N; break;
  case 'O': returnValue = O; break;
  case 'o': returnValue = O; break;
  case 'P': returnValue = P; break;
  case 'p': returnValue = P; break;
  case 'Q': returnValue = Q; break;
  case 'q': returnValue = Q; break;
  case 'R': returnValue = R; break;
  case 'r': returnValue = R; break;
  case 'S': returnValue = S; break;
  case 's': returnValue = S; break;
  case 'T': returnValue = T; break;
  case 't': returnValue = T; break;
  case 'U': returnValue = U; break;
  case 'u': returnValue = U; break;
  case 'V': returnValue = V; break;
  case 'v': returnValue = V; break;
  case 'W': returnValue = W; break;
  case 'w': returnValue = W; break;
  case 'X': returnValue = X; break;
  case 'x': returnValue = X; break;
  case 'Y': returnValue = Y; break;
  case 'y': returnValue = Y; break;
  case 'Z': returnValue = Z; break;
  case 'z': returnValue = Z; break;
  case ' ': returnValue = _; break;
  case '3': returnValue = B2; break;
  case '<': returnValue = TEMP; break;
  case '*': returnValue = FULL; break;
  case '|': returnValue = LINE; break;
  case '_': returnValue = _; break;
  case ':': returnValue = COL; break;
  case '-': returnValue = DASH; break;
  case ')': returnValue = BRA2; break;
  case '%': returnValue = SMILE; break;
  case '.': returnValue = DOT; break;
  case '^': returnValue = COLDOT; break;
  }
  return returnValue;
}

//An array holding the powers of 2 these are used as bit masks when calculating what to display
const int powers[] = {1,2,4,8,16,32,64,128};

//Loads the current scroll state frame into the data[] display array
void
load_sprite()
{
  int currentChar = getChar(message[idx]);
  int nextChar = getChar(message[idx+1]);
  int row, column;

  for(row = 0; row < 8; row++) { // iterate through each row
    data[row] = 0; //reset the row we're working on
    for(column=0; column < 8; column++){ // iterate through each column
      //loads the current charachter offset by offset pixels
     data[row] += ((powers[column] & (letters[currentChar][row] << offset)));
     //loads the next charachter offset by offset pixels
     data[row] += (powers[column] & (letters[nextChar][row] >> (8 - offset) ));
    }
  }
  offset++; // increment the offset by one row
  if (offset == 8) {
    offset = 0;
    idx++;
    if (idx == sizeof(message) - 2) {
      idx = 0;
    }
  } // if offset is 8 load the next charachter pair for the next time through
}

void
show_sprite(int speed2)
{
 int d;
 int iii, column, i, row, bit;
 for(iii = 0; iii < speed2; iii++){                 //show the current frame speed2 times
  for(column = 0; column < 8; column++){            //iterate through each column
   for(i = 0; i < 8; i++){
       OUT_LOW(row_pins[i]);                      //turn off all row pins
   }
   for(i = 0; i < 8; i++){ //Set only the one pin
     if(i == column){
         OUT_LOW(col_pins[i]);}  //turns the current row on
     else{
         OUT_HIGH(col_pins[i]); }//turns the rest of the rows off
   }

   for (row = 0; row < 8; row++) { // iterate through each pixel in the current column
    bit = (data[column] >> row) & 1;
    if (bit == 1) {
      OUT_HIGH(row_pins[row]); //if the bit in the data array is set turn the LED on
    }
   }
   //     BBOS_DELAY_MSEC(delay); //leave the column on for pauseDelay microseconds (too high a delay causes flicker)
   for (d = 0; d < 500; d++);
  }
 }
}

void
update_led_matrix()
{
  load_sprite();
  show_sprite(speed);
}

int
main()
{
  setup();
  while (1) {
    update_led_matrix();
  }
  return 0;
}
