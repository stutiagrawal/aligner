import runBashCmd
import multiprocessing

if __name__ == "__main__":
    reads_1 = '/mnt/cinder/SCRATCH/data/SRR292250_1.fastq'
    reads_2 = '/mnt/cinder/SCRATCH/data/SRR292250_2.fastq'
    ref = '/home/ubuntu/reference/human_g1k_v37_decoy.fasta.gz'
    platform = 'illumina'

    max_proc = int(0.8 * multiprocessing.cpu_count())

    for i in xrange(max_proc, 0, -1):
        log_file = "mosaik_%s" %(i)
        cmd = ['python', 'mosaik.py', reads_1, reads_2, ref, platform, '--p', str(i), '--log_file', log_file]
        runBashCmd._do_run(cmd)
