block_size = 256
memory_size = block_size


# Function to allocate memory to a process based on its size request
def allocate_memory(request_size):
    size = block_size
    allocation_tree = []
    # Keep splitting the block until it is small enough for the request
    while size / 2 >= request_size:
        allocation_tree.append(size)  # Remember the split sizes
        size /= 2  # Split the block into two smaller buddies
    allocation_tree.append(size)  # Add the final block size that matches the request
    return size, allocation_tree  # Return the allocated block size and its split history


# Function to show how memory is currently being used (allocated and free blocks)
def display_memory(free_blocks, allocations):
    print("\nMemory Visualization")
    memory_map = []
    block_number = 1

    # List all allocated blocks
    for process, allocated_size in allocations.items():
        memory_map.append(f"Block {block_number}: Allocated to {process}: {int(allocated_size)} KB")
        block_number += 1

    # List all free blocks
    for block in sorted(free_blocks, reverse=True):
        memory_map.append(f"Block {block_number}: Free Block: {int(block)} KB")
        block_number += 1

    # Print the memory map
    for block in memory_map:
        print(block)
    print("\n" + "=" * 40)  # Add a divider for clarity


# Function to show how memory was split for a specific process, including free blocks
def display_allocation_tree(process, allocation_tree, process_size, free_blocks):
    print(f"\nAllocation Tree for {process} (Process Size: {process_size} KB)")
    level = 0
    # Show each split level as a tree structure for allocated memory
    for size in allocation_tree:
        print("  " * level + f"|-- {int(size)} KB")  # Indent each level of the tree
        level += 1
    print("\nFree Blocks Tree:")
    level = 0
    for size in sorted(free_blocks, reverse=True):
        print("  " * level + f"|-- Free: {int(size)} KB")
    print("=" * 40)  # Add a divider for clarity


# Main function to simulate the Buddy System
def simulate_buddy_system(requests):
    free_blocks = {block_size}  # Start with one big free block of memory
    allocations = {}

    for idx, req in enumerate(requests, 1):
        allocated_size, allocation_tree = allocate_memory(req)  # Try to allocate memory for the request
        buddy_details = []

        # Check if there is enough memory for the request
        if not any(free_block >= allocated_size for free_block in free_blocks):
            print(f"\nProcess {idx} requesting {req} KB cannot be allocated due to insufficient memory.")
            return allocations

        # If the exact block size is available, allocate it
        if allocated_size in free_blocks:
            free_blocks.remove(allocated_size)
        else:
            # Otherwise, keep splitting larger blocks until the required size is found
            while allocated_size not in free_blocks:
                buddy_details.append(allocated_size)  # Keep track of the splits
                allocated_size *= 2  # Find the next larger block
            free_blocks.remove(allocated_size)  # Remove the large block
            free_blocks.add(allocated_size / 2)  # Add two smaller blocks as buddies
            free_blocks.add(allocated_size / 2)
            buddy_details.append(allocated_size / 2)

        allocations[f"P{idx}"] = allocated_size  # Record the allocated block
        print(f"\nAllocated {int(allocated_size)} KB for Process {idx}")
        print(
            f"   Buddies Allocated: {', '.join(map(lambda x: str(int(x)) + ' KB', buddy_details)) if buddy_details else f'{int(allocated_size)} KB'}")
        print(f"   Free Blocks: {sorted(map(int, free_blocks), reverse=True)}")

        # Show the memory map and how the memory was split, including free blocks
        display_memory(sorted(free_blocks, reverse=True), allocations)
        display_allocation_tree(f"P{idx}", allocation_tree, req, free_blocks)

    return allocations


# Input and Simulation
# Ask the user for memory requests for three processes
a, b, c = map(int, input("Enter three numbers separated by commas: ").split(','))
requests = [a, b, c]  # Store the memory requests in a list
print("\nSimulating Buddy System...\n")
allocations = simulate_buddy_system(requests)  # Start the simulation

