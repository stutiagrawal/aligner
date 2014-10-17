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

def run_command(cmd, error_msg, program, dataset, logger=default_logger):

    start_time = time.time()
    exitcode = runBashCmd._do_run(cmd)
    end_time = time.time()

    time_in_min = (end_time - start_time)/60.0

    if exitcode != 0:
        logger.error(error_msg)
    logger.info('TIME_%s:\t%s\t%s' %(program, dataset, time_in_min))

def align_mosaik(reads_1, reads_2, reference, platform, num_proc, outdir, ann_p, ann_s, logger=default_logger):

    if(is_valid_input(reads_1, reads_2, reference, platform)):
        ref_file_name = reference.split("/")[-1]
        if(ref_file_name == ''):
            ref_file_name = reference.split("/")[-2]

        ref_build = '%s.dat' %(os.path.join(outdir, ref_file_name))


        if(not(os.path.isfile(ref_build))):
            #Build the reference
            cmd = ['MosaikBuild', '-fr', reference, '-oa' , ref_build]
            error_msg = "Build failed for %s" %(reference)
            program = "MosaikBuild_reference"
            run_command(cmd, error_msg, program, ref_build, logger=default_logger)

        ref_jump = '%s_jump.dat' %(os.path.join(outdir, ref_file_name))

        if not(os.path.isfile("%s_keys.jmp" %ref_jump) and os.path.isfile("%s_meta.jmp" %ref_jump)
                and os.path.isfile("%s_positions.jmp" %ref_jump)):
            #Create the jump database

            assert(os.path.isfile(ref_build))
            cmd = ['MosaikJump', '-ia', ref_build, '-out', ref_jump, '-hs', '15']
            error_msg = "Build failed for jump database %s" %(ref_jump)
            program = 'MosaikJump_reference'
            run_command(cmd, error_msg, program, ref_jump, logger=default_logger)

        sample_name = reads_1.split("/")[-1].split("_")[0]
        reads_build = '%s.dat' %(os.path.join(outdir, sample_name))

        if(not(os.path.isfile(reads_build))):
            #Build the reads

            cmd = ['MosaikBuild', '-q', reads_1, '-q2', reads_2, '-out', reads_build, '-st', platform]
            error_msg = "Build failed for %s and %s" %(reads_1, reads_2)
            program = 'MosaikBuild Reads'
            run_command(cmd, error_msg, program, reads_build, logger=default_logger)

        if(os.path.isfile(ref_build) and os.path.isfile(reads_build)):
            #Align the reads with the reference

            output = "%s_aligned_%s.dat" %(os.path.join(outdir, sample_name), num_proc)
            cmd = ['MosaikAligner', '-in', reads_build, '-out', output, '-ia', ref_build, '-hs', '15', '-mm', '4', '-mhp', '100', '-act', '20', '-j', ref_jump, '-p', num_proc, '-annpe', ann_p, '-annse', ann_s]
            error_msg = "Alignment failed for %s" %(reads_build)
            program = 'MosaikAligner Reads'
            run_command(cmd, error_msg, program, output, logger=default_logger)

if __name__ == "__main__":

        parser = argparse.ArgumentParser(prog='aligner.py', description='Alignment of reads')
        parser.add_argument('reads_1', help='path to reads_1.fastq')
        parser.add_argument('reads_2', help='path to reads_2.fastq')
        parser.add_argument('ref', help='path to reference genome reference.fasta')
        parser.add_argument('platform', help='name of sequencing platform: illumina, 454, helicos, sanger, solid')
        parser.add_argument('--outdir', help='path to output directory', default='/mnt/cinder/SCRATCH/data')
        parser.add_argument('--p', help='number of threads to use', default='1')
        parser.add_argument('--log_file', help='name of log file', default='aligner.log')
        parser.add_argument('--ann_p', help='path to ann file for alignment',
                default='/home/ubuntu/software/MOSAIK/src/networkFile/2.1.26.pe.100.0065.ann')
        parser.add_argument('--ann_s', help='path to ann file for alignment',
                default='/home/ubuntu/software/MOSAIK/src/networkFile/2.1.26.se.100.005.ann')
        args = parser.parse_args()

        logger = setupLog.setup_logging(logging.INFO, 'aligner', args.log_file)

        align_mosaik(args.reads_1, args.reads_2, args.ref, args.platform, args.p, args.outdir, args.ann_p, args.ann_s)
