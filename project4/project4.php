<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Project 4: CS 5700 Fundamentals of Computer Networking: David Choffnes, Ph.D.</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Homepage for David Choffnes, Ph.D., Assistant Professor in Computer Science at Northeastern University">
<meta name="author" content="">
<!--script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-2830907-1']);
  _gaq.push(['_setDomainName', 'choffnes.com']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script-->



<!-- Le styles -->
<link href="https://david.choffnes.com/bootstrap/css/bootstrap.css" rel="stylesheet">
<style>
body {
    padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
	padding-bottom: 60px;
}

/* Custom container */
.navbar {
margin: 0 auto;
    max-width: 800px;
}
.container-narrow {
margin: 0 auto;
    max-width: 800px;
}
.container-narrow > hr {
margin: 30px 0;
}
.navbar-footer-grey {
margin: 0 auto;
    max-width: 800px;
	text-align: center;
}
.navbar .btn-navbar {
	float: left;
}
.nav-red {
color: red;
}
.floatrightconf{
float:right;
position: relative;
right: -120px;
margin-left:-100px;
color:#6633CC;
}
.pub {
  width: 675px;
}
.pub > li {
  width: 650px;
}
</style>
<link href="https://david.choffnes.com/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">


<!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
<!--[if lt IE 9]>
<script src="https://david.choffnes.com/bootstrap/js/html5shiv.js"></script>
<![endif]-->

<!-- Fav and touch icons -->
<link rel="apple-touch-icon-precomposed" sizes="144x144" href="https://david.choffnes.com/bootstrap/ico/apple-touch-icon-144-precomposed.png">
<link rel="apple-touch-icon-precomposed" sizes="114x114" href="https://david.choffnes.com/bootstrap/ico/apple-touch-icon-114-precomposed.png">
<link rel="apple-touch-icon-precomposed" sizes="72x72" href="https://david.choffnes.com/bootstrap/ico/apple-touch-icon-72-precomposed.png">
<link rel="apple-touch-icon-precomposed" href="bootstrap/ico/apple-touch-icon-57-precomposed.png">
<link rel="shortcut icon" href="https://david.choffnes.com/bootstrap/ico/favicon.png">
</head>

<body data-spy="scroll" data-target=".classnavbar">
<div class="navbar navbar-inverse navbar-fixed-top">

        
<div class="navbar-inner">
<div class="container-fluid">
<button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
<center><span>MENU &nbsp;</span><div style="display: inline-block">
<span class="icon-bar"></span>
<span class="icon-bar"></span>
<span class="icon-bar"></span></div></center>
</button>
<div class="nav-collapse collapse">
<ul class="nav">
<li ><a class="brand" href="https://david.choffnes.com/">David Choffnes</a></li>



<li class="dropdown ">
<a id="drop1" href="#" role="button" class="dropdown-toggle" data-toggle="dropdown">RESEARCH<b class="caret"></b></a>
<ul class="dropdown-menu" role="menu" aria-labelledby="drop1">
<li role="presentation"><a id="item1" role="menuitem" tabindex="-1" href="https://david.choffnes.com/projects.php">Projects</a></li>
<li role="presentation"><a role="menuitem" tabindex="-1" href="https://david.choffnes.com/pubs.php">Publications</a></li>
<li role="presentation"><a role="menuitem" tabindex="-1" href="https://david.choffnes.com/vision.php">Vision</a></li>
<li role="presentation"><a role="menuitem" tabindex="-1" href="https://david.choffnes.com/collaborators.php">Collaborators</a></li>
<li role="presentation"><a role="menuitem" tabindex="-1" href="https://david.choffnes.com/software.php">Software</a></li>
<li role="presentation"><a role="menuitem" tabindex="-1" href="https://david.choffnes.com/support.php">Support</a></li>
</ul>
</li>

<li class="dropdown ">
<a id="drop1" href="#" role="button" class="dropdown-toggle" data-toggle="dropdown">TEACHING<b class="caret"></b></a>
<ul class="dropdown-menu" role="menu" aria-labelledby="drop1">
<li role="presentation"><a role="menuitem" tabindex="-1" href="https://david.choffnes.com/classes/cs4700fa20/">Current (CS4700/5700 Fall 20)</a></li>
<li role="presentation"><a role="menuitem" tabindex="-1" href="https://david.choffnes.com/teaching.php#past">Past</a></li>
</ul>
</li>

<li class="dropdown ">
<a id="drop1" href="#" role="button" class="dropdown-toggle" data-toggle="dropdown">ABOUT<b class="caret"></b></a>
<ul class="dropdown-menu" role="menu" aria-labelledby="drop1">
<li role="presentation"><a role="menuitem" tabindex="-1" href="https://david.choffnes.com/about.php">Brief</a></li>
<li role="presentation"><a role="menuitem" tabindex="-1" href="https://david.choffnes.com/about.php#cv">CV</a></li>
<li role="presentation"><a role="menuitem" tabindex="-1" href="https://david.choffnes.com/rec.php">Extracurricular</a></li>
<li role="presentation"><a role="menuitem" tabindex="-1" href="https://david.choffnes.com/news.php">News</a></li>
</ul>

</li>

<IC WEBSITES</h2>
As with project 2, you should not test your program against public web servers. <b>Only test
your program against pages hosted by CCIS</b>. When you are testing your program, you will almost
certainly send packets with invalid IP and TCP headers. These packets may trigger security warnings
if you send them to public websites, e.g. the website adiinistrator may think someone is trying
to hack their site with spoofed packets.
</p><p>
You may test your program against Fakebook, or against this assignment page. We have also created
some large files full of random bytes that you can use to stress-test your implementation:
<a href="2MB.log">2 MB file</a>, <a href="10MB.log">10 MB file</a>, <a href="50MB.log">50 MB file</a>.
</p><p>
<h2>High Level Requirements</h2>
You goal is to write a program called <i>rawhttpget</i> that takes one command line parameter
(a URL), downloads the associated web page or file, and saves it to the current directory.
The command line syntax for this program is:
</p><p>
./rawhttpget [URL]
</p><p>
An example invocation of the program might look like this:
</p><p>
./rawhttpget http://david.choffnes.com/classes/cs4700fa20/project4.php
</p><p>
This would create a file named <i>project4.php</i> in the current directory containing the
downloaded HTML content. If the URL ends in a slash ('/') or does not include any path, then
you may use the default filename
<i>index.html</i>. For example, the program would generate a file called <i>index.html</i> if
you ran the following command:
</p><p>
./rawhttpget http://www.ccs.neu.edu
</p><p>
<b>The file created by your program should be exactly the same as the original file on the server</b>.
You can test whether your file and the original are identical by using <i>wget</i> or a web
browser to download the file, and then comparing the file generated by your program and the original
using <i>md5sum</i> or <i>diff</i>. Do not include extra info in your generated file, like HTTP headers
or line breaks.
</p><p>
Since the point of this assignment is not to focus on HTTP, there are many things your program
does not need to handle. Your program does not need to support HTTPS. Your program does not need to
follow redirects, or handle HTTP status codes other than 200. In the case of a non-200 status
code, print an error to the console and close the program. Your program does not need to follow
links or otherwise parse downloaded HTML.
</p><p>
<h2></h2>
<h2>Low Level Requirements</h2>
The primary challenge of this assignment is that you <b>must</b> use raw sockets. A raw socket
is a special type of socket that bypasses some (or all) of the operating system's network stack.
For example, in C a socket of type SOCK_STREAM/IPPROTO_RAW bypasses the operating system's IP and TCP/UDP layers.
In your program, you will need to create two raw sockets: one for receiving packets and one for
sending packets. The receive socket must be of type <strike>SOCK_STREAM/IPPROTO_IP</strike> SOCK_RAW/IPPROTO_TCP; the send socket must be
of type SOCK_RAW/IPPROTO_RAW. The reason you need two sockets has to do with some quirks of the Linux kernel.
The kernel will not deliver any packets to sockets of type SOCK_STREAM IPPROTO_RAW, thus your code will
need to bind to the IPPROTO_IP interface to receive packets. However, since you are required to
implement TCP and IP, you must send on a SOCK_RAW/IPPROTO_RAW socket.
</p><p>
There are many tutorials online for doing raw socket programming. I recommend
<a href="http://www.binarytides.com/raw-sockets-c-code-linux/">Silver Moon's tutorial</a> as 
a place to get started. That tutorial is in C; Python also has native support for raw socket
programming. However, <b>not all languages support raw socket programming</b>. Since many of
you program in Java, I will allow the use of the <a href="http://www.savarese.com/software/rocksaw/">
RockSaw Library</a>, which enables raw socket programming in Java.
</p><p>
When you start to write your program, you will immediately notice that thee on a stock Ubuntu Linux 20.04 machine,
so keep that in mind when developing your code and setting up your VM. <b>Do not develop your program
on Windows or OSX</b>: the APIs for raw sockets on those systems are incompatible with Linux, and thus
your code will not work when we grade it.
</p><p>
For most of you, the VM option will probably be easiest. There are many
<a href="https://ubuntu.tutorials24x7.com/blog/how-to-install-ubuntu-on-windows-using-vmware-workstation-player">tutorials</a>
on how to do this.
If you use Windows, you will need a (free) copy of VMWare Player, as well as an ISO of Ubuntu. Once
you have your VM set up, you will need to install development tools. Exactly what you need will depend
on what language you want to program in. There are ample instructions online explaining how to install
gcc, Java, and Python-dev onto Ubuntu.
</p><p>
<h2>Modifying IP Tables</h2>
Regardless of whether you are developing on your own copy of Linux or in a VM, you will need to make
one change to <i>iptables</i> in order to complete this assignment. You must set a rule in <i>iptables</i>
that drops outgoing TCP RST packets, using the following command:
<pre>% iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP</pre>
To understand why you need this rule, think about how the kernel behaves when it receives unsolicited TCP
packets. If your computer receives a TCP packet, and there are no open ports waiting to receive that packet,
the kernel generates a TCP RST packet to let the sender know that the packet is invalid. However, in your
case, your program is using a raw socket, and thus the kernel has no idea what TCP port you are using. So,
the kernel will erroneously respond to packets destined for your program with TCP RSTs. You don't want
the kernel to kill your remote connections, and thus you need to instruct the kernel to drop outgoing
TCP RST packets. You will need to recreate this rule each time your reboot your machine/VM.
</
131f
p><p>
<h2>Debugging</h2>
Debugging raw socket code can be very challenging. You will need to get comfortable with 
<a href="http://www.wireshark.org/">Wireshark</a>
in order to debug your code. Wireshark is a packet sniffer, and can parse all of the relevent fields
from TCP/IP headers. Using Wireshark, you should be able to tell if you are formatting outgoing
packets correctly, and if you are correctly parsing incoming packets.
</p><p>
<h2>Language</h2>
You can write your code in whatever language you choose, as long as your code compiles and runs
on a <b>stock</b> copy of Ubuntu 20.04 <b>on the command line</b>.
</p><p>
Be aware that many languages do not support development using raw sockets. I am making an
explicit exception for Java, allowing the use of the RockSaw library. If you wish to program in
a language (other than Java) that requires third party library support for raw socket programming,
<b>ask me for permission</b> before you start development.
</p><p>
As usual, do not use libraries that are not installed by default on Ubuntu 20.04
(with the exception of RockSaw). Similarly, your code must compile and run on the
command line. You may use IDEs (e.g. Eclipse) during development, but do not turn in your IDE
project without a Makefile. Make sure you code has <b>no dependencies</b> on your IDE.
</p><p>
<h2>Submitting Your Project</h2>
Before turning in your project, you and your partner(s) must register your group. To register yourself
in a group, execute the following script:
<pre>$ /course/cs5700f20/bin/register project4 [team name]</pre>
This will either report back success or will give you an error message.  If you have trouble registering,
please contact the course staff. <b>You and your partner(s) must all run this script with the same 
[team name]</b>. This is how we know you are part of the same group.
</p><p>
To turn-in your project, you should submit your (thoroughly documented) code along with three other files:
<ul><li>A Makefile that compiles your code.</li>
<li>A plain-text (no Word or PDF) README file. In this file, you should briefly describe your high-level
approach, what TCP/IP features you implemented, and any challenges you faced. <b>You must also include a detailed description of which student worked on which part of the code.</b></li>
<li>If your code is in Java, you must include a copy of the RockSaw library.</li>
</ul>
Your README, Makefile, source code, external libraries, etc. should all be placed in a directory. You submit
your project by running the turn-in script as follows:
<pre>$ /course/cs5700f20/bin/turnin project4 [project directory]</pre>
[project directory] is the name of the directory with your submission. The script will print out every
file that you are submitting, so make sure that it prints out all of the files you wish to submit!

<b>Only one group member needs to submit your project.</b> Your group may submit as many times as you
wish; only the last submission will be graded, and the time of the last submission will determine
whether your assignment is late.
</p><p>
<h2>Grading</h2>
This project is worth 16 points. You will receive full credit if 1) your code compiles, runs, and correctly
downloads files over HTTP, 2) you have not used any illegal libraries, and 3) you use the correct type of
raw socket. All student code will be scanned by plagarism
detection software to ensure that students are not copying code from the Internet or each other.
</p><p>
5 points will be awarded for each of the three protocols you must implement, i.e. 5 points for HTTP,
5 ponts for TCP, and 5 points for IP. 1 point will be awarded for your documentation. Essentially,
6 points should be easy to earn; the other 10 are the challenge. 
</p><p>
<h2>Extra Credit</h2>
There is an opportunity to earn 2 extra credit points on this assignment. To earn these points, you must
use and AF_PACKET raw socket in your program, instead of a SOCK_RAW/IPPROTO_RAW socket. An AF_PACKET raw socket
bypasses the operating systems layer-2 stack as well at layers 3 and 4 (TCP/IP). This means that your
program must build Ethernet frames for each packet, as well as IP and TCP headers. You can assume that
we will only test your code on machines with Ethernet connections, i.e. you do not need to worry about
alternative layer-2 protocols like Wifi or 3G. This extra credit will be quite challenging, since it will
involve doing MAC resolution with ARP requests. We have not discussed ARP in class, and you will need
to learn about and handle this protocol on your own. Essentially, the challenge is to figure out the
MAC address of the gateway, since this information needs to be included in the Ethernet header.
</p><p>
<b>If you complete the extra credit, make sure to mention this in your README.</b> Explain how you
implemented Ethernet functionality, and any additional challenges your faced (e.g. ARP).
</p>


4fa
    
    
    </div> <!-- /container -->
    
    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document s