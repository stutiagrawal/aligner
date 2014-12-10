import runBashCmd
import logging
import argparse
import os
import errno
import setupLog
import time

default_logger = logging.getLogger(name='aligner')

def align_snap(index_dir, reads_1, reads_2, output_dir, num_proc, logger=default_logger):
    """Align the paired end reads using snap"""

    genome = "%s" %(os.path.join(index_dir, "Genome"))
    genome_hash = "%s" %(os.path.join(index_dir, "GenomeIndexHash"))
    genome_index = "%s" %(os.path.join(index_dir, "GenomeIndex"))
    overflow_table = "%s" %(os.path.join(index_dir, "OverflowTable"))

    if(os.path.isfile(genome) and os.path.isfile(genome_hash)
            and os.path.isfile(genome_index) and os.path.isfile(overflow_table)):

        cmd = ['time', '/usr/bin/time', 'snap', 'paired', index_dir, reads_1, reads_2]
        out = ['-o', '%s' %(os.path.join(output_dir, "out_SNAP_%s.bam" % num_proc))]
        opt = ['-t', num_proc]

        cmd = cmd + out + opt

        error_msg = "failed to run snap on: %s and %s" %(reads_1, reads_2)
        exitcode = runBashCmd._do_run(cmd)

        if exitcode != 0:
            logger.error(error_msg)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='snap.py', description='Alignment of reads using SNAP')
    parser.add_argument('reads_1', help='path to reads_1.fastq')
    parser.add_argument('reads_2', help='path to reads_2.fastq')
    parser.add_argument('index_dir', help='path to index directory')
    parser.add_argument('outdir', help='path to output directory', default='/mnt/cinder/SCRATCH/data')
    parser.add_argument('--p', help='number of threads to use', default='1')
    parser.add_argument('--log_file', help='name of log file', default='aligner.log')

    args = parser.parse_args()

    logger = setupLog.setup_logging(logging.INFO, 'aligner', args.log_file)

    align_snap(args.index_dir, args.reads_1, args.reads_2, args.outdir, args.p, logger)
