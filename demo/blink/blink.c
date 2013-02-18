#include <propeller.h>

void
blinker_runner()
{
  _DIRA = 1 << 20;
  _OUTA = 1 << 20;
  sleep(1);
  _OUTA = 0x00;
  sleep(1);
}

void
buttons_runner()
{
}
