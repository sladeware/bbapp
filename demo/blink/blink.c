/*
 * http://www.bionicbunny.org/
 */

#include "bb/os.h"
#include BBOS_PROCESSOR_FILE(pins.h)

#define BUTTONS 0xFF

void
blinker_runner()
{
  struct bbos_message* msg;
  uint16_t i;
  uint16_t mask;
  if ((msg = bbos_receive_message()) != NULL) {
    for (i = 0, mask = *((uint16_t*)msg->payload); i < 8; mask >>= 1, i++) {
      if (mask & 1) {
        DIR_OUTPUT(i + 16);
        OUT_HIGH(i + 16);
      } else {
        OUT_LOW(i + 16);
      }
    }
    bbos_delete_message(msg);
    return;
  }
  /* Request buttons bits */
  if ((msg = bbos_request_message(BUTTON_DRIVER)) != NULL) {
    msg->label = ARE_BUTTONS_PRESSED;
    *((uint16_t*)msg->payload) = BUTTONS;
    bbos_send_message(msg);
  }
}
