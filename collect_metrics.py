import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import multiprocessing

def collect_metrics(dirname, program):
    max_proc = max(32, multiprocessing.cpu_cout())

    threads = [0] * max_proc
    time_elapsed = [0] * max_proc
    cpu_time = [0] * max_proc
    user_time = [0] * max_proc
    mem_time = [0] * max_proc

    for filename in os.listdir(dirname):
        metric = str()
        if(filename.startswith(program) and not(filename.endswith(".py"))):
                filename = os.path.join(dirname, filename)
                fp = open(filename, "r")

                for line in fp:
                    if("user" in line and "system" in line):
                        metric = line

                metric = metric.split()
                if(len(metric) >= 9):
                    user = float(metric[3].replace("user", ""))/3600.0

                    system = float(metric[4].replace("system", ""))/3600.0

                    elapsed = metric[5].replace("elapsed", "")
                    if not (elapsed == "0:00.00"):
                        (h, m, s) = metric[5].replace("elapsed", "").split(":")
                        elapsed = (float(h)*3600 + float(m)*60 + float(s))/3600.0
                    else:
                        elapsed = 0.00

                    cpu = metric[6].replace("%CPU", "")
                    if(cpu == "?"):
                        cpu = 0

                    mem = metric[8].replace("maxresident)k", "")
                    num_threads = filename.split("_")[-1]

                pos = int(num_threads) - 1
                threads[pos] = int(num_threads)
                time_elapsed[pos] = elapsed
                cpu_time[pos] = float(cpu)
                user_time[pos] = float(user)
                mem_time[pos] = float(mem)

    #elapsed_line, = plt.plot(threads, time_elapsed, 'bs')
    cpu_line, = plt.plot(threads, cpu_time, 'rs')
    #user_line, = plt.plot(threads, user_time, 'g--')
    #plt.legend([elapsed_line, cpu_line, user_line], ['elapsed', 'cpu', 'user'])
    plt.legend([cpu_line], ['cpu'])
    plt.savefig("%s_timing.png" %(program))
    plt.clf()

    #print "%s\t%s\t%s\t%s\t%s\t%s" %(num_threads, user, system, elapsed, cpu, mem)

collect_metrics(".", "novo")
