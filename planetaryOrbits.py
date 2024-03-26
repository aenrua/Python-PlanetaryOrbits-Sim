# https://fiftyexamples.readthedocs.org/en/latest/gravity.html - Code that I used as a basis

import math
import matplotlib.pyplot as plt
import turtle
from turtle import *

g = 6.6743e-11 # Gravitational constant

# !Scale
au = (149.6e6 * 1000) # 149.6 million km (distance from Earth to Sun) in meters
scale = 75 / au

max_step = 620 # Maximum number of simulation steps (total for Jupiter to complete 1 orbit)

file = open("Projects/Simulation/planetaryOrbits.txt", "w") # Open a text file in write mode, which stores the simulation data (also creates it if it doesn't exist)

# !Representation of celestial bodies
class Body(Turtle):
	name = "Body"
	mass = None
	vx = vy = 0.0 # Starting velocity in x and y
	px = py = 0.0 # Starting position in x and y

	def attraction(self, other): # Method to calculate the gravitational attraction between two bodies
		if self is other: # Report an error if other object is same as itself
			raise ValueError(f"Attraction of object {self.name} to itself requested")
		# Distance of other body
		sx, sy = self.px, self.py
		ox, oy = other.px, other.py
		dx = (ox - sx) # Difference in x coordinates between two bodies
		dy = (oy - sy) # Difference in y coordinates between two bodies
		d = math.sqrt(dx**2 + dy**2) # Calculate the Euclidean distance between two bodies

		if d == 0: # Report error if distance is 0
			raise ValueError(f"Collision between objects {self.name} and {other.name}")

		f = g * self.mass * other.mass / (d**2) # Force of attraction

		# Direction of force
		theta = math.atan2(dy, dx) # Determine the angle between the x-axis and the line connection two bodies
		fx = math.cos(theta) * f # Determine how much of the total gravitational force acts in the horizontal direction
		fy = math.sin(theta) * f # Determine how much of the total gravitational force acts in the vertical direction
		return fx, fy

def update_info(step, bodies): # Define the main simulation loop where calculations for updating positions and velocities are performed
	print(f"Week {step}") # Print information about the celestial bodies at a each step
	for body in bodies:
		if body.name != "Sun":
			print(f"{body.name:<8} | Pos (x, y): {body.px/au:>6.2f} {body.py/au:>6.2f} | Vel (m/s): {body.vx:>10.3f} {body.vy:>10.3f}") # Formatting of the information
	print() # Add a break between each week

def loop(bodies, earth): # For celestial bodies and the earth years counter
	timestep = 3600 * 24 * 7 # Set the timestep to amount of seconds in a week
	step = 1
	earth_years = -1

	final_data = [] # Create an empty list that stores the formatted information
	for step in range(0, max_step + 1): # Iterate from step 0 to the maximum step
		update_info(step, bodies) # Print information about celestial body in current step

		# Earth years counter
		if 0.98 <= earth.px / au <= 1.00 and -0.05 <= earth.py / au <= 0.05:
			earth_years += 1
			turtle.clear()
			turtle.penup()
			turtle.goto(-450, 350)
			turtle.pendown()
			turtle.color("white")
			turtle.hideturtle()
			turtle.write(f"Earth Years: {earth_years}", font=("Calibri", 20, "normal"))

		force = {} # Creates a dictionary for total gravitational forces acting on each celestial body
		for body in bodies:
			total_fx = total_fy = 0.0
			for other in bodies: # Calculate the gravitational attraction between the current celestial body and all other bodies, using the "attraction" method
				if body is other: # Don't calculate the body's attraction to itself
					continue
				fx, fy = body.attraction(other)
				total_fx += fx
				total_fy += fy

			force[body] = (total_fx, total_fy) # Record the total force exerted in the dictionary

		# Update velocities based upon the force
		for body in bodies:
			fx, fy = force[body]
			body.vx += fx / body.mass * timestep # Update the x-axis velocity of the body
			body.vy += fy / body.mass * timestep # Update the y-axis velocity of the body

			if body.name != "Sun": # Update only the positions of planets
				body.px += body.vx * timestep
				body.py += body.vy * timestep
				body.goto(body.px * scale, body.py * scale) # Move the celestial body to the new position

		# Format the data in the text file
		for body in bodies:
			text_values = f"Week: {step:3}  {body.name:4}   Position ={body.px/au:6.2f} {body.py/au:6.2f}  Velocity ={body.vx:10.2f} {body.vy:10.2f}"
			final_data.append(text_values) # Goes through the data and put's it in order, then appends to list created earlier

		file.write(str(final_data) + "\n") # Convert the final_data list into a string and write to the text file
		final_data = []	# Clears the list so the next data step can be appended

	file.close() # Close the text file and save changes
	graph(earth_years)

# !Define the conditions for the celestial bodies and the turtle screen
def main():
	window = turtle.Screen()
	window.bgcolor("black")

	sun = Body()
	sun.name = "Sun"
	sun.mass = 1.98892 * 10**30
	sun.shape("circle")
	sun.color("yellow")
	sun.resizemode("user")
	sun.shapesize(1)

	venus = Body()
	venus.name = "Venus"
	venus.mass = 4.8685 * 10**24
	venus.px = 0.723 * au
	venus.vy = 35.02 * 1000
	venus.shape("circle")
	venus.color("purple")
	venus.resizemode("user")
	venus.shapesize(0.35)

	earth = Body()
	earth.name = "Earth"
	earth.mass = 5.9742 * 10**24
	earth.px = 1 * au
	earth.vy = 29.783 * 1000
	earth.shape("circle")
	earth.color("blue")
	earth.resizemode("user")
	earth.shapesize(0.35)

	mars = Body()
	mars.name = "Mars"
	mars.mass = 6.39 * 10**23
	mars.px = 1.524 * au
	mars.vy = 24.1 * 1000
	mars.shape("circle")
	mars.color("red")
	mars.resizemode("user")
	mars.shapesize(0.25)

	jupiter = Body()
	jupiter.name = "Jupiter"
	jupiter.mass = 1.898 * 10**27
	jupiter.px = 5.203 * au
	jupiter.vy = 13.06 * 1000
	jupiter.shape("circle")
	jupiter.color("green")
	jupiter.resizemode("user")
	jupiter.shapesize(0.50)

	for body in [sun, venus, earth, mars, jupiter]:
		body.penup() # Removes the lines from the sun
		body.goto(body.px * scale, body.py * scale) # Sets the starting x and y-axis position of each celestial body
		body.pendown() # Enables the orbital trails of each planet

	loop([sun, venus, earth, mars, jupiter], earth)
turtle.title("Orbits of Venus, Earth, Mars and Jupiter around the Sun")

# !Creates and saves graph
def graph(earth_years):
	sim_data = open("Projects/Simulation/planetaryOrbits.txt", "r")
	plt.xlabel("AU")
	plt.ylabel("AU")
	plt.title("Orbits of Venus, Earth, Mars and Jupiter around the Sun")
	plt.axis([-6, 6, -6, 6])
	plt.grid()

	celestial_coordinates = [] # Create a list to store the coordinates of celestial bodies

	for z in sim_data:
		i = z.split() # Put's data from each row into separate columns
		xs = float(i[5])
		ys = float(i[6])
		xv = float(i[16])
		yv = float(i[17])
		xe = float(i[27])
		ye = float(i[28])
		xm = float(i[38])
		ym = float(i[39])
		xj = float(i[49])
		yj = float(i[50])
		total = [xs, ys, xv, yv, xe, ye, xm, ym, xj, yj] # Create a list that contains the x and y coordinates of the celestial bodies at each simulation step
		celestial_coordinates.append(total) # Append the total list to the celestial_coordinates list

	celestial_coordinates = list(zip(*celestial_coordinates)) # Transpose the list, grouping the x and y coordinates together

	# Plot the orbits of the celestial bodies using the x and y values
	plt.plot(celestial_coordinates[0], celestial_coordinates[1], color = "yellow", marker = "o", label = "Sun")
	plt.plot(celestial_coordinates[2], celestial_coordinates[3], color = "purple", label = "Venus")
	plt.plot(celestial_coordinates[4], celestial_coordinates[5], color = "blue", label = "Earth")
	plt.plot(celestial_coordinates[6], celestial_coordinates[7], color = "red", label = "Mars")
	plt.plot(celestial_coordinates[8], celestial_coordinates[9], color = "green", label = "Jupiter")
	plt.legend(loc="upper right", fontsize=10)

	try:
		# Show the AU values for each planet (only in the saved file)
		planet_au = {
			"Venus": max(celestial_coordinates[2]),
			"Earth": max(celestial_coordinates[4]),
			"Mars": max(celestial_coordinates[6]),
			"Jupiter": max(celestial_coordinates[8])
		}
		for planet, max_planet_au in planet_au.items():
			planet_color = {"Venus": "purple", "Earth": "blue", "Mars": "red", "Jupiter": "green"}
			if planet == "Venus":
				plt.text(-0.68, +1.8, f"{max_planet_au:.2f} AU", fontsize=10, color=planet_color[planet], bbox=dict(facecolor="white", edgecolor="none"))
			elif planet == "Earth":
				plt.text(+1.69, -0.15, f"{max_planet_au:.2f} AU", fontsize=10, color=planet_color[planet], bbox=dict(facecolor="white", edgecolor="none"))
			elif planet == "Mars":
				plt.text(-2.65, -1.6, f"{max_planet_au:.2f} AU", fontsize=10, color=planet_color[planet], bbox=dict(facecolor="white", edgecolor="none"))
			elif planet == "Jupiter":
				plt.text(-3.6, +3.1, f"{max_planet_au:.2f} AU", fontsize=10, color=planet_color[planet])
		# Show the total Earth years (only in the saved file)
		earth_position = celestial_coordinates[4], celestial_coordinates[5] # Create a tuple with Earth's x and y coordinates
		earth_orbit_completion = math.atan2(earth_position[1][-1], earth_position[0][-1]) / (2 * math.pi)
		# Explanation of the line above:
		# Calculate the angle in radians between the positive x-axis and the tuple that contains the last x and y coordinates of Earth ([-1] is the last element in the list)
		# Then divide the result by 2 * pi to convert the angle into a percentage of completion of one full orbit around the Sun
		plt.text(-2.35, -3.21, f"Total Earth Years: {earth_years + 1 + earth_orbit_completion:.2f}", fontsize=12, color="black", bbox=dict(facecolor="white", edgecolor="none"))
		plt.savefig("Projects/Simulation/planetaryOrbits.png")
	except Exception as e:
		print(f"Error saving the file: {e}")
	try:
		plt.show()
	except Exception as e:
		print(f"Error showing the graph: {e}")

	# try:
	# 	if save_as_file:
	# 		plt.savefig("Projects/Simulation/planetaryOrbits.png")
	# except Exception as e:
	# 	print(f"Error saving the file: {e}")
	# try:
	# 	plt.show()
	# except Exception as e:
	# 	print(f"Error showing the graph: {e}")

if __name__ == "__main__":
	main()