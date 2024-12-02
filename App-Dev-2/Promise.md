In JavaScript, **Promises** are used to handle asynchronous operations, allowing you to work with values that might not yet be available, but will be resolved in the future. A promise can be in one of three states:

- **Pending**: The initial state; the promise is neither resolved nor rejected.
- **Resolved**: The operation was successful, and the promise has a value.
- **Rejected**: The operation failed, and the promise has a reason (error).

A promise is created using the `new Promise()` constructor, where you provide an executor function that takes two arguments: `resolve` and `reject`.

### Example of a Promise:
```javascript
const myPromise = new Promise((resolve, reject) => {
    let success = true;  // Simulating a success or failure condition

    if (success) {
        resolve("Operation successful!");  // Resolve the promise with a value
    } else {
        reject("Something went wrong!");  // Reject the promise with an error message
    }
});
```

### Key Methods for Handling Promises

1. **`then()`**: The `then()` method is used to define what should happen when the promise is resolved (success). It accepts two callbacks:
   - The first callback is called when the promise is resolved (success case).
   - The second callback (optional) is called when the promise is rejected (error case).

```javascript
myPromise
    .then(result => {
        console.log(result);  // Handles the resolved value
    })
    .catch(error => {
        console.log(error);  // Handles any errors from rejection
    });
```

2. **`catch()`**: The `catch()` method is used to handle errors. It acts like the second argument in the `then()` method, but is a cleaner and more explicit way to handle promise rejections.

```javascript
myPromise
    .catch(error => {
        console.log(error);  // Handle promise rejection
    });
```

3. **`finally()`**: The `finally()` method is used to specify code that should run after the promise is settled (whether it is resolved or rejected). It doesn’t receive any arguments, and it’s often used for clean-up actions.

```javascript
myPromise
    .finally(() => {
        console.log("Promise settled (either resolved or rejected).");
    });
```

### Full Example:
```javascript
const myPromise = new Promise((resolve, reject) => {
    let success = false;  // Simulating failure

    if (success) {
        resolve("Success!");
    } else {
        reject("Error occurred.");
    }
});

myPromise
    .then(result => {
        console.log(result);  // This will not be executed since the promise is rejected
    })
    .catch(error => {
        console.error(error);  // This will handle the rejection
    })
    .finally(() => {
        console.log("Promise is settled (done).");
    });
```

### Summary:
- **`resolve(value)`**: Marks the promise as fulfilled, passing the `value`.
- **`reject(error)`**: Marks the promise as failed, passing the `error` or failure reason.
- **`then()`**: Runs a callback when the promise is resolved.
- **`catch()`**: Handles promise rejections (errors).
- **`finally()`**: Executes code after the promise is resolved or rejected, often for cleanup.

Promises allow you to write asynchronous code in a more readable and manageable way, chaining operations and handling errors more easily. 

![Question on Promise from IITM BS Degree](https://github.com/user-attachments/assets/118fa3c9-5df2-4a5e-8074-1d29c5d509e1)



### Now, code Breakdown for the question:

```javascript
new Promise((error, pass) => {
    if (5 === "5") {
        error(5); // This is used to resolve the promise with value 5.
    } else {
        pass(8); // This should reject the promise with value 8.
    }
})
```

### Flow of the Promise Chain:

#### 1. The Promise Constructor:
- **The promise is rejected**, because `5 === "5"` evaluates to `false`, and it calls `error(8)`, which rejects the promise with the value `8`.

#### 2. First `.then()`:
```javascript
.then(d => {
    console.log("Checkpoint 4", d); // This won't be called because the promise was rejected.
    throw new Error(20); // This won't be executed.
    return d * 5; // This won't be executed either.
})
```
- The first `.then()` block doesn't run because the promise was rejected, so it immediately moves to the rejection handler in the next `.then()`.

#### 3. Second `.then()` (Rejection Handler):
```javascript
.then(
    d => { 
        console.log("Checkpoint 2", d); // This doesn't run, as the promise was rejected
        return d;
    },
    d => { 
        console.log("Checkpoint 5", d.message); // Logs "Checkpoint 5 undefined", since `d` is the rejection value (a number, not an error object)
        return d.message * 2; // This will be NaN because d.message is undefined.
    }
)
```
- In this second `.then()`, the **second function** is used because the promise was rejected.
- **`d` here is the rejection value (`8`)**, not an error object.
- Since `8` is a number, it doesn't have a `message` property, so `d.message` is `undefined`.
- Therefore:
  - **`console.log("Checkpoint 5", d.message)` logs "Checkpoint 5 undefined"**.
  - **`return d.message * 2`** results in **`undefined * 2`**, which gives **`NaN`**.

#### 4. `.catch()`:
```javascript
.catch(e => {
    console.log("Checkpoint 3", e.message); // This won't run because the error is handled by the second `then()`.
    return e.message * 2;
})
```
- Since the error was already handled in the rejection handler (`.then()`), this `.catch()` block **does not run**.

#### 5. `.finally()`:
```javascript
.finally(d => {
    console.log("Checkpoint 1", d); // Logs "Checkpoint 1 undefined" because `d` is `undefined` here.
    return d * 5; // Returns NaN because `undefined * 5` is NaN.
})
```
- The `.finally()` block is always executed regardless of whether the promise is resolved or rejected.
- However, in this case, **`d` is `undefined`** because the value from the previous rejection handler was `undefined` (since `d.message * 2` returned `NaN`).
- Therefore:
  - **`console.log("Checkpoint 1", d)`** logs **"Checkpoint 1 undefined"**.
  - **`return d * 5`** results in **`NaN`** because `undefined * 5` is `NaN`.

#### 6. Final `.then()`:
```javascript
.then(d => {
    console.log("Checkpoint 6", d); // Logs "Checkpoint 6 NaN".
    return d * 5; // Returns NaN.
})
```
- The final `.then()` receives the value returned from the `.finally()` block, which is `NaN`.
- Therefore:
  - **`console.log("Checkpoint 6", d)`** logs **"Checkpoint 6 NaN"**.
  - **`d * 5`** results in **`NaN`**, and that's returned.

### Final Output:
- **"Checkpoint 5 undefined"** — because the rejection handler received `8` (a number) and tried to access `d.message`, which is `undefined`.
- **"Checkpoint 1 undefined"** — because `.finally()` received `undefined`.
- **"Checkpoint 6 NaN"** — because `.finally()` returned `NaN`, which is passed into the final `.then()`.

### Conclusion:
- **The promise is rejected** (not resolved) because `5 === "5"` evaluates to `false`, and `pass(8)` is called in the constructor.
- The `.then()` block for resolution is skipped, and the error is caught by the rejection handler in the second `.then()`.
- The `.catch()` block is ignored because the rejection is already handled.
