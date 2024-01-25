from scipy.optimize import fminbound
from rocketcea.cea_obj_w_units import CEA_Obj


def optimizemr(C: CEA_Obj, pc: float, eps: float, optmode: int) -> float:
    """
    #### Optimize Mixture Ratio at defined expansion area ratio.
    `optmode == 1`: Maximize vacuum specific impulse
    `optmode == 2`: Maximize specific impulse at optimum expansion
    `optmode == 3`: Maximize sea level specific impulse
    """
    if optmode == 1:
        f = lambda x: -C.get_Isp(Pc=pc, MR=x, eps=eps)
        
    elif optmode == 2:

        def f(x: float) -> float:
            pe = pc / C.get_PcOvPe(Pc=pc, MR=x, eps=eps)
            return -C.estimate_Ambient_Isp(Pc=pc, MR=x, eps=eps, Pamb=pe)[0]

    elif optmode == 3:
        f = lambda x: -C.estimate_Ambient_Isp(Pc=pc, MR=x, eps=eps, Pamb=101325)[0]

    return fminbound(f, 0.5, 15)


def optimizermr_at_pe(C: CEA_Obj, pc: float, pe: float, optmode: int) -> float:
    """
    #### Optimize Mixture Ratio at constant exit pressure.
    `optmode == 1`: Maximize vacuum specific impulse
    `optmode == 2`: Maximize specific impulse at optimum expansion
    `optmode == 3`: Maximize sea level specific impulse
    """
    if optmode == 1:

        def f(x: float) -> float:
            eps = C.get_eps_at_PcOvPe(Pc=pc, MR=x, PcOvPe=pc / pe)
            return -C.get_Isp(Pc=pc, MR=x, eps=eps)

    elif optmode == 2:

        def f(x: float) -> float:
            eps = C.get_eps_at_PcOvPe(Pc=pc, MR=x, PcOvPe=pc / pe)
            return -C.estimate_Ambient_Isp(Pc=pc, MR=x, eps=eps, Pamb=pe)[0]

    elif optmode == 3:

        def f(x: float) -> float:
            eps = C.get_eps_at_PcOvPe(Pc=pc, MR=x, PcOvPe=pc / pe)
            return -C.estimate_Ambient_Isp(Pc=pc, MR=x, eps=eps, Pamb=101325)[0]

    return fminbound(f, 0.5, 15)