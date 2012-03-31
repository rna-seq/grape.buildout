#!/usr/bin/env python
#
# $Id$
#
# Copyright (c) 2012, Maik Roeder.
#
# Copyright (c) 2009, Jay Loden, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Extends top to make a benchmark.

Author: Maik Roeder maikroeder@gmail.com
"""

"""
A clone of top / htop.

Author: Giampaolo Rodola' <g.rodola@gmail.com>
"""

import os
import sys
if os.name != 'posix':
    sys.exit('platform not supported')
import time
from datetime import datetime, timedelta
import psutil

BENCHMARK = []
BENCHMARK_HEADER = []
BENCHMARK_FILE = open("bench.log", "w")
BENCHMARK_START = datetime.now()
BENCHMARK_CURSES = False

procs = [p for p in psutil.process_iter()]  # the current process list

def poll(interval):
    # add new processes to procs list; processes which have gone
    # in meantime will be removed from the list later
    cpids = [p.pid for p in procs]
    for p in psutil.process_iter():
        if p.pid not in cpids:
            procs.append(p)

    # sleep some time
    time.sleep(interval)

    procs_status = {}
    # then retrieve the same info again
    for p in procs[:]:
        try:
            p._username = p.username
            p._nice = p.nice
            p._meminfo = p.get_memory_info()
            p._mempercent = p.get_memory_percent()
            p._cpu_percent = p.get_cpu_percent(interval=0)
            p._cpu_times = p.get_cpu_times()
            p._name = p.name
            try:
                procs_status[str(p.status)] += 1
            except KeyError:
                procs_status[str(p.status)] = 1
        except psutil.NoSuchProcess:
            procs.remove(p)

    # return processes sorted by CPU percent usage
    processes = sorted(procs, key=lambda p: p._cpu_percent, reverse=True)
    return (processes, procs_status)

def print_header(procs_status):
    """Print system-related info, above the process list."""
    BENCHMARK = []
    if len(BENCHMARK_HEADER) == 0:
        needs_header = True
        BENCHMARK_HEADER.append('Seconds')
    else:
        needs_header = False
    timedelta = datetime.now() - BENCHMARK_START
    BENCHMARK.append(str(timedelta.days * 24 * 60 * 60 + timedelta.seconds))
    
    # cpu usage
    for cpu_num, perc in enumerate(psutil.cpu_percent(interval=0, percpu=True)):
        # Add the header info to the BENCHMARK_HEADER
        if needs_header:
            BENCHMARK_HEADER.append(str(cpu_num))
        # Add all percentages for the cpu usage
        BENCHMARK.append("%5s" % perc)

    # physmem usage (on linux we include buffers and cached values
    # to match htop results)
    phymem = psutil.phymem_usage()
    buffers = getattr(psutil, 'phymem_buffers', lambda: 0)()
    cached = getattr(psutil, 'cached_phymem', lambda: 0)()
    used = phymem.total - (phymem.free + buffers + cached)
    if needs_header:
        BENCHMARK_HEADER.append('MemPercent')
        BENCHMARK_HEADER.append('MemUsed')
        BENCHMARK_HEADER.append('MemTotal')
    BENCHMARK.append("%5s" % str(phymem.percent))
    BENCHMARK.append("%6s" % str(int(used / 1024 / 1024)))
    BENCHMARK.append("%s" % str(int(phymem.total / 1024 / 1024)))
    
    # swap usage
    vmem = psutil.virtmem_usage()
    if needs_header == 0:
        BENCHMARK_HEADER.append('SwapPercent')
        BENCHMARK_HEADER.append('SwapUsed')
        BENCHMARK_HEADER.append('SwapTotal')
    BENCHMARK.append("%5s" % str(vmem.percent))
    BENCHMARK.append("%6s" % str(int(vmem.used / 1024 / 1024)))
    BENCHMARK.append("%s" % str(int(vmem.total / 1024 / 1024)))

    # processes number and status
    st = []
    for x, y in procs_status.items():
        if y:
            st.append("%s=%s" % (x, y))
    st.sort(key=lambda x: x[:3] in ('run', 'sle'), reverse=1)
    
    if needs_header:
        BENCHMARK_HEADER.append('Processes')
        BENCHMARK_HEADER.append('Running')
        BENCHMARK_HEADER.append('Sleeping')
    BENCHMARK.append("%s" % len(procs))
    if 'running' in st:
        BENCHMARK.append("%s" % st.split(' ').split('=')[-1])
    else:
        BENCHMARK.append("0")
    if "sleeping" in st:
        BENCHMARK.append("%s" % st.split('=')[-1])
    else:
        BENCHMARK.append("0")
    
    
    # load average, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.BOOT_TIME)
    av1, av2, av3 = os.getloadavg()
    line = " Load average: %.2f %.2f %.2f  Uptime: %s" \
            % (av1, av2, av3, str(uptime).split('.')[0])

    if needs_header:
        BENCHMARK_HEADER.append('Load1')
        BENCHMARK_HEADER.append('Load2')
        BENCHMARK_HEADER.append('Load3')
        # Now write the header
        BENCHMARK_FILE.write("%s\n" % '\t'.join(BENCHMARK_HEADER))
    BENCHMARK.append("%.2f" % av1)
    BENCHMARK.append("%.2f" % av2)
    BENCHMARK.append("%.2f" % av3)

    BENCHMARK_FILE.write("%s\n" % '\t'.join(BENCHMARK))


def refresh_window(procs, procs_status):
    """Print results on screen by using curses."""
    print_header(procs_status)

def main():
    try:
        interval = 0
        while 1:
            args = poll(interval)
            refresh_window(*args)
            interval = 6
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    main()
