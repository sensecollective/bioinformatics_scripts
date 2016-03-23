#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import os
from time import time
import datetime
import csv


__author__ = "Raony Guimarães"
__copyright__ = "Copyright 2011, The Exome Pipeline"
__credits__ = ["Raony Guimarães"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Raony Guimarães"
__email__ = "raonyguimaraes@gmail.com"
__status__ = "Production"
		
#run example
#python gatk.py -i alignment/exome.sorted.bam

parser = OptionParser()

parser.add_option("-a", dest="annovar_file",
                  help="CSV Generated by annovar", metavar="ANN")
parser.add_option("-v", dest="vcf_file",
                  help="VCF File Generated by GATK", metavar="VCF")
(options, args) = parser.parse_args()

annovar_file = csv.reader(open(options.annovar_file, "rb"))
header = annovar_file.next()
print header
#self.variants_array = array(list(annovar_file))
# 10 e 11
variants = {}
for line in annovar_file:
    variant = {}
    variant['sift'] = line[10]
    variant['polyphen'] = line[11]
    variant_id = "%s-%s" % (line[15], line[16])
    variants[variant_id] = variant


print len(variants)
vcf_file=open(options.vcf_file, 'r')
out_file=open(options.vcf_file+'.annovar.vcf', 'w')

for line in vcf_file:
	if line.startswith('#'):
	    out_file.writelines(line)
	else:
	    line = line.split('\t')
	    variant_id = "%s-%s" % (line[0], line[1])
	    if variant_id in variants:
		if variants[variant_id]['sift'] != '':
		    line[7] = line[7]+';ANN_SIFT=%s' % (variants[variant_id]['sift'])
		if variants[variant_id]['polyphen'] != '':
		    line[7] = line[7]+';ANN_POLYPHEN=%s' % (variants[variant_id]['polyphen'])
		out_file.writelines("\t".join(line))
	    else:
		out_file.writelines("\t".join(line))




