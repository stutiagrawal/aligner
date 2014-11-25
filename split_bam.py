import runBashCmd
import logging
import argparse
import os
import errno
import setupLog
import time
import multiprocessing

def convert_to_fastq(inpdir, bam_file, uuid, picard_path, logger):

        if(os.path.isdir(inpdir) and os.path.isdir(picard_path)):
            cmd = ['time', 'java','-Xms2G','-Xmx30G', '-jar', '%s' %(os.path.join(picard_path,'picard.jar')), 'SamToFastq',
                    'VALIDATION_STRINGENCY=SILENT', 'MAX_RECORDS_IN_RAM=7500000']
            inp = ['INPUT=%s' %(bam_file), 'FASTQ=%s' %(os.path.join(inpdir,'%s_1.fastq.gz' %(uuid))),
                    'SECOND_END_FASTQ=%s' %(os.path.join(inpdir, '%s_2.fastq.gz' %(uuid)))]
            cmd = cmd + inp

            start_time = time.time()
            exitcode = runBashCmd._do_run(cmd)

            end_time = time.time()

            if exitcode != 0:
                msg = 'Conversion failed for: %s' %(bam_file)
                logger.error(msg)
                logger.info('PICARD_TIME:\t%s\t%s\t%s' %(bamfile, os.path.getsize(bamfile),float(end_time) - float(start_time)))
            else:
                logger.error('Invalid path %s or %s' %(inpdir, picard_path))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='split_bam.py', description='Convert to FASTQ')
    parser.add_argument('bam', help='path to bam file')
    parser.add_argument('picard', help='path to picard')
    parser.add_argument('outdir', help='path to output directory')
    parser.add_argument('uuid', help='UUID for the bam file')
    parser.add_argument('--log_file', default=os.path.join(os.getcwd(),'samToFastq.log'), help='path to log file')

    args = parser.parse_args()

    logger = setupLog.setup_logging(logging.INFO, 'fastq', args.log_file)

    convert_to_fastq(args.outdir, args.bam, args.uuid, args.picard, logger)
