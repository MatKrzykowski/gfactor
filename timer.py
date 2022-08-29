import time

from common import echo


def print_time(i, L, t_start):
    t_done = time.time() - t_start
    t_rem = (t_done) * (L - i) / i

    if t_done > 60:
        t_done /= 60
        if t_done > 60:
            t_done /= 60
            if t_done > 24:
                t_done /= 24
                t_done_unit = 'd'
            else:
                t_done_unit = 'h'
        else:
            t_done_unit = 'min'
    else:
        t_done_unit = 's'

    if t_rem > 60:
        t_rem /= 60
        if t_rem > 60:
            t_rem /= 60
            if t_rem > 24:
                t_rem /= 24
                t_rem_unit = 'd'
            else:
                t_rem_unit = 'h'
        else:
            t_rem_unit = 'min'
    else:
        t_rem_unit = 's'

    mes1 = f"Time ellapsed: {t_done:.1f} {t_done_unit}\n\n"
    if i < L:
        mes2 = f"Estimated time remaining: {t_rem:.1f} {t_rem_unit}\n\n"
    else:
        mes2 = "Done"

    echo(mes1)
    echo(mes2)
