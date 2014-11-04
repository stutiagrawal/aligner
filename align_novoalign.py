import runBashCmd
import logging
import argparse
import os
import errno
import setupLog
import time
import multiprocessing

default_logger = logging.getLogger(name='aligner')

def is_valid_input(reads_1, reads_2, reference, platform):

    if(not(os.path.isfile(reads_1))):
        return False
    if(not(os.path.isfile(reads_2))):
        return False
    if(not(os.path.isfile(reference))):
        return False
    if(not(platform in ['454', 'illumina', 'helicos', 'sanger', 'solid'])):
        return False
    return True

def run_command(cmd, error_msg, program, dataset, logger=default_logger, output=None):

    start_time = time.time()
    exitcode = runBashCmd._do_run(cmd, output_file=output)
    end_time = time.time()

    time_in_min = (end_time - start_time)/60.0

    if exitcode != 0:
        logger.error(error_msg)
    logger.info('TIME_%s:\t%s\t%s' %(program, dataset, time_in_min))

def align_novo(reads_1, reads_2, reference, platform, num_proc, outdir, logger=default_logger):

    if(is_valid_input(reads_1, reads_2, reference, platform)):
        #Build the reference genome
        ref_name = reference.split("/")[-1]
        if(ref_name == ""):
            ref_name = reference.split("/")[-2]

        if platform == "illumina" or platform == "454":
            ref_build = "%s.nix" %(os.path.join(outdir, ref_name))
            cmd = ['time', '/usr/bin/time', 'novoindex', ref_build, reference]
        elif platform == "solid":
            ref_build = "%s.ncx" %(os.path.join(outdir, ref_name))
            cmd = ['time', '/usr/bin/time', 'novoindex', '-c', ref_build, reference]
        error_msg = "build failed for %s" %(ref_build)
        if(not(os.path.isfile(ref_build))):
            run_command(cmd, error_msg, "Novoindex", reference)

        #Align the reads
        if(os.path.isfile(ref_build)):
            sample_name = reads_1.split("/")[-1].split("_")[0]
            align_file = "%s_novo.sam" %(os.path.join(outdir, sample_name))
            aln = open(align_file, "w")
            cmd = ['time', '/usr/bin/time', 'novoalign','-o', 'SAM', '-c', num_proc, '-d', ref_build, '-f', reads_1, reads_2]
            error_msg = "Alignment failed for novoalign: %s" %(sample_name)
            run_command(cmd, error_msg, "novoalign", sample_name, output=aln)
            aln.close()

if __name__ == "__main__":

        parser = argparse.ArgumentParser(prog='align_novolaign.py', description='Alignment of reads using novoalign')
        parser.add_argument('reads_1', help='path to reads_1.fastq')
        parser.add_argument('reads_2', help='path to reads_2.fastq')
        parser.add_argument('ref', help='path to reference genome reference.fasta')
        parser.add_argument('platform', help='name of sequencing platform: illumina, 454, helicos, sanger, solid')
        parser.add_argument('--outdir', help='path to output directory', default='/mnt/cinder/SCRATCH/data')
        parser.add_argument('--p', help='number of threads to use', default='1')
        parser.add_argument('--log_file', help='name of log file', default='aligner.log')
        args = parser.parse_args()

        logger = setupLog.setup_logging(logging.INFO, 'aligner', args.log_file)

        align_novo(args.reads_1, args.reads_2, args.ref, args.platform, args.p, args.outdir)
