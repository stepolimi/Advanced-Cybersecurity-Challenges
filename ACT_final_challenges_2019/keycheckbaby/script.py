import claripy
import angr

p=angr.Project('./keycheck_baby')

simfile = angr.SimPackets('input')

st = p.factory.entry_state(stdin=simfile);
sm = p.factory.simulation_manager(st)
sm.explore(find=lambda s: b"Your input looks" in s.posix.dumps(1))
for s in sm.found:
    print(s.posix.dumps(0))

#flag = flag{y0u_d4_qu33n_0f_cr4ck1ngz}




