#!/usr/bin/env python
from Bio import SeqIO
from Bio.SeqUtils import GC
import gzip
from datetime import datetime
from sys import argv,exit
from ntpath import basename
start_time = datetime.now()
#print("It took " + str(datetime.now() - start_time) + " long to read and write the GC values")
print("Reading GC values")
if argv[1].endswith('.gz'):
	handle = gzip.open(argv[1])
else:
	handle = open(argv[1])
gc_values = [GC(rec.seq) for rec in SeqIO.parse(handle, "fastq")]
if gc_values==[]:
	exit()
print("It took " + str(datetime.now() - start_time) + " long to read and write the GC values")
print("Writing GC values")

file_writer=open("%s/%s_gc.txt"%(argv[2],basename(argv[1])),"a")
for i in gc_values:
    file_writer.write(str(i)+"\n")

file_writer.close()

print("It took " + str(datetime.now() - start_time) + " long to read and write the GC values")
handle.close()

R_file=open('%s/rgraph.R'%argv[2], 'a')
R_file.write('''
setwd("%s")


data=read.table("%s_gc.txt", header=FALSE)



# calculate the theoretical mean and SD based on GC content that we see
meanDensity <- mean(data$V1)
sdDensity <- sd(data$V1)

# number of observations in input file
nObs<- nrow(data)

# create new normal distribution based on observed values
newDistro <- rnorm(nObs, mean=meanDensity, sd=sdDensity)


# plot the stuff
oriDataDensity <- density(data$V1)
newDensity <- density(newDistro)


# calculate the axis so plots can be overlay
yaxis <- max(oriDataDensity$y, newDensity$y)

pdf(file="%s_gc.pdf")
plot(oriDataDensity, ylim=c(0,yaxis), xlim=c(0,100), col="red", lwd=2, xlab="%% GC Content", main="GC Distribution for %s")
par(new=TRUE)
plot(newDensity, ylim=c(0,yaxis), xlim=c(0,100), col="blue", lwd=2, xaxt="n", yaxt="n", main="", xlab="", ylab="")
legend(x="topright", legend=c("Distribution of GC content", "Theoretical distribution of GC content"), 
       text.col=c("red", "blue"), cex=0.8)
dev.off()
'''%(argv[2], basename(argv[1]), basename(argv[1]).split('.')[0],  basename(argv[1]).split('.')[0]))
R_file.close()


