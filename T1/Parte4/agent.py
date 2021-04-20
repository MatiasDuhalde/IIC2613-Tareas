import sys
import os
import queue

class Agent:
    def __init__(self, env):
        self.env = env
        self.x = env.init_x      # no es el tamaño de la grilla, es la posición del agente
        self.y = env.init_y
        self.visited = set()     # celdas ya visitadas
        self.visited.add((self.x, self.y))
        self.frontier = set()    # al profesor le fue util mantener esta variable
        for n in env.neighbors(self.x, self.y):
            self.frontier.add(n)
        self.path = []           # self.path es el camino que estamos siguiendo
                                 # no es necesario que uses este atributo, pero al
                                 # profe le fue útil



    # get_action(self, perceptions) supone que perceptions es una lista de
    # strings [s1,...,sn] donde si es sense_breeze(x,y) o sense_stench(x,y) para algúun x,y
    # debe retornar:
    #   - una tupla de la forma ('goto',x,y) para hacer que el agente se mueva a (x,y)
    #   - una tupla de la forma ('shoot',x,y) para hacer que el agente dispare a (x,y)
    #   - una tupla de la forma ('unsolvable') cuando el agente ha demostrado que el problema
    #     no tiene una solución segura
    def get_action(self, perceptions):
        def find_path(startx, starty, goalx, goaly, safe_area):
            # encuentra un camino entre (startx,starty) a (goalx,goaly)
            # pasando solo por celdas de safe_area

            if (startx, starty) == (goalx, goaly):
                return True, []
            closed = set()
            fr = queue.Queue()
            fr.put((startx, starty, []))
            while not fr.empty():
                (x, y, path) = fr.get()
                closed.add((x,y))
                for (nx, ny) in self.env.neighbors(x, y):
                    if (nx, ny) in closed:
                        continue
                    newpath = path + [(nx, ny)]
                    if (nx, ny) == (goalx, goaly):
                        return True, newpath
                    else:
                        if (nx, ny) in safe_area:
                            fr.put((nx, ny, newpath))
            return False, []


        def unsat_without(atom):
            # Consiedera completar e implementar este método
            # No es obligatorio que lo hagas, pero al profesor le fue útil.
            # Dado un cierto atom, arma un archivo extra.lp, el método retorna True
            # si y solo si el programa que resulta de considerar wumpus.lp y extra.lp
            # es tal que NO tiene modelos que no contienen a atom
            # i.e. todos los modelos contienen a atom

            def get_models(filename):  # extrae los modelos desde filename
                f = open(filename, 'r')
                lines = f.readlines()
                lines = [l.strip() for l in lines]
                if 'SATISFIABLE' in lines:
                    answers = []
                    i = 0
                    while True:
                        while i < len(lines) - 1 and lines[i].find('Answer:', 0) == -1:
                            i += 1
                        if i == len(lines) - 1:
                            return answers
                        i += 1
                        answers.append(lines[i].split(' '))
                    return answers
                elif 'UNSATISFIABLE' in lines:
                    return []
                print(filename, 'no es un output legal de clingo')
                return []

            # COMPLETAR - aquí se eliminaron 13 líneas de la solución (incluyendo comentarios)
            fextra = open('extra.lp', 'w')
            # Define extra and add cell range statement
            extra = f'cell(0..{self.env.size_x - 1},0..{self.env.size_x - 1}).\n'
            # Add visited cells (alive cells)
            for alive in self.env.get_visited():
                extra += f'alive({alive[0]},{alive[1]}).\n'
            # Add found perceptions (sense_stench and sense_breeze)
            for perception in perceptions:
                extra += f'{perception}.\n'
            # Add number of pits and wumpuses, if available
            num_pits = self.env.get_num_pits()
            num_wumpus = self.env.get_num_wumpus()
            if num_pits != None:
                extra += f'num_pits({num_pits}).\n'
            if num_wumpus != None:
                extra += f'num_wumpus({num_wumpus}).\n'
            # Add atom
            extra += f':- {atom}.\n'
            fextra.write(extra)
            fextra.close()
            os.system('clingo -n 0 wumpus.lp extra.lp > out.txt 2> /dev/null')
            # si usas Windows, la siguiente línea debiera funcionar
            # os.system('clingo -n 0 wumpus.lp extra.lp > out.txt 2> NUL')
            models = get_models('out.txt')
            return models == []

        # COMPLETAR - aquí se eliminaron 29 líneas de la solución (incluyendo comentarios)
        # Get target. Target is a cell in frontier that is 100% safe
        def unsat_without_frontier(predicate):
            for cell in self.frontier:
                atom = f'{predicate}({cell[0]},{cell[1]})'
                if unsat_without(atom):
                    return cell
            return tuple()


        # Get neighbors and update frontier. Only add to frontier if cell hasn't been visited.
        neighbors = self.env.neighbors(self.x, self.y)
        self.frontier.update(set(neighbors) - self.env.visited)
        target = unsat_without_frontier('safe')

        # If there's no target, we may need to shoot
        if not target:
            # TODO Define shoot condition here
            wumpus_target = unsat_without_frontier('wumpus')
            if wumpus_target:
                return ('shoot', wumpus_target[0], wumpus_target[1])
            # Else the model is unsolvable
            return 'unsolvable'

        # If target is a neighbor add to path, if not, backtrack (i.e. new target is last step)
        if not target in neighbors:
            found_path, path = find_path(self.x, self.y, target[0], target[1], self.env.visited)
            if not found_path:
                return 'unsolvable'
            target = path[0]

        # Change position to target and remove from frontier
        self.x = target[0]
        self.y = target[1]
        if (self.x, self.y) in self.frontier:
            self.frontier.remove((self.x, self.y))
        # Go to new position in environment
        return ('goto', self.x, self.y)
