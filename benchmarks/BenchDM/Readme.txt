= Installation =

Install ggplot2 in R:

    install.packages("ggplot2")

= Getting started =

Launch R and import the ggplot2 library like this:

    library(ggplot2)

Then copy paste the code from the following sections into R.

library(ggplot2)
features <- read.csv("/Users/maik/grape.buildout/benchmarks/BenchDM/input/execute_3.log", sep="\t")
#features <- subset(features, Seconds <=20000)
 
# Show Memory percentage over time
qplot(Seconds/60/60, MemPercent, data=features)

# Show Memory used percentage over time
qplot(Seconds/60/60, MemUsed/1024, data=features)

# Show number of proccesses over time
qplot(Seconds/60/60, Processes, data=features)

# Show load over time
qplot(Seconds/60/60, Load1, data=features)

# Show swap over time
qplot(Seconds/60/60, SwapPercent, data=features)

# Show swap over time
qplot(Seconds/60/60, T1, data=features)

qplot(Seconds/60/60, (X0 + X1 + X2 + X3 + X4 + X5 + X6 + X7)/8, data=features)

# Show CPUs
cpus <- melt(features, id = "Seconds", measure = c("X0", "X1", "X2", "X3","X4", "X5", "X6", "X7"))
qplot(Seconds/60/60, value, colour=variable, data=cpus)
qplot(Seconds/60/60, value, data=emp) + facet_grid(variable ~ .)
 
 

library(ggplot2)
processes <- read.csv("/Users/maik/grape.buildout/benchmarks/BenchDM/intermediate/seconds_program_3.txt", sep="\t")
qplot(Seconds/60/60, program, data=processes) + facet_grid(process ~ .)

library(ggplot2)
cumulative <- read.csv("/Users/maik/grape.buildout/benchmarks/BenchDM/intermediate/process_cumulative_seconds_3.txt", sep="\t")
ordered <- within(cumulative, {process <- reorder(process, cumulative_seconds)})
qplot(cumulative_seconds / 60 / 60, process, data=ordered)

library(ggplot2)
cumulative <- read.csv("/Users/maik/grape.buildout/benchmarks/BenchDM/intermediate/process_cumulative_seconds_3.txt", sep="\t")
non_overlap <- subset(cumulative, process != 'overlap' & process != 'gzip' & process != '')
ordered <- within(non_overlap, {process <- reorder(process, cumulative_seconds)})
qplot(cumulative_seconds / 60 / 60, process, data=ordered)
