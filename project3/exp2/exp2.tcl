# tecl simularion for experiment 2
#
# node 1 (tcp)                            node 4 (tcp)
#      \                                    /
#       \          tcp flow 1 -> 4         /
#       n2 -------------------------------n3
#       /          cbr flow 2 -> 3         \
#      /           tcp flow 5 -> 6          \
# node 5 (tcp)                          node 6 (tcp)

if {$argc != 5} {
    puts "need 5 arguments"
} else {
    # 0 = Reno/Reno, 1 = NewReno/Reno, 2 = Vegas/Vegas, 3 = NewReno/Vegas
    set tcpVersion [lindex $argv 0]
    # range from 1~4 secs, tcp at 5
    set CBRstart {1 + [lindex $argv 2] * 0.001}
    #puts $CBRsize
    set CBRsize [lindex $argv 1]mbps
    #puts $CBRstart
    # 0 is tcp1 first, 1 is tcp2 first
    set TCPorder [lindex $argv 3]
    # number of output file, exp1_num.tr
    set outputNum [lindex $argv 4]
    #puts $outputNum
    #set seed [lindex $argv 4]
}

# set random seed
#$defaultRNG seed $seed

# create network nodes
set ns [new Simulator]

#set namfile [open exp1.nam w]
#$ns namtrace-all $namfile
set outputName "trace_files/exp2_$outputNum.tr"
set tracefile [open $outputName w]
$ns trace-all $tracefile

proc finish {} {
        global ns tracefile tcp1 sink1
        $ns flush-trace
#        close $namfile
        close $tracefile
        set lastACK [$tcp1 set ack_]
        set lastSEQ [$tcp1 set maxseq_]
        set rePKT [$tcp1 set nrexmitpack_]
        set reBYTE [$tcp1 set nrexmitbytes_]
        set sent [$tcp1 set ndatabytes_]
        set ACKed [$sink1 set bytes_]
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
$ns queue-limit $n5 $n2 25
$ns queue-limit $n3 $n6 25

#setup a TCP Reno connection
if {$tcpVersion == 0} {
    set tcp1 [new Agent/TCP/Reno]
    set tcp2 [new Agent/TCP/Reno]
} elseif {$tcpVersion == 1} {
    set tcp1 [new Agent/TCP/Newreno]
    set tcp2 [new Agent/TCP/Reno]
} elseif {$tcpVersion == 2} {
    set tcp1 [new Agent/TCP/Vegas]
    set tcp2 [new Agent/TCP/Vegas]
} elseif {$tcpVersion == 3} {
    set tcp1 [new Agent/TCP/Newreno]
    set tcp2 [new Agent/TCP/Vegas]
} else {
    puts "tcp version number unhandled $tcpVersion"
}
$tcp1 set class_ 0 
#what is this set class thing?
$tcp1 set window_ 1000
$tcp2 set window_ 1000
$ns attach-agent $n1 $tcp1
$ns attach-agent $n5 $tcp2
set sink1 [new Agent/TCPSink]
set sink2 [new Agent/TCPSink]
$ns attach-agent $n4 $sink1
$ns attach-agent $n6 $sink2
$ns connect $tcp1 $sink1
$ns connect $tcp2 $sink2
$tcp1 set fid_ 1
$tcp2 set fid_ 2

#do i do something about FTP here too?
set ftp1 [new Application/FTP]
set ftp2 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp2 attach-agent $tcp2
$ftp1 set type_ FTP
$ftp2 set type_ FTP

#setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null
$udp set fid_ 3

#setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ $CBRsize
$cbr set random_ false

#schedule events for the CBR and FTP agents
if {$TCPorder == 0} {
    $ns at 5.0 "$ftp1 start"
    $ns at 5.0 "$ftp2 start"
} elseif {$TCPorder == 1} {
    $ns at 5.0 "$ftp2 start"
    $ns at 5.0 "$ftp1 start"
}
$ns at $CBRstart "$cbr start"
$ns at 125.0 "$ftp1 stop"
$ns at 125.0 "$ftp2 stop"
$ns at 125.0 "$cbr stop"

#detach tcp and sink agents
$ns at 125.0 "$ns detach-agent $n1 $tcp1 ; $ns detach-agent $n4 $sink1"
$ns at 125.0 "$ns detach-agent $n5 $tcp2 ; $ns detach-agent $n6 $sink2"

#call the finish procedure
$ns at 125.0 "finish"

#print CBR packet size and interval (do i need this?)
puts "CBR packet size = [$cbr set packet_size_]"
puts "CBR interval = [$cbr set interval_]"

#run the simulation
$ns run

