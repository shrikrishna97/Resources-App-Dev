
### Q1
Suppose a client machine **A** is communicating with a data center **B** located 8000 km away from **A**.  
The speed of light in the cable is assumed to be `2 × 10^8 m/s` (instead of the default `3 × 10^8 m/s`).  

How long will it take for a **request to reach the server and for the response to return back to the client (round-trip time)**?

---

**Solution:**

```
             request ————>>———————
   Client A                          Server B
             <<—————— response ————
   Distance between A and B = 8000 km
```
Latency is the delay between sending a request and receiving a response in a system.

- Formula:  
  Speed = Distance / Time  
  Time = Distance / Speed  

- One-way distance:  
  8000 × 1000 = 8 × 10^6 m  

- One-way time:  
  (8 × 10^6) / (2 × 10^8) = 0.04 s  

- Round-trip time (RTT):  
  2 × 0.04 = 0.08 s  

- Converting to milliseconds:  
  0.08 × 1000 = **80 ms**  

**Final Answer:**  
Latency (Round-trip latency) = **80 ms**

---

### Q2
Suppose a client machine **C** is communicating with a data center **D** located 15000 km away from **C**.  
Assume that the TCP connection has already been established and is kept alive.  
If the client can send a **new request only after receiving an acknowledgement (response) for the previous request**, what is the maximum number of successful requests that can be completed from **C** to **D** in one second?  

(Assume the speed of light in cable is `2 × 10^8 m/s`.)

---

**Solution:**

```
             request ————>>———————
   Client C                          Server D
             <<—————— response ————
   Distance between C and D = 15000 km
```

- Formula:  
  Speed = Distance / Time  
  Time = Distance / Speed  

- One-way distance:  
  15000 × 1000 = 1.5 × 10^7 m  

- One-way time:  
  (1.5 × 10^7) / (2 × 10^8) = 0.075 s = 75 ms  

- Round-trip time (RTT):  
  2 × 75 ms = 150 ms  

- Number of requests possible in 1 second (1000 ms):  
  1000 / 150 ≈ 6.67  

- Only **6 full request–response cycles** can complete in 1 second.  
  (The 7th would not complete within the 1 second window.)  

**Final Answer:**  
Maximum number of successful requests = **6 per second**

---

### Q3
Consider a client located **6000 km** from a server.  
The client makes a request through a **cable**, but after the request reaches the server, the cable breaks and the **response is sent to the client via air**.  

If this change of medium causes an **additional delay of 75 ms at the server**, how long will the client have to wait before receiving the response?  

(Assume speed of light in cable = `2 × 10^8 m/s`, in air = `3 × 10^8 m/s`)  

*Assume RTT = latency.*

---

**Solution:**


```
             request ————>>——————— (cable)
   Client A                          Server B
             <<—————— response ———— (air)
   Distance between A and B = 6000 km
```

- **Formula:**  
  Latency = request time + response time + server delay  

- **Request time (cable):**  
  6000 × 1000 / 2 × 10^8 = 0.03 s = 30 ms  

- **Response time (air):**  
  6000 × 1000 / 3 × 10^8 = 0.02 s = 20 ms  

- **Server delay:**  
  75 ms = 0.075 s  ( you can choose either second or milisecond , but we will prefer `ms` in this course)

- **Total client wait (latency):**  
  0.03 + 0.02 + 0.075 = 0.125 s = 125 ms  

**Final Answer:**  
Client wait time (latency) = **125 ms**

---

### Q4
A client **C** and a server **S**, located 12,000 km apart, are connected via a cable.  
A request is sent by the client to the server, but while sending back the response, the cable breaks and the response is now sent via **air**.  

This change in medium causes an **additional delay of 20 ms**.  

As compared to the Round Trip Time (RTT) of the healthy network, the RTT of the faulty system would ________.  

**Options:**  
A. Increase  
B. Decrease  
C. Remain Same  
D. Insufficient Information  

(Speed of light in cable = `2 × 10^8 m/s`, in air = `3 × 10^8 m/s`)  

---

**Solution:**

```
             request ————>>——————— (cable)
   Client C                          Server S
             <<—————— response ———— (air)
   Distance between A and B = 12000 km
```

- **Case 1: Healthy network**  
  RTT1 = 2 × (12000 × 1000 / 2 × 10^8) = 0.12 s = 120 ms  

- **Case 2: Faulty network**  
  RTT2 = (12000 × 1000 / 2 × 10^8) + (12000 × 1000 / 3 × 10^8) + 0.02  
       = 0.06 + 0.04 + 0.02  
       = 0.12 s = 120 ms  

**Conclusion:**  
RTT remains the same despite the medium change and server delay.  

**Answer:** C. Remain Same


---

### Q5
A network has a bandwidth of **8 Gbps**. A client wants to send **5000 requests per second** over this network.   
What should be the size of **each request** in **MB**?  

*Use the following unit conversions:*  
- 1 Byte = 8 bits  
- 1 KB = 1000 Bytes  
- 1 MB = 1000 KB  
- 1 GB = 1000 MB  

**Hint:** Bandwidth can be expressed in two equivalent ways:  
1. Bandwidth = Number of requests per second × Size of each request  
2. Bandwidth = Total data per second

---

**Solution:**

**Step 1: Using requests/sec × size per request**

Bandwidth (bits/sec) = Number of requests/sec × Size per request (bits)

8,000,000,000 = 5000 × S  

S = 8,000,000,000 / 5000 = 1,600,000 bits  

Convert to bytes:  

S = 1,600,000 / 8 = 200,000 Bytes = 0.2 MB

---

**Step 2: Using total data per second analogy**

Total data sent per second = 5000 requests × 0.2 MB/request = 1000 MB = 1 GB/s  

Convert to bits/sec:  

1 GB = 8 × 10^9 bits → Bandwidth = 8 Gbps  

This confirms the calculation matches the given network bandwidth.

---

**Answer:**  
Size of each request = **0.2 MB**

---

**Key Takeaway:**  
- **Bandwidth = requests/sec × size per request** → emphasizes **request granularity**  
- **Bandwidth = total data per second** → emphasizes **total data transferred**  
Both approaches give the same result and help understand network data flow.


---

### Q8

<img width="912" height="786" alt="image" src="https://github.com/user-attachments/assets/59e0282a-4eeb-4ccb-8aff-4066bc81da3c" />


---

## Step 1: Extract bandwidth segments from the graph

From the graph you shared:

* **0–4 h:** BW = 8 Mb/s
* **4–8 h:** BW = 6 Mb/s
* **8–12 h:** BW = 8 Mb/s
* **12–16 h:** BW = 2 Mb/s
* **16–20 h:** BW = 2 Mb/s
* **20–24 h:** BW = 4 Mb/s

*(These are the orange steps in the graph representing total network usage.)*

---

## Step 2: Formula

```
 Data= Bandwidth × Time
```

* Time must be in seconds (1 hour = 3600 s)
* Convert bits to bytes by dividing by 8

---

## Step 3: Calculate total data

```
Segment 0–4 h: 8 Mb/s × 4 h = 8 × 4 × 3600 = 115,200 Mb
Segment 4–8 h: 6 Mb/s × 4 h = 6 × 4 × 3600 = 86,400 Mb
Segment 8–10 h: 8 Mb/s × 2 h = 8 × 2 × 3600 = 57,600 Mb
Segment 10–14 h: 2 Mb/s × 4 h = 2 × 4 × 3600 = 28,800 Mb
Segment 14–18 h: 4 Mb/s × 4 h = 4 × 4 × 3600 = 57,600 Mb
```

Sum = 115,200 + 86,400 + 57,600 + 28,800 + 57,600 = 345,600 Mb

Convert to **MB**: 345,600 / 8 = 43,200 MB = 43.2 GB 

* **Answer: 43.2 GB** → **Option C** is correct.

---



