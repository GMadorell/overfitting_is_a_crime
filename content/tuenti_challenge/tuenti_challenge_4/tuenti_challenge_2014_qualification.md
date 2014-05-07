Title: Tuenti Challenge 4 - Qualification Round
Date: 2014-05-07
Category: Programming
Tags: python, tuenti-challenge, programming, puzzles
Slug: tuenti-challenge-4-qualification
Author: Gerard Madorell
Summary: Explanation of how I solved some of the Tuenti Challenge 4 Qualification Round challenges, using Python.


After recently having tryed out the qualification round for the google code jam, I saw that tuenti was doing an identical contest. Needless to say, I immediately decided to jump in.

Tuenti challenge is a competition in which programmers try to solve hard problems with a time limit. It consists of a set of rounds, between which you advance if you're faster and better than your oponents.

The sad part is that I did only have time for thinking about 10 of the total 20 exercises, and I managed to solve 8 of those.

As always, you can find the source code for all the exercises explained below hosted at github: https://github.com/Skabed/programming-challenges/tree/master/tuenti/tuenti_challenge_4/qualification.

Let's see what type of problems we're facing.

# 1.- Anonymous Poll #
This problem is obviously a warmup to make sure everyone understands how to work with this kind of problems.

We're faced with a poll, apparantly anonymous. But, is it really that random? We are going to write a program to try and guess which person answered a poll, taking advantage that we have some data about the students.

We're given a csv file with the following info about the students:

* Name 
* Gender
* Age
* Education
* Academic Year

Then, our input is of the form: 

    Gender,Age,Education,AcademicYear

And we just need to say which students may have answered that particular poll.

I solved this problem simply by creating a sqlite database and then doing a simple query per input line.

The only problem I really had was that I didn't read a tiny detail - the answer should be lexicographically sorted :S.

    #!python
    def solve_instance(self, instance):
        cursor = self.__connection.cursor()

        cursor.execute(
            """
                SELECT student_name
                FROM STUDENTS
                WHERE gender = ? AND age = ? AND education = ? AND academic_year = ?
            """, (instance.gender, int(instance.age), instance.studies, int(instance.academic_year))
        )

        names = cursor.fetchall()

        if len(names) > 0:
            return ",".join(sorted(map(lambda item: str(item[0]), names)))
        else:
            return "NONE"


# 2.- F1 Racing Team #
Time for building some tracks!

This exercise was a lot harder than the previous one, and it might very well be the first time I've solved an exercise of this kind.

In this challenge we're given a track in plain text format and our job is to provide a valid 2D circuit for it.

We have 4 characters:

* *#* for indicating the start of the track.
* *-* for the straight lines.
* */* for changing directions to the right.
* *\\* for changing directions to the left.

Also, a requirement is that the start of the track should be on a horizontal straight. The track can't cross itself and it will be a fully connected path.

Example input:

    ------\-/-/-\-----#-------\--/----------------\--\----\---/---

Example output:

    /---------\
    |         |
    |       /-/
    |       |
    \----\  \-----#-------\
         |                |
         |                |
         \----------------/

Quite sincerely, I didn't quite know how to solve it in a "mathematical" way, so my strategy revolved around creating a list (as if it was a 2D map) and then iterating over the input string.

At the beggining I did it with python lists, but that solution didn't scale at all, so at the end I used a numpy array, which is must faster.

A fun fact about this exercise is that I actually managed to crash Ubuntu running out of memory when trying huge inputs.


    #!python
    def solve_instance(self, instance, matrix_size=1000):
        road = instance.road

        race = np.zeros((matrix_size, matrix_size), dtype=np.int8)

        x = (len(race) // 2) - 1
        y = len(race) // 2
        direction = RIGHT

        # Place 
        road = self.unify_road(road)
        for character in road:
            # Move along the direction.
            x, y = self.update_coordinates(direction, x, y)
            # Insert the character of the road as a number.
            race[len(race) - y][x] = self.format_character(character, direction)

            if character in CORNERS:
                direction = self.update_direction(character, direction)

        # Remove all rows and columns that are full of zeros.
        race = self.trim_race(race)

        return self.format_race(race)

# 3.- Gambler's Cup #
In this exercise we have to find which algorithm the man behind a door uses in order to provide clues to win a lottery. The algorithm has two numbers as input and outputs a float rounded up to two decimals. There is a nice web application we can use to query numbers in order to get results. For example, this are some of the numbers I tested:

* x = 0, y = 0 -> output = 0
* x = 1, y = 0 -> output = 1
* x = 0, y = 1 -> output = 1
* x = 1, y = 1 -> output = 1.41
* x = 2, y = 2 -> output = 2.83
* x = 4, y = 4 -> output = 5.66

I was already thinking about using a regression machine learning algorithm when the solution struck me. You only have to use the euclidean distance between (0, 0) and (x, y)!

So, yeah, I think it's the first time I have ever solved a challenge with a single line of code.

    #!python
    def solve_instance(self, instance):
        return math.sqrt(instance.x * instance.x + instance.y * instance.y)


# 4.- Shape Shifters #
Welcome to the future. Humans have evolved and have mastered the art of changing their DNA, this process allowing them to change their appearance. Shifting from one form to another requires many small incremental DNA mutations (changing one nucleotide at a time).

Our job here is, given some source state, a finishing state and a list of possible intermediate states, to output the shortest path possible between the start and the end states. Only one nucleotide can change at a time.

Example input:  
The first line is the starting state, the second line corresponds to the ending state and the rest of lines are the intermediate states.
    
    AGC
    CAA
    AGC
    TTT
    CGC
    CGA
    CAA
    TGT

Example output:

    AGC->CGC->CGA->CAA

The key in this challenge was to identify it as finding the shortest path in a graph. Once I realised that, I solved it using the highly optimized NetworkX graphs.

To form the graph, I used every single state as a node. I then used Levenshtein edit distance and added an edge between the nodes that were one unit distant, exploiting the fact that only one nucleotide can change between states.

    #!python
    def solve_instance(self, instance):
        self.graph = nx.Graph()

        self.add_nodes_to_graph(instance)
        self.add_edges_to_graph(instance)

        path = shortest_path(self.graph, instance.start, instance.end)
        return "->".join(path)

    def add_nodes_to_graph(self, instance):
        all_nodes = [instance.start] + [instance.end] + instance.intermediate
        for node in all_nodes:
            self.graph.add_node(node)

    def add_edges_to_graph(self, instance):
        all_nodes = [instance.start] + [instance.end] + instance.intermediate
        for i in range(len(all_nodes)):
            for j in range(len(all_nodes)):
                if i != j and editdistance.eval(all_nodes[i], all_nodes[j]) == 1:
                    self.graph.add_edge(all_nodes[i], all_nodes[j])


# 5.- Tribblemaker #
In this exercise, we're given a 8x8 configuration of cells. We need to apply the game of life mechanics to them. Here's a pretty nifty explanation of it: http://www.math.cornell.edu/~lipa/mec/lesson6.html

Basically, we need to run a pattern that is guaranteed to repeat itself within 100 iterations. We need to output which generation repeats and the interval within repetitions. We also need to ignore the edges, the grid does not wrap around.

Example input:  
"X" are alive cells whereas "-"" are dead cells.

    X------X
    --------
    ---X----
    ---X----
    ---X----
    --------
    --------
    X------X

Output: 1 2  
That means that the generation 1 (we start at the 0 generation) repeats itself every two generations.

Solution:  
I solved this challenge by iterating over the 100 possible generations, searching at each step whether there was one in history which was exactly the same.

In order to find the next generation, I applied a neat computer vision trick: convolutions. They basically apply the given matrix of weights (kernel) and they sum the result of applying the kernel to each pixel. I'm sure it's not the most optimal way to do it, but I'm pretty sure it's one of the fastest to implement :). More info here: http://en.wikipedia.org/wiki/Kernel_(image_processing)#Convolution

    #!python
    def solve_instance(self, instance):
        self.conv_kernel = np.array([[1, 1, 1],
                                     [1, 10, 1],
                                     [1, 1, 1]])

        rows = instance.rows

        grid = self.initialize_grid(rows)

        loop_start, interval = self.find_game_of_life_repetitions(grid)

        return "{0} {1}".format(loop_start, interval)

    def initialize_grid(self, rows):
        grid = np.zeros((8, 8), dtype=np.int8)

        for i in range(len(rows)):
            for j in range(len(rows)):
                if rows[i][j].lower() == "x":
                    grid[i][j] = ALIVE

        return grid

    def find_game_of_life_repetitions(self, grid):
        """ Return: (generation at which the repetition start,
                     interval (in generations) between repetitions). """
        history = [grid]
        for generation in range(1, 102):
            grid = self.next_generation(grid)

            for old_generation, old_grid in enumerate(history):
                if np.array_equal(grid, old_grid):
                    return old_generation, generation - old_generation

            history.append(grid)
        else:
            raise Exception("Examples are guaranteed to repeat after 100 generations")

    def next_generation(self, grid):
        convolution = scipy.ndimage.filters.convolve(grid,
                                                     self.conv_kernel,
                                                     mode="constant")  # Change to wrap for real GoL.

        boolean = (convolution == 3) | (convolution == 12) | (convolution == 13)
        return np.int8(boolean)

# 6.- Man in the middle #
I skipped this exercise.  
Basically, they gave us two files written in javascript - client & server. We had a man in the middle service and we needed to decrypt the messages that they were sending each other.

So, as my cryptographic skills aren't that good and there isn't any really similar API between node crypto and python crypto, this exercise proved too hard for my knowledge.


# 7.- Yes we scan #
We're given a call log where each line is of the form:

    id1 id2

Each id identifies a spy. Our job is: given two ids, find at which call they're related. We consider that two spies are related if there's a connection between them. For example, if spy 1 knows spy 2, and spy 2 knows spy 3, then spy 1 is related to 3 via 2.

We need to tell at which call record the relation is evidenced, as well.

I modeled this problem as a graph problem: nodes are the spy ids and edges the relationship created when they call each other. After that, I fetch the shorter simple paths between our input ids and return the one that is related sooner (meaning a smaller call id).

One problem I faced is that it's impossible to get all the simple paths between our objective nodes, as the call log has 10^6 lines, so I cut it off at a maximum path length of 25.


    #!python
    def solve_instance(self, instance):
        self.graph = networkx.Graph()

        with open("phone_call.log", "r") as log:
            for i, line in enumerate(log):
                id1, id2 = map(lambda string: int(string), line.strip().split())
                if not self.graph.has_node(id1):
                    self.graph.add_node(id1)
                if not self.graph.has_node(id2):
                    self.graph.add_node(id2)
                if not self.graph.has_edge(id1, id2):
                    self.graph.add_edge(id1, id2, call_id=i)

        id1, id2 = instance.id_start, instance.id_end

        if not has_path(self.log_graph, id1, id2):
            return "Not connected"

        cutoff = 25
        path = min(networkx.all_simple_paths(self.log_graph, id1, id2, cutoff=cutoff), 
                   key=lambda p: self.find_max_id(p))

        call_id = self.find_max_id(path)

        return "Connected at {0}".format(call_id)

    def find_max_id(self, path):
        latest_call = max(pairwise(path), key=lambda pair: self.log_graph[pair[0]][pair[1]]["call_id"])
        return self.log_graph[latest_call[0]][latest_call[1]]["call_id"]


# 8.- Tuenti restructuration. #
In this exercise we're given a table distribution and an objective distribution, as 3x3 matrices. Our job is to count how many adjacent swaps we need to do in order to get to the end status.

Input:

    1, 2, 3
    4,  , 5
    6, 7, 8

    7, 6, 8
    5,  , 3
    1, 2, 4
(middle is empty, but can be used as well)

Output:

    12


This is very very similar to the 8 puzzle game, which is explained here: http://www.cs.princeton.edu/courses/archive/spr10/cos226/assignments/8puzzle.html

I used A* with a very strange heuristic. I tryed really hard to come up with a good heuristic, but I failed so I used a standard euclidean distance, which solved the test correctly after dividing it by 1.4 so it's acceptable. This felt like a huge hack, to be honest, but I already spent way too much time on this exercise and I was already about to skip it as well.

    #!python
    def solve_instance(self, instance, instance_id):
        initial = instance.initial_table
        objective = instance.objective

        translator = self.get_translator(initial)
        initial = self.to_array(initial, translator)
        try:
            objective = self.to_array(objective, translator)
        except KeyError:
            return -1

        hard_heuristic_sol = \
            self.solve_heuristic(initial, objective, lambda actual, target: euclidean(actual, target) / 1.4)
        return "{0}".format(hard_heuristic_sol)

    def solve_heuristic(self, initial, objective, heuristic):
        initial_state = State(initial, 0, None, heuristic)

        q = StatePriorityQueue(objective)
        q.add_state(initial_state)

        while True:
            state = q.consume()
            if state.is_final(objective):
                break

            for new_state in state.expand():
                q.add_state(new_state)

        return state.n_moves_made

    class State(object):
        def __init__(self, position=None, n_moves_made=None, previous_state=None, heuristic=None):
            self.position = position
            self.n_moves_made = n_moves_made
            self.previous_state = previous_state
            self.h = heuristic

        def calculate_heuristic(self, target):
            return self.h(self.position, target) + self.n_moves_made

        def is_final(self, target):
            return manhattan_2d(self.position, target) == 0

        def expand(self):
            """ Returns the new states we can reach from this state. """
            states = []
            # Top left corner.
            states.append(self.create_modification((0, 0), (0, 1)))
            states.append(self.create_modification((0, 0), (1, 0)))

            # Top right corner.
            states.append(self.create_modification((0, 2), (0, 1)))
            states.append(self.create_modification((0, 2), (1, 2)))

            # Bot left corner.
            states.append(self.create_modification((2, 0), (2, 1)))
            states.append(self.create_modification((2, 0), (1, 0)))

            # Bot right corner.
            states.append(self.create_modification((2, 2), (2, 1)))
            states.append(self.create_modification((2, 2), (1, 2)))

            # Middle cells - clockwise starting from north.
            states.append(self.create_modification((0, 1), (1, 1)))
            states.append(self.create_modification((1, 2), (1, 1)))
            states.append(self.create_modification((2, 1), (1, 1)))
            states.append(self.create_modification((1, 0), (1, 1)))

            return states

        def create_modification(self, from_coords, to_coords):
            new_pos = self.position.copy()
            x1, y1 = from_coords
            x2, y2 = to_coords
            new_pos[x1, y1], new_pos[x2, y2] = new_pos[x2, y2], new_pos[x1, y1]

            return State(new_pos, self.n_moves_made + 1, self, self.h)



# 9.- Bendito Chaos
A huge party is being organized in AwesomeVille. Everyone wants to come, even people from other cities. That means that there's going to be a major traffic jam, so we need to calculate how many people can come from each city and then calculate the food and beverages.

Two types of roads exist: normal and rist ones. Depending on the area, the max speed of each road varies. Each road may have one or two lanes, but they're all unidirectional.

We have a map of the raods connecting each city with AwesomeVille. Everyone wants to get there really fast, but they won't break the law.

All the roads are always (even at the start) 100% full. Size of each car is 4m and there is a space of 1m between cars (meaning that a car enters the road and leaves it each 5m).

We need to calculate the amount of people that can come in 1h.

Example input:  
We have:

* Amount of cities.
* Name of each city.
* Speed of s roads, speed of d roads.
* Amount intersections, amount roads.
* For each intersection: from, to, lane_type, amount_lanes.  

.

    1
    BoringVille
    80 60
    2 5
    BoringVille 0 normal 1
    BoringVille 1 normal 2
    0 1 dirt 2
    0 AwesomeVille dirt 1
    1 AwesomeVille normal 1

Example output:
    
    BoringVille 28000

Solution:  
The key here is to see that this is really a graph problem, in which the intersections and the cities are the nodes and the roads the edges. More concretely, we have to find the maximum flow between the two cities. The flow, in this particular problem corresponds to the road speed times the amount of lanes the road has.

There's a good algorithm for solving the maximum flow problem: Ford & Fulkerson. We have to restrict the flow, though, to those nodes that are connected directly to AwesomeVille.

    def solve_instance(self, instance):
        graph = self.construct_graph(instance)

        flow = nx.ford_fulkerson_flow(graph, instance.city_name, FINAL)

        max_speed_kmh = 0
        for node, flow_dict in flow.items():
            if FINAL in flow_dict:
                max_speed_kmh += flow_dict[FINAL]

        seconds_in_a_hour = 3600
        meters_per_car = 5

        max_speed_ms = max_speed_kmh * (1000/1) * (1/seconds_in_a_hour)
        cars_per_second = max_speed_ms * (1/meters_per_car)
        cars_per_hour = cars_per_second * seconds_in_a_hour

        return "{0} {1:.0f}".format(instance.city_name, cars_per_hour)

    def construct_graph(self, instance):
        g = nx.DiGraph()
        speed = instance.get_speed_map()
        for road in instance.roads:
            g.add_nodes_from([road.from_, road.to])
            g.add_edge(road.from_, road.to, road_type=road.road_type, lanes=road.lanes_n,
                       capacity=int(speed[road.road_type] * road.lanes_n))
        return g


# 10.- Random Password #
Okay, this problem is really strange. All the information we have is (literally):

> It seems to be a random password... how could it be?

> Get the key for your input. Start at: http://random.contest.tuenti.net/?input=INPUT

That's it :S.

Well, what do we know from here? We can make requests to a website and it will hopefully return something once we give it the correct input.  
Information given suggests using brute force (*random password*), but I'm pretty sure that's not the case.

I spent way too much time trying to solve this problem, but I had to skip it at the end, and I didn't have time for solving any more problems.









