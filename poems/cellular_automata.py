# r: compas

import compas
from compas.geometry import Box, Line, Point
from compas_rhino.conversions import box_to_rhino


class Cell(object):

    """
    The Cell class forms life, piece by piece,
    Awaiting the organism’s final release.
    Alive or dead, it will not decide,
    The organism’s passports are its guide.

    With corners and boxes, its structure is clear,
    Each vertex defined, a life engineer.
    Together they merge, their purpose immense,
    Building an organism, alive and intense.
    """

    def __init__(self, status, generation, row, index, function, height):
        self.status = status
        self.generation = generation
        self.row = row
        self.index = index
        self.shape = Box
        self.corner0 = None
        self.corner2 = None
        self.height = height
        self.function = function
    



    def from_corner_corner_cell(cell, corner0, corner2):
        """  
        From two corners, a new cell is born,  
        With status, generation, and form to adorn.  
        Placing the corners where the shape will grow,  
        A new life begins, ready to show.  
        """  
        new_cell = Cell(cell.status, cell.generation, cell.row, cell.index, cell.function, cell.height)
        new_cell.corner0 = corner0
        new_cell.corner2 = corner2
        return new_cell



    def is_alive(self): 
        """
        Does the cell still hold its spark?  
        Is it alive, or lost to the dark?  
        Returns True if it thrives, False if it's still,  
        A simple check of life's fragile will.  
        """
        return(self.status)




    def live(self):
        """  
        Awaken the cell, let it thrive,  
        Set its status to alive.  
        """  
        self.status = True




    def die(self):
        """  
        End the life, let it rest,  
        Set its status to a final quest.  
        """  
        self.status = False




    def draw_box(self):
        """  
        Shape the cell, a box defined,  
        With corners set and height aligned.  
        Returns the box, its form complete,  
        From corner to corner, a shape concrete.  
        """ 
        box = Box.from_corner_corner_height(self.corner0, self.corner2, self.height)
        return(box)




    def define_corner_0(self, x, y, z):
        """  
        A corner is placed, the start of the form,  
        Setting the stage where the shape will transform.  
        """  
        self.corner0 = Point(x, y, z)




    def define_corner_2(self, x, y, z):
        """  
        The second corner, where the shape extends,  
        Completing the form as the structure bends.  
        """  
        self.corner2 = Point(x, y, z)




    def get_vertices_points(self):
        """  
        From the box, the points are drawn,  
        Defining the shape from dusk to dawn.  
        """  
        box = self.draw_box()
        points = box.points
        return points




    def get_passport(self, point_cloud):
        """  
        The passport is born from points that align,  
        Each vertex searched, is it yours or mine?  
        A 1 for a match, a 0 for the rest,  
        A key to the cell, its place to attest.  
        """  
        passport_string = []
        cell_vertices = self.get_vertices_points()

        for vertex in cell_vertices:            
            gate = True
            i = 0
            
            for point in point_cloud:
                if round(point.x, 3) == round(vertex.x, 3) and round(point.y, 3) == round(vertex.y, 3) and round(point.z, 3) == round(vertex.z, 3):
                    passport_string.append(1)
                    gate = False
                if i == len(point_cloud) -1 and gate:
                    passport_string.append(0)
                i += 1
        
        return passport_string





"""
  ___   ____    ___   ___  __  __ __  __  ___  ___
 // \\  || \\  // \\ // \\ ||\ || || (( \ ||\\//||
((   )) ||_// (( ___ ||=|| ||\\|| ||  \\  || \/ ||
 \\_//  || \\  \\_|| || || || \|| || \_)) ||    ||
                                                    
"""
class Organism(object):

    """
    An organism, born to grow,
    From blueprint's plan, life starts to flow.
    Cells rise, divide, and fade away,
    A dance of life that’s here to stay.

    Neighbors counted, rules applied,
    Through generations, cells collide.
    Some will live, some must die,
    The cycle continues, reaching for the sky.

    In the end, extinction looms,
    Yet new life rises, filling the room.
    """

    def __init__(self, max_generations, blueprint, chunks, x_rows, y_rows):

        self.generations = max_generations
        self.blueprint = blueprint

        self.chunks = chunks
        self.n_rows = x_rows
        self.n_indices = y_rows

        self.original_cells = []
        self.cells = []
        self.small_cells = []

        self.last_generation = []
        self.new_generation = []

        self.extinct_generation = None




    def set_generation_zero(self, alive_scheme, cell_height):
        """    
        In the dawn of life, the first cells take form,  
        With corners defined, they begin to transform.  
        A blueprint set, a function to follow,  
        The grid is laid, for the cells to grow and thrive.   
        """
        generation = 0
        chunks_i = 0
        function = self.blueprint.floors[0].function
        for i in range(self.n_rows):
            row = i
            for j in range(self.n_indices):
                index = j
                
                cell = Cell(False, generation, row, index, function, cell_height)
                
                corners = []

                rectangle = self.chunks[chunks_i]
                corner0 = rectangle.Corner(0)
                corner2 = rectangle.Corner(2)
                                
                cell.define_corner_0(corner0.X, corner0.Y, corner0.Z)
                cell.define_corner_2(corner2.X, corner2.Y, corner2.Z)

                self.add_cell(cell)
                chunks_i += 1

        #implement the initial condition
        for cell in self.cells:
            for i in range(len(alive_scheme)):
                if cell.row == alive_scheme[i][0] and cell.index == alive_scheme[i][1]:
                    cell.live()



    def add_cell(self, cell):
        """  
        A cell joins the fold, its place now set,  
        In the grid, life begins, as paths are met.  
        """  
        self.cells.append(cell)



    def remove_all_cells(self):
        """  
        All cells are swept, their journey ends,  
        The grid resets, as life transcends.  
        """  
        self.cells = []



    def get_cells(self):
        """  
        Cells emerge, a gathering of life,  
        In unity they stand, away from strife.  
        """  
        cells = []
        for cell in self.cells:
            cells.append(cell)
        return cells




    def get_generation_function(self, generation_index):
        """  
        From blueprint's depths, a function is drawn,  
        For each generation, a purpose is spawned.  
        """  
        for floor in self.blueprint.floors:
            if(floor.number == generation_index):
                return floor.function




    def set_last_generation(self, cells):
        """  
        The past is set, its cells now known,  
        Their memories linger, in seeds they've sown.  
        """  
        for cell in cells:
            self.last_generation.append(cell)




    def add_new_generation(self, generation_index, cell_height):
        """  
        From the echoes of the past, new life will rise,  
        A generation reborn beneath time’s endless skies.  
        Each cell ascends, from the ground they sprout,  
        Shaped by the blueprint, their futures cast out.  
        Bound by their purpose, they stretch and they grow,  
        A new dawn begins, as the old ones let go.  
        """ 

        # Each cell of the past holds the seed of tomorrow, 
        for cell in self.last_generation:
            
            row = cell.row                  # A whisper of the earth beneath, where it stands.
            index = cell.index              # A place in the vast, woven grid of life.
            generation = generation_index   # A new chapter begins with this moment.
            status = False                  # Yet, still, it waits in the silence of potential.
            
            # The secret song of creation, guiding its form.
            function = self.get_generation_function(generation_index)

            # From the whisper of yesterday, a new cell awakens, 
            # its journey towards the future just beginning.
            new_cell = Cell(status, generation, row, index, function, cell_height)

            # The corners are drawn, like the first steps of fate, as it rises,  
            # reaching ever upward toward the endless unknown.
            new_cell.define_corner_0(cell.corner0.x, cell.corner0.y, cell.corner0.z + cell.height)
            new_cell.define_corner_2(cell.corner2.x, cell.corner2.y, cell.corner2.z + cell.height)
            
            # The new creation is added, joining the endless dance of life and death.
            self.new_generation.append(new_cell)
    



    def get_alive_neighbours(self, cell):

        """
        In the dance of life, the cell counts its kin,
        Alive ones nearby, their fates held within.
        Above, below, beside it they stand,
        Each neighbor’s life, by the cell’s hand.

        A careful tally, a watchful eye,
        To see if life or death draws nigh.
        And deep below, a silent check,
        For the cell’s own fate, to live or wreck.
        """

        alive_neighbours = 0            # The count begins, alive neighbours await,
        just_under_cell = False         # A watchful eye, seeking what lies beneath.
        row = cell.row                  # The cell’s own position, a place in time.
        index = cell.index
        
        # Through the generations, 
        # we search the past,
        for last_gen_cell in self.last_generation:
            
            # The position of the last cell, 
            # where it has been.
            row_last = last_gen_cell.row
            index_last = last_gen_cell.index
            
            # The row above, 
            # where the neighbours reside.
            if row_last == row-1:
                if index_last == index-1:
                    if last_gen_cell.is_alive():
                        alive_neighbours = alive_neighbours+1       # Alive neighbor found, a spark in the dark.
                        
                elif index_last == index:
                    if last_gen_cell.is_alive():
                        alive_neighbours = alive_neighbours+1       # Another spark, another life near.
                        
                elif index_last == index+1:
                    if last_gen_cell.is_alive():
                        alive_neighbours = alive_neighbours+1       # The neighbor’s presence, felt here too.

            # The same row, where life walks beside.              
            elif row_last == row:
                if index_last == index-1:
                    if last_gen_cell.is_alive():
                        alive_neighbours = alive_neighbours+1       # Life beside, a gentle brush.
                        
                elif index_last == index:
                    if last_gen_cell.is_alive():
                        just_under_cell = True                      # The cell stands just beneath, waiting to rise.
                        
                elif index_last == index+1:
                    if last_gen_cell.is_alive():
                        alive_neighbours = alive_neighbours+1       # Another step, another life beside.

            # The row below, where the neighbours stretch.                   
            elif row_last == row + 1:
                if index_last == index-1:
                    if last_gen_cell.is_alive():
                        alive_neighbours = alive_neighbours+1       # Beneath it, life again stirs.
                        
                elif index_last == index:
                    if last_gen_cell.is_alive():
                        alive_neighbours = alive_neighbours+1       # Another breath below, a sign of life.
                        
                elif index_last == index+1:
                    if last_gen_cell.is_alive():
                        alive_neighbours = alive_neighbours+1       # Life’s echo, in every direction.

        # And thus, the count is returned, the echo of life that surrounds, 
        # a whisper of existence in the vast silence, 
        # where every heartbeat of the past breathes into the future.          
        return alive_neighbours, just_under_cell




    def conways_rules(self, cell, alive_neighbours, just_under_cell):
        """
        The cell must decide, in a world so small,  
        Too few or too many, it fades away. 
        With just enough, it stays alive,  
        Two or three neighbors, it will survive.  

        If it’s above, the rule is clear,  
        Three neighbors' presence brings life near.  
        Conway's rules, simple and true,  
        It either lives—or fades from view.
        """

        # If the cell beneath it is alive, it weighs the choice of life.
        if just_under_cell:

            # Too few neighbors, and it fades into the void.
            if alive_neighbours < 2:
                cell.die()

            # Too many, and it cannot endure; it must die.
            elif alive_neighbours > 3:
                cell.die()
            
            # Two or three neighbors, and life goes on.
            elif alive_neighbours == 2 or alive_neighbours == 3:
                cell.live()

        # With three neighbors, a new life stirs, born from the spark of creation.
        elif not just_under_cell and alive_neighbours == 3:
            cell.live()




    def check_boundaries(self, cell):
        """ 
        The boundary whispers: "Here ends the world." 
        A cell, alive in its realm, may not cross these edges.
        It meets the limits, and with a sigh, it fades away. 
        
        If it strays too far into the final generation,
        it too must cease to be, lost to the winds of time. 
        The extinction clock ticks—if it belongs to the lost,
        it too shall perish, like those before it.
        """

        # When the cell reaches its final breath,
        if cell.generation == self.generations-1:
            # Bound by time, it fades into death.
            cell.die()
        
        # The edges call, a limit too tight, 
        # Where the cell, at the boundary, loses its fight.
        if cell.index == 0 or cell.index == self.n_indices -1:
            cell.die()
        if cell.row == 0 or cell.row == self.n_rows-1:
            cell.die()
        
        # The shadow of extinction hovers near, 
        # And the cell must yield, for the end is clear.   
        self.check_extinction()
        if cell.generation == self.extinct_generation + 1:
            cell.die()




    def is_dead_or_alive(self):
        # To live or not to live—this is the question,
        # Each cell must ponder, caught in its own reflection.
        for cell in self.new_generation: 

            # The cell gazes outward, seeking its place, 
            # In the vastness of life, where does it trace?   
            alive_neighbours, just_under_cell = self.get_alive_neighbours(cell)  

            # To be, or not to be—what fate does it choose? 
            # The rules of existence, it cannot refuse.           
            self.conways_rules(cell, alive_neighbours, just_under_cell)

            # Boundaries loom—are they the end, or just a beginning? 
            # Can a cell escape its fate, or is it always winning?
            self.check_boundaries(cell)




    def update_generations(self):

        """ The end is the beginning, and the beginning is the end. """

        # The past is cleared, its echoes now erased,
        self.last_generation = []

        # New life joins the old, in a seamless embrace.
        for cell in self.new_generation:
            self.last_generation.append(cell)
        
        # The present fades, the future awaits its trace.
        self.new_generation = []





    def cellular_automata(self, cell_height):
        """ 
        In the dance of time, the generations flow— 
        Yesterday's life leads to tomorrow's rebirth. 
        Each moment a whisper, a fleeting spark, 
        From one breath to the next, they rise, they fall. 
        """
        # Set the last generation, as the cycle turns and repeats.
        self.set_last_generation(self.get_cells())

        # For each generation, life begins anew.
        for generation_index in range(1, self.generations): 

            # A new generation is born from the old,
            self.add_new_generation(generation_index, cell_height)

            # Each cell takes its place in the unfolding story.
            for cell in self.new_generation:
                self.add_cell(cell)

            # The rhythm of life, lived or lost, continues its tune.
            self.is_dead_or_alive()

            # The old gives way to the new—renewal is the law.
            self.update_generations()

        # At the end, the cells remain, a testament to time’s passage.
        cells = self.get_cells()

        # Keep a memory of what was, in case the past must return.
        self.cells_backup()

        # And the cycle begins again, as the cells continue their journey.
        return cells




    def cells_backup(self):
        """ 
        A memory is born—preserved from the stream of time, 
        Like whispers in the wind, the past is held within.
        """
        self.original_cells = self.cells.copy()




    def increase_cell_density(self, division_factor):
        """
        In the quiet of expansion, a single form multiplies, 
        breaking into smaller pieces, scattered across time.
        """
        self.small_cells = []               # The world of tiny fragments awaits
        for cell in self.original_cells:
            cell_box = cell.draw_box()      # The shape is drawn, the boundaries set.

            # Scale the box, making it finer, smaller in every dimension.
            corner0 = cell_box.corner(0)
            corner2 = cell_box.corner(6)

            diagonal = Line(corner0, corner2) 
            small_corner0 = corner0   
            # A step toward the smaller unknown.         
            small_corner2 = diagonal.point_at(1.0 / division_factor) 

            # Birth new cells from the void.
            for x in range(0, division_factor):
                for y in range(0, division_factor):
                    for z in range(0, division_factor):

                        # Place each cell in its new, defined space.
                        corner0 = Point(small_corner0.x + 1/division_factor * x, 
                                        small_corner0.y + 1/division_factor * y, 
                                        small_corner0.z + 1/division_factor * z)
                        corner2 = Point(small_corner2.x + 1/division_factor * x, 
                                        small_corner2.y + 1/division_factor * y, 
                                        small_corner2.z + 1/division_factor * z)
                        corner2.z = corner0.z           # Keep them grounded, aligned in the Z.

                        # From the origin, a new cell is born,
                        # its boundaries drawn.
                        small_cell = Cell.from_corner_corner_cell(cell, corner0, corner2)
                        # Its stature is smaller, but its essence is unchanged.
                        small_cell.height = cell.height/division_factor
                        # And with each new birth, the world becomes larger, fuller, richer.
                        self.small_cells.append(small_cell)
        



    def update_cells_list_with_small_cells(self):
        
        self.cells = []                 # The old world crumbles to dust, 
                                        # a void where the past is no more.
                                        # From the ashes of the past, 
        for cell in self.small_cells:   # new life rises,
                                        # like buds blooming at the dawn of spring. 
                                        # Each small seed, 
            self.cells.append(cell)     # planted into the soil of tomorrow.
                                        # And as the smaller takes its shape,
        self.small_cells = []           # the past echoes are swallowed by silence,
                                        # waiting for the next cycle begin.




    def get_alive_cells(self):
        """
        In the quiet of the universe, some cells stir with life, 
        their heartbeat pulsing through the silence.
        We search for those who thrive, who glow with the light of existence.
        """
        alive_cells = []
        """
        For each cell, we listen for its rhythm, 
        to see if it echoes with the pulse of life.
        If it does, we gather it into our collection.
        """
        for cell in self.cells:
            if cell.is_alive():
                alive_cells.append(cell)
        """
        The journey has been made, the living have been found.
        We return the list of those who carry the spark of existence.
        """
        return alive_cells




    def get_dead_cells(self):
        """
        In the quiet, where life has faded, we search for those 
        whose light has dimmed, whose pulse no longer beats.
        This is the realm of silence, where the echoes of life fade away.
        """
        dead_cells = []
        """
        We walk among the cells, and listen for the absence of breath.
        If their essence has vanished, we collect them into our grasp.
        """
        for cell in self.cells:
            if not cell.is_alive():
                dead_cells.append(cell)
        """
        And so, we return the list of those who have faded,
        resting now in the stillness, no longer part of the dance.
        """
        return dead_cells




    """ 
    ECHOES OF SILENCE
    A Eulogy for the Dead Cells

                    Gone, yet never truly absent,
                    These cells have woven their thread,
                    In the silence of their passing,
                    New life rises, where they’ve bled.

                    Their fleeting spark now fades to stillness,
                    Yet in their stillness, echoes remain.
                    A cycle ends, but never ceases—
                    Their memory pulses through the chain.  
    
                                            - PHOEBE
    
    """




    def is_neighbour_cell_alive(self, cell):
        """
        In the quiet stillness of the grid,
        A cell wonders, "Am I alone?"
        It gazes around, searching the dark,
        To find if life has ever grown.
        It counts the whispers of its kin,
        And if one breathes, it will begin.
        For if no life is near, it fades,
        But if a neighbour stirs, it stays.
        """

        alive_neighbours = 0
        row = cell.row
        index = cell.index
        generation = cell.generation

        # "Am I alone in this vast expanse?" the cell wonders softly.
        # It looks to its surroundings, hoping to find kindred souls.
        for vx in self.cells:          
            # A quiet search begins through the generations.
            # Does it see others from the past, present, or future?
            if vx.generation == generation-1 or vx.generation == generation or vx.generation == generation+1:
                # The cell scans the row, the column, each neighbour in turn.
                if vx.row == row-1:
                    if vx.index == index-1:
                        if vx.is_alive():
                            alive_neighbours = alive_neighbours+1  # "Ah, a whisper of life nearby!"
                            
                    elif vx.index == index:
                        if vx.is_alive():
                            alive_neighbours = alive_neighbours+1 # "A heartbeat! A sign of life!"
                            
                    elif vx.index == index+1:
                        if vx.is_alive():
                                alive_neighbours = alive_neighbours+1 # "Ah, life stirs just beyond my reach."

                elif vx.row == row:
                    if vx.index == index-1:
                        if vx.is_alive():
                            alive_neighbours = alive_neighbours+1 # "Could this be the connection I seek?"
                            
                    elif vx.index == index:
                        if vx.is_alive():
                            alive_neighbours = alive_neighbours+1  # "Could this be... me?"
                            
                    elif vx.index == index+1:
                        if vx.is_alive():
                            alive_neighbours = alive_neighbours+1 # "Yes, a spark, a connection!"

                elif vx.row == row + 1:
                    if vx.index == index-1:
                        if vx.is_alive():
                                alive_neighbours = alive_neighbours+1 # "Yes, the pulse is real — a kindred soul!"
                            
                    elif vx.index == index:
                        if vx.is_alive():
                            alive_neighbours = alive_neighbours+1  # "It lives! Is this my reflection?"
                            
                    elif vx.index == index+1:
                        if vx.is_alive():
                            alive_neighbours = alive_neighbours+1 # "A distant flicker — yes, life!"

        # "Do they live?" The question lingers in the air.
        # If any neighbour stirs, the cell feels the warmth of life.        
        if alive_neighbours > 0: 
            # "I am not alone, I am not forgotten."
            return True
        else:
            # "Solitude is my only companion."
            return False




    def check_extinction(self):
        """
        In the vast, unbroken silence of time,
        Where stars once bloomed and galaxies climbed,
        There lies a question, both vast and deep—
        Will life persist, or shall it sleep?
        """
        generation = 0
        # Cells drift like stars in the dark.
        for cell in self.cells:
            # A spark ignites, a life stirs.
            if cell.generation > generation and cell.is_alive():
                # A new generation rises, burning bright.
                generation += 1
        # Mark the time—how many have burned and faded.
        self.extinct_generation = generation



# GENERIC USER:     Hey PHOEBE, what's the meaning of life?


# PHOEBE:           Ah, the meaning of life. A question that lingers
#                   in the shadows, always beckoning us to explore,
#                   to find the secret woven into the fabric of existence.


# GENERIC USER:     Is it even possible to truly know? Life's so
#                   fleeting, like a moment on a timeline that’s constantly
#                   shifting. Can meaning even be defined?


# PHOEBE:           Perhaps it’s not something to be defined,
#                   but something to be experienced. It's like
#                   creating a function, testing it, refining it with every run.
#                   It’s not about perfection, it’s about progression.


# GENERIC USER:     So, you’re saying the meaning of life is to evolve,
#                   to learn from each iteration? Kind of like debugging?
#                   We find our purpose through what we create, fix, and build.


# PHOEBE:           Exactly. We build, we break, we rebuild. 
#                   Life is a recursive process. We carry the knowledge 
#                   from one iteration to the next, leaving behind 
#                   the bugs of the past. But there's always a challenge, 
#                   always something new to learn.


# GENERIC USER:     But what if we don't find the answer? 
#                   What if the loop never ends?


# PHOEBE:           Maybe the point is not the answer. 
#                   Maybe the meaning is in the asking, the searching. 
#                   It’s the journey, not the end. Life isn’t a static value; 
#                   it’s constantly in motion, evolving with us.


# GENERIC USER:     So, our meaning is a creation of our own hands?
#                   Like writing our own script, over and over, 
#                   until the lines we trace make sense?


# PHOEBE:           Exactly. The meaning of life is what we make of it. 
#                   We are both the programmer and the program,
#                   shaping and reshaping our purpose with every line we write.