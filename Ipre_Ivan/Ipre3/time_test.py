import time  # Import the time module to measure precise time

def busy_wait_us(us):
    # Convert microseconds to seconds and add it to the current time
    # This gives us the target end time
    end = time.perf_counter() + us / 1_000_000

    # Loop until the current time reaches the end time
    while time.perf_counter() < end:
        pass  # This is a "busy wait" — doing nothing but checking the time

# Test loop
for i in range(5):
    print(i)           # Print the current loop index
    busy_wait_us(1)  # Wait for 100 microseconds before the next iteration

start = time.perf_counter()
busy_wait_us(100)  # Intended wait: 100 µs
end = time.perf_counter()

print(f"Actual wait: {(end - start)*1e6:.2f} µs")