#Just an idea I'm (Danis) working on. We can chuck it if you guys don't like it
1. Introduction
When the internet first started, it was meant to cater to a specific and limited set of applications. Now, we have reached a point in time when the internet caters to almost --- applications (Source: ). Several of these applications could make use of enhancements made to the IP layer (Layer 3 of the OSI Model, RFC). Adding additional data to this layer like geo tagging, time stamp information etc. can help applications (for example, internet of things applications) to do so much more than what they currently do. Adding location information can help collect and deliver location specific content, form real time location accurate visualisation models for IoT networks etc. Adding time stamp information as tags will allow us to visalize the network in real time. Another additional advantage of including the information as metadata rather than application layer (Layer 7 of the OSI model) payload is that every node becomes aware of this information (routers, and other network nodes can process information only upto layer 3). 

2. Problem Statement
The current layer 3 (IP Layer) of the internet contains only the very basic data tags. This was done for the sake of KISS (Keep It Simple Stupid). But in the modern day, there are many applications which can do so much more if we provide more information as packet tags to them. Our problem statement is directed with this objective in mind. problems we hope to address along the course of this project are:-
a) Implement addition of additional metadata in Layer 3 Packets
b) Address issues of increased overhead not significantly affecting performance
c) Ensure that the IP layer is still compatible with existing hardware (hardware scalablity) 

3. Project Objectives
The project objective is to augment the IP layer (Layer 3) of the internet so that we add Internet of Things functionality augmenting information like location coordinates indicating where the data is collected from, adding time stamp information etc. This will enable us to develop a real time view of the internet of thing system without resorting to external dependencies that utilise a seperate stream of service like GPS services. Certain literature sources refer to a network of this kind as a Location Aware network. Our project stops short of this, by only inserting geo tagging and time stamp information to layer 3 packets for each hop.

4. How do you plan to carry out the project

5. How will you evaluate your project

6. What exactly will be shown during the demo
