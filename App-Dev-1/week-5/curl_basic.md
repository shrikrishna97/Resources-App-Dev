When getting started with `curl`, there are a few basic and commonly used commands that can be quite helpful. These commands will cover a wide range of common use cases, from simple GET requests to more complex interactions with APIs:

### 1. **Basic GET Request**
   - **Command**: `curl <URL>`
   - **Purpose**: Fetches the content of the specified URL.
   - **Example**:
     ```
     curl https://example.com
     ```
   - This retrieves the content of the webpage at `https://example.com` and prints it to the terminal.

### 2. **GET with Verbose Output**
   - **Command**: `curl -v <URL>`
   - **Purpose**: Shows detailed information about the request and response, including headers.
   - **Example**:
     ```
     curl -v https://example.com
     ```
   - **Use Case**: Useful for debugging HTTP request issues and seeing detailed headers in the request and response.

### 3. **Follow Redirects**
   - **Command**: `curl -L <URL>`
   - **Purpose**: Follow HTTP `3xx` redirects.
   - **Example**:
     ```
     curl -L http://example.com
     ```
   - **Use Case**: Use this when a URL redirects to another location, and you want `curl` to automatically follow the redirect and get the final response.

### 4. **Download a File**
   - **Command**: `curl -O <URL>`
   - **Purpose**: Saves the file at the specified URL to the current directory, keeping the original filename.
   - **Example**:
     ```
     curl -O https://example.com/file.zip
     ```
   - **Use Case**: Handy when you want to download files directly to your local machine.

### 5. **Custom Headers**
   - **Command**: `curl -H "Header: value" <URL>`
   - **Purpose**: Adds custom headers to the request.
   - **Example**:
     ```
     curl -H "Authorization: Bearer <token>" https://api.example.com/data
     ```
   - **Use Case**: Often used when interacting with APIs that require authentication or specific headers.

### 6. **Send Data with POST**
   - **Command**: `curl -X POST -d "param1=value1&param2=value2" <URL>`
   - **Purpose**: Sends data to the server using a POST request.
   - **Example**:
     ```
     curl -X POST -d "username=user&password=pass" https://example.com/login
     ```
   - **Use Case**: Useful when submitting form data or interacting with APIs.

### 7. **Send JSON Data**
   - **Command**: `curl -X POST -H "Content-Type: application/json" -d '{"key": "value"}' <URL>`
   - **Purpose**: Sends JSON data with a `POST` request.
   - **Example**:
     ```
     curl -X POST -H "Content-Type: application/json" -d '{"username": "user", "password": "pass"}' https://example.com/api/login
     ```
   - **Use Case**: This is commonly used when interacting with JSON-based RESTful APIs.

### 8. **Store Output to a File**
   - **Command**: `curl <URL> -o <filename>`
   - **Purpose**: Saves the output to a specified file.
   - **Example**:
     ```
     curl https://example.com -o output.html
     ```
   - **Use Case**: This saves the content of `https://example.com` to `output.html` instead of displaying it in the terminal.

### 9. **Include HTTP Headers in Output**
   - **Command**: `curl -i <URL>`
   - **Purpose**: Fetches the response and includes the HTTP headers in the output.
   - **Example**:
     ```
     curl -i https://example.com
     ```
   - **Use Case**: Useful if you want to see both the headers and the response body together.

### 10. **Upload a File**
   - **Command**: `curl -X POST -F "file=@path/to/file" <URL>`
   - **Purpose**: Uploads a file to a server.
   - **Example**:
     ```
     curl -X POST -F "image=@/path/to/image.jpg" https://example.com/upload
     ```
   - **Use Case**: This is helpful when you need to upload files through APIs that support `multipart/form-data`.

### 11. **Check Response Time**
   - **Command**: `curl -w "@curl-format.txt" -o /dev/null -s <URL>`
   - **Purpose**: Allows you to measure different aspects of the request timing (like DNS lookup, connection time).
   - **Example**:
     ```
     curl -w "Time: %{time_total}\n" -o /dev/null -s https://example.com
     ```
   - **Use Case**: Useful for performance testing and analyzing the time taken for each step of a request.

### 12. **Get HTTP Status Code Only**
   - **Command**: `curl -s -o /dev/null -w "%{http_code}" <URL>`
   - **Purpose**: Outputs only the HTTP status code.
   - **Example**:
     ```
     curl -s -o /dev/null -w "%{http_code}" https://example.com
     ```
   - **Use Case**: Useful when you want to check if a URL is accessible and returns a specific HTTP status code (e.g., `200` for OK).

### Summary Table:

| **Command**          | **Description**                                          |
|----------------------|----------------------------------------------------------|
| `curl <URL>`         | Basic GET request.                                       |
| `curl -v <URL>`      | Verbose output with headers.                             |
| `curl -L <URL>`      | Follow redirects.                                        |
| `curl -O <URL>`      | Download a file with its original name.                  |
| `curl -H`            | Add custom headers.                                      |
| `curl -X POST`       | Send a POST request.                                     |
| `curl -X POST -d`    | Send form data with a POST request.                      |
| `curl -X POST -H "Content-Type: application/json" -d` | Send JSON data.         |
| `curl <URL> -o <filename>` | Save output to a file.                             |
| `curl -i <URL>`      | Include headers in the response.                         |
| `curl -F`            | Upload a file to a server.                               |
| `curl -w`            | Display timing details of the request.                   |
| `curl -s -o /dev/null -w` | Get HTTP status code only.                          |

These commands cover most of the common scenarios you'll encounter when working with `curl`. As you get more familiar with `curl`, you may discover additional flags and options that are helpful for more advanced use cases.