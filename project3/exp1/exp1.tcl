# tecl simularion for experiment 1
#
# node 1 (tcp)                            node 4 (tcp)
#      \                                    /
#       \          tcp flow 1 -> 4         /
#       n2 -------------------------------n3
#       /          cbr flow 2 -> 3         \
#      /                                    \
# node 5 (idle?)                          node 6 (idle?)

if {$argc != 4} {
    puts "need 4 arguments"
} else {
    # 0 = Tahoe, 1 = Reno, 2 = newReno, 3 = Vegas
    set tcpVersion [lindex $argv 0]
    # range from 1~10 Mgbs
    set CBRstart [lindex $argv 1]
    #puts $CBRsize
    # either 5 seconds before or after or at the same as TCP; TCP at 5.0 const
    set CBRsize [lindex $argv 2]mbps
    #puts $CBRstart
    # number of output file, exp1_num.tr
    set outputNum [lindex $argv 3]
    #puts $outputNum
}


# create network nodes
set ns [new Simulator]

#set namfile [open exp1.nam w]
#$ns namtrace-all $namfile
set outputName "trace_files/exp1_$outputNum.tr"
set tracefile [open $outputName w]
$ns trace-all $tracefile

proc finish {} {
        global ns tracefile tcp sink
        $ns flush-trace
#        close $namfile
        close $tracefile
        set lastACK [$tcp set ack_]
        set lastSEQ [$tcp set maxseq_]
        set rePKT [$tcp set nrexmitpack_]
        set reBYTE [$tcp set nrexmitbytes_]
        set sent [$tcp set ndatabytes_]
        set ACKed [$sink set bytes_]
        puts stdout "final ack: $lastACK, final seq num: $lastSEQ, acked bytes: $ACKed, total sent bytes (ex header): $sent, retransmitted bytes (ex header): $reBYTE, retransmitted packets: $rePKT"
        exit 0
}

#create 6 nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#create links between the nodes
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n2 $n5 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail

#node position for NAM
$ns duplex-link-op $n1 $n2 orient left-up
$ns duplex-link-op $n3 $n4 orient right-up

#set up queue limit for tcp
$ns queue-limit $n1 $n2 25
$ns queue-limit $n2 $n3 25
$ns queue-limit $n3 $n4 25

#setup a TCP Reno connection
if {$tcpVersion == 0} {
    set tcp [new Agent/TCP]
} elseif {$tcpVersion == 1} {
    set tcp [new Agent/TCP/Reno]
} elseif {$tcpVersion == 2} {
    set tcp [new Agent/TCP/Newreno]
} elseif {$tcpVersion == 3} {
    set tcp [new Agent/TCP/Vegas]
} else {
    puts "tcp version number unhandled $tcpVersion"
}
$tcp set class_ 0 
#what is this set class thing?
$tcp set window_ 1000
$ns attach-agent $n1 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set fid_ 1

#do i do something about FTP here too?
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP

#setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null
$udp set fid_ 2

#setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ $CBRsize
$cbr set random_ false

#schedule events for the CBR and FTP agents
$ns at 5.0 "$ftp start"
$ns at $CBRstart "$cbr start"
$ns at 125.0 "$ftp stop"
$ns at 125.0 "$cbr stop"

#detach tcp and sink agents
$ns at 125.0 "$ns detach-agent $n1 $tcp ; $ns detach-agent $n4 $sink"

#call the finish procedure
$ns at 125.0 "finish"

#print CBR packet size and interval (do i need this?)
puts "CBR packet size = [$cbr set packet_size_]"
puts "CBR interval = [$cbr set interval_]"

#run the simulation
$ns run

