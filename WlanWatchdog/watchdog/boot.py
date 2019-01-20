# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import main
#import webrepl

#webrepl.start()
machine.freq(80000000)
gc.collect()

