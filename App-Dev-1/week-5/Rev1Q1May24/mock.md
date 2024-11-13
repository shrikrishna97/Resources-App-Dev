### 1. **Question 4 (Encoding Calculation)**
**Question:**
Let \( L = \{'a', 'b', 'c', 'd', 'A', 'B', 'C', 'D', '0', '1', ' '\} \) be a complete character set. If a document that uses fixed encoding for all characters is created using the character set \( L \) and has a disk size of 2 Kilobytes, the number of characters in the document would be_______. [Take 1 Byte = 8 bits, 1 KB = 1000 Bytes, 1 MB = 1000 Kilobytes and so on.]

**Solution:**
1. The character set \( L \) contains **11** unique characters.
2. To encode these characters, we need **4 bits** (since \( 2^4 = 16 \) is the smallest power of 2 that can represent all 11 characters).
3. The document size is **2 Kilobytes (KB)**, which is **2000 bytes** (since 1 KB = 1000 Bytes).
4. Each character takes **4 bits** to store.
5.  \( 1 \) byte = \( 8 \) bits , so each byte can store **2 characters**.
6. Therefore, in **2000 bytes**, we can store:
   2000 * 2 = 4000 characters.

**Answer:** 4000 characters.

---

### 2. **Question 6 (Number of Characters with 5 Bits)**
**Question:**
How many characters can be encoded using 5 bits?

**Solution:**
- With **5 bits**, the total number of combinations we can represent is:
  ```math
  2^5 = 32
  ```
  
- So, **32 characters** can be encoded using **5 bits**.

**Answer:** 32

---

### 3. **Question 7 (ASCII Representation Calculation)**
**Question:**
How many bits are required to represent ‘IITM’ in ASCII?

**Solution:**

1. **Each** character in **ASCII** is represented by **8 bits** (1 byte).
2. The string **‘IITM’** has **4 characters**.
3. Total bits required:
   ```math
   4 * 8 = 32 \, \text{bits}
   ```
   

**Answer:** 32 bits

---

### 4. **Question 8 (Data Consumption Calculation)**
**Question:**
A mobile client starts from and is cruising away continuously at 60 kmph from the network tower whose network range is 40 km and bandwidth is 120 Mbps. How much data (in Gigabytes) will be consumed by the client who is continuously using the entire bandwidth before completely moving out of the network?

*Take 1 Byte = 8 bits, 1 KB = 1000 Bytes, 1 MB = 1000 Kilobytes and so on.*  
*Consider the speed of light in air to be 3 x 10^8 m/sec.*  

---

#### Solution:

**Step 1: Understanding the Problem**  
The mobile client moves away from the network tower at a speed of 60 kmph. The range of the network is 40 km, so once the client moves beyond 40 km, it will lose the network signal. The bandwidth available is 120 Mbps (megabits per second).

**Step 2: Calculate Time in the Network Range**  
Since the client is moving away from the tower at 60 kmph and the range is 40 km:

- Speed = 60 kmph
- Distance = 40 km

We need to calculate the time taken to move out of the range:
```math
\text{Time (t)} = \frac{\text{Distance}}{\text{Speed}} = \frac{40 \, \text{km}}{60 \, \text{kmph}}
```
Converting time to seconds:
```math
\text{Time} = \frac{40}{60} \, \text{hours} = \frac{2}{3} \, \text{hours} = \frac{2}{3} \times 3600 \, \text{seconds} = 2400 \, \text{seconds}
```
**Step 3: Calculate Data Consumption**  
The client is using the full bandwidth of 120 Mbps for the entire duration of 2400 seconds.

- Bandwidth (BW) = 120 Mbps (megabits per second)

To find the total data consumed:
```math
\text{Data (in megabits)} = \text{BW} \times \text{Time} = 120 \, \text{Mbps} \times 2400 \, \text{s} = 288000 \, \text{Mb}
```
**Step 4: Convert Megabits to Gigabytes**  
Since we have data in megabits (Mb), let's convert it to Gigabytes (GB):

1 Byte = 8 bits, so 1 MB (Megabyte) = 8 Mb (Megabits).
```math
\text{Data (in megabytes)} = \frac{288000 \, \text{Mb}}{8} = 36000 \, \text{MB}
```


And since 1 GB = 1000 MB:

```math
\text{Data (in GB)} = \frac{36000 \, \text{MB}}{1000} = 36 \, \text{GB}
```
The data consumed by the client before moving out of the network is **36 GB**.

**Answer: C. 36**

