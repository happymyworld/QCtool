## QC tool
A simple pipeline editor/launcher for common QC operations. It works as a GUI interface (QCtool.py, requires QT4 and pyqt4 to run, can be compiled upon request) and as command-line (QCtool_cmd.py).
In both cases, it needs an input folder (can be the root folder of MiSeq output, or a simple folder containing .fastq files), an output location, and a list of the QC tools to be included in the analysis.
All the main parameters and paths for each of the tools in the pipeline are listed in the settings.txt file, which has to be edited before the first execution.

### To do:
- include Vicky and Alex's report-making scripts
