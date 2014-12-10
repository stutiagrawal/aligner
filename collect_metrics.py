import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import multiprocessing
import argparse

def create_graph(x_axis_data, y_axis_data, line_label, fig_name, x_axis_label = "", y_axis_label = ""):
    line, = plt.plot(x_axis_data, y_axis_data, 'rs')
    plt.legend([line],[line_label])
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.savefig(fig_name)
    plt.clf()

def collect_metrics(dirname, program):
    max_proc = max(32, multiprocessing.cpu_count())

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
                print metric
		if(len(metric) >= 9):
                    user = float(metric[3].replace("user", ""))/3600.0

                    system = float(metric[4].replace("system", ""))/3600.0

                    elapsed = metric[5].replace("elapsed", "")
                    if not (elapsed == "0:00.00"):
			if("." not in elapsed):
			    h, m , s = elapsed.split(":")
                        else:
			    elapsed = elapsed.replace(".", ":")
			    h = 0
			    m,s,ms = elapsed.split(":")
			elapsed = (float(h)*3600 + float(m)*60 + float(s))/3600
                    else:
                        elapsed = 0.00

                    cpu = metric[6].replace("%CPU", "")
                    if(cpu == "?"):
                        cpu = 0

                    mem = metric[8].replace("maxresident)k", "")
                    num_threads = filename.split("_")[-1]

		pos = int(num_threads) - 1
                threads[pos] = int(num_threads)
                time_elapsed[pos] = (user + system)/int(num_threads)
                cpu_time[pos] = float(cpu)
                user_time[pos] = float(user)
                mem_time[pos] = float(mem)
    for i in xrange(len(threads)):
        print "%s\t%s\t%s\t%s\t%s" %(threads[i], time_elapsed[i], cpu_time[i], user_time[i], mem_time[i])
    create_graph(threads, time_elapsed, "Elapsed time", "%s_elapsed" %(program), "No. of threads", "Time(h)")
    create_graph(threads, cpu_time, "CPU time", "%s_CPU_time" %(program), "No. of threads", "Time(h)")
    create_graph(threads, user_time, "User_time", "%s_user_time" %(program), "No. of threads", "Time(h)")
    create_graph(threads, mem_time, "MEM_used", "%s_mem_used" %(program), "No. of threads", "Memory(K)")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='collect_metrics.py', description='Plot graphs')
    parser.add_argument('dirname', default=".", help='path to directory with log files')
    parser.add_argument('program', help='Tool used to generate results')
    args = parser.parse_args()

    collect_metrics(args.dirname, args.program)

