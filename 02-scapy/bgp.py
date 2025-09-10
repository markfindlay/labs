from scapy.all import *
from scapy.contrib import bgp
import socket
import time 
import threading

def bgp_server(quit_server: threading.Event):
    s=socket.socket()
    s.connect(("10.255.255.2",179))
    ss=StreamSocket(s,Raw)
    BGPO = bgp.BGPOpen()
    BGPH = bgp.BGPHeader()
    bgp_capability_MP_v4_unicast = bgp.BGPCapMultiprotocol()
    bgp_capability_MP_v4_unicast.afi=1
    bgp_capability_MP_v4_unicast.safi=1
    bgp_capability_MP_v4_unicast.reserved=00
    bgp_open = BGPH/BGPO
    bgp_open.my_as=1
    bgp_open.hold_time=90
    bgp_open.bgp_id="10.255.255.1"
    bgp_open.opt_params=[bgp.BGPOptParam(param_value=bgp_capability_MP_v4_unicast)]
    result = ss.sr(bgp_open)
    print(result)
    result = ss.sr(bgp.BGPKeepAlive())
    print(result)
    keepalive_timer = time.time()
    while True:
        print("Start of loop.")
        if quit_server.is_set():
            print("Received server stop event...")
            ss.close()
            sys.exit()
        try:
            print(ss.recv())
            if time.time() - keepalive_timer > 30:
                keepalive_timer = time.time()
                ss.sr(bgp.BGPKeepAlive())
        except EOFError as e:
            ss.close()
            print(f"End of stream - exception thrown. {e}")
            sys.exit()
        time.sleep(0.5)

def main():
    quit_server = threading.Event()
    bgp_thread = threading.Thread(target=bgp_server, args=(quit_server, ))
    bgp_thread.start()
    print("BGP started. Type quit to end")
    time.sleep(2)
    while True:
        cmd = input(">")
        if cmd == "quit":
            print("Sending stop signal to BGP thread...")
            quit_server.set()
            print("Waiting for BGP thread...")
            bgp_thread.join()
            break

if __name__ == "__main__":
    main()