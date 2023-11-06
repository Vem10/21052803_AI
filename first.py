import numpy as np
from PIL import Image, ImageDraw
import random

# Step 1: Generate a canvas with the same dimensions as the input image.
def create_canvas(image_path):
    input_image = Image.open(image_path)
    canvas = Image.new("RGBA", input_image.size)
    return canvas

# Step 2: Generate a population of random squares.
def generate_population(canvas, N):
    population = []
    for _ in range(N):
        # Randomly generate square parameters: (x, y, size, color, opacity)
        x = random.randint(0, canvas.width)
        y = random.randint(0, canvas.height)
        size = random.randint(10, 100)  # You can adjust the size range
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        opacity = random.randint(50, 255)  # You can adjust the opacity range
        square = (x, y, size, color, opacity)
        population.append(square)
    return population

# Step 3: Perform crossover (you can experiment with different techniques).
def crossover(parent1, parent2):
    # Choose crossover points (e.g., splitting the square parameters in half).
    split_point = len(parent1) // 2
    child = parent1[:split_point] + parent2[split_point:]
    return child

# Step 4: Mutation (you can experiment with mutation strategies).
def mutate(square, mutation_rate):
    mutated_square = list(square)
    for i in range(2, len(square)):
        if random.random() < mutation_rate:
            if i == 2:  # Mutation for size
                mutated_square[i] = random.randint(10, 100)  # Adjust the size range
            elif i == 3:  # Mutation for color
                mutated_square[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            else:  # Mutation for opacity
                mutated_square[i] = random.randint(50, 255)  # Adjust the opacity range
    return tuple(mutated_square)

# Step 5: Selection (you can experiment with different selection methods).
# Step 5: Selection (you can experiment with different selection methods).
def select_best_squares(population, image, n):
    population_with_scores = []

    for square in population:
        canvas_copy = image.copy()
        draw = ImageDraw.Draw(canvas_copy)
        x, y, size, color, opacity = square
        left_top = (x, y)
        right_bottom = (x + size, y + size)
        fill_color = color + (opacity,)
        draw.rectangle([left_top, right_bottom], fill=fill_color)
        score = compare_images(canvas_copy, "ai\task-2\pop.png" )
        population_with_scores.append((square, score))

    population_with_scores.sort(key=lambda x: x[1])
    best_squares = [square for square, _ in population_with_scores[:n]]
    return best_squares


# Additional function for evaluating fitness (Objective Function).
def compare_images(image1, image2):
    # Open the second image and convert it to a NumPy array
    image2 = Image.open(image2)
    np_image2 = np.array(image2)

    # Convert the first image to a NumPy array
    np_image1 = np.array(image1)

    # Compute Mean Squared Error (MSE)
    mse = ((np_image1 - np_image2) ** 2).mean()
    return mse

# Main Genetic Algorithm loop
def genetic_algorithm(image_path, num_squares, num_generations, mutation_rate):
    input_image = Image.open(image_path)
    canvas = create_canvas(image_path)
    current_population = generate_population(canvas, num_squares)

    for generation in range(num_generations):
        # Perform crossover
        new_population = []
        while len(new_population) < num_squares:
            parent1 = random.choice(current_population)
            parent2 = random.choice(current_population)
            child = crossover(parent1, parent2)
            new_population.append(child)

        # Perform mutation
        mutated_population = [mutate(square, mutation_rate) for square in new_population]

        # Select the best squares
        current_population = select_best_squares(mutated_population, input_image, num_squares)

    # Visualize the final result (optional)
    final_canvas = canvas.copy()
    draw = ImageDraw.Draw(final_canvas)
    for square in current_population:
        draw.rectangle(square, fill=square[3] + (square[4],))
    final_canvas.show()

# Example usage
# genetic_algorithm("C:\Users\KIIT\OneDrive\Desktop\experiment_documents\lab\PL\Labs\5th sem\daa\ai\task-2\pop.png", num_squares=50, num_generations=100, mutation_rate=0.2)

# Example usage with double backslashes
genetic_algorithm("C:\\Users\\KIIT\\OneDrive\\Desktop\\experiment_documents\\lab\\PL\\Labs\\5th sem\\daa\\ai\\task-2\\pop.png", num_squares=50, num_generations=100, mutation_rate=0.2)
