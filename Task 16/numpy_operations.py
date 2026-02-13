import numpy as np
import time

print("=== NumPy Operations Demonstration ===\n")

# 1 & 2. Create Arrays of Different Dimensions
# 1D Array
arr1 = np.array([1, 2, 3, 4, 5])

# 2D Array
arr2 = np.array([[1, 2, 3],
                 [4, 5, 6]])

# 3D Array
arr3 = np.array([[[1, 2], [3, 4]],
                 [[5, 6], [7, 8]]])

print("1D Array:\n", arr1)
print("\n2D Array:\n", arr2)
print("\n3D Array:\n", arr3)

# 3. Mathematical Operations
print("\nMathematical Operations:")
print("Addition:", arr1 + 5)
print("Multiplication:", arr1 * 2)
print("Square:", arr1 ** 2)

# 4. Broadcasting Example
print("\nBroadcasting Example:")
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])

vector = np.array([10, 20, 30])

broadcast_result = matrix + vector
print(broadcast_result)

# 5. Statistical Functions
print("\nStatistical Functions:")
print("Mean:", np.mean(arr1))
print("Median:", np.median(arr1))
print("Standard Deviation:", np.std(arr1))
print("Sum:", np.sum(arr1))
print("Max:", np.max(arr1))
print("Min:", np.min(arr1))

# 6. NumPy vs Python List Performance Comparison
size = 1000000

python_list = list(range(size))
numpy_array = np.arange(size)

start = time.time()
python_result = [x * 2 for x in python_list]
end = time.time()
print("\nPython List Time:", end - start)

start = time.time()
numpy_result = numpy_array * 2
end = time.time()
print("NumPy Array Time:", end - start)

# 7. Generate Random Data
print("\nRandom Data:")
random_array = np.random.rand(3, 3)
print(random_array)

# 8. Optimize Calculations (Vectorization)
large_array = np.arange(1000000)

start = time.time()
optimized = large_array * 5
end = time.time()
print("\nOptimized Vectorized Calculation Time:", end - start)

# 9. Visualize Array Structure
print("\nArray Structure Info:")
print("Shape:", arr2.shape)
print("Dimensions:", arr2.ndim)
print("Data Type:", arr2.dtype)
print("Size:", arr2.size)
