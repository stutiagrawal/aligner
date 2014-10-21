import runBashCmd
import multiprocessing
import os

if __name__ == "__main__":
    reads_1 = '/mnt/cinder/SCRATCH/data/SRR292250_1.fastq'
    reads_2 = '/mnt/cinder/SCRATCH/data/SRR292250_2.fastq'
    ref = '/mnt/cinder/SCRATCH/data/human_g1k_v37_decoy.fasta'
    platform = 'illumina'

    max_proc = int(0.8 * multiprocessing.cpu_count())

    for i in xrange(max_proc, 0, -1):
        log_file = "novo_%s" %(i)
        
	os.system("python align_novoalign.py %s %s %s %s --p %s --log_file %s" %(reads_1, reads_2, ref, platform, i, log_file))
"""
cmd = ['python', 'align_novolaign.py', reads_1, reads_2, ref, platform, '--p', str(i), '--log_file', log_file]
        runBashCmd._do_run(cmd)
"""
