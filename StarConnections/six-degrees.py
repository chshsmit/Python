import sys
import graph_toolz
import itertools

#
what_should_this_do = sys.argv[1]

if what_should_this_do not in ["path", "bfs", "justbuild"]:
    print("Your option is illegal. Please choose one of ")
    print(" [\"path\", \"bfs\", \"justbuild\"]")
else:
    f_input = open(sys.argv[2],'r', encoding="utf-8")
    thresh = int(sys.argv[3])

    all_cast = list()
    acted_in = dict()
    total = 0

    non_movies = ['Oscar\'s', 'Oscar', 'Hollywood', 'Sexiest', 'Awards', 'MTV',
                  'Movie Stars', 'Playboy', 'Blockbusters', 'Golden Globe',
                  'Saturday Night Live', 'Funny Females', 'Celebrity', 'SNL',
                  'Making', 'Shocking', 'Blockbuster', 'Concert','Gala',
                  'Red Carpet', 'Movies', '100', 'Donostia']

    to_check = ' '

    # This part over here builds the graph
    for line in f_input.readlines():
        total = total + 1
        tokens = line.split('#')
        person = tokens[0].strip()

        for i in range(1,len(tokens)):
            not_movie = False
            movie = tokens[i].strip()
            if len(movie) == 0:
                continue

            for word in non_movies:
                if movie.find(word) != -1:
                    not_movie = True
                    break
            if not_movie:
                continue

            all_cast.append((movie, person))

            if movie == to_check:
                print(person)

    f_input.close()
    print("Created raw all_cast for every movie")

    all_cast.sort(key = lambda tup: tup[0])
    print("Sorted all_cast")

    cast = list()
    network = graph_toolz.Graph()
    prev = ' '

    size = 0

    for i in range(0, len(all_cast)):
        movie = (all_cast[i])[0]
        person = (all_cast[i])[1]
        if movie == prev and i != len(all_cast)-1:
            cast.append(person)
            size = size+1
            continue

        elif movie == prev and i==len(all_cast)-1:
            cast.append(person)
            size = size+1

        if size < thresh:
            for actor in cast:
                if actor not in acted_in:
                    acted_in[actor] = set([prev])
                else:
                    acted_in[actor].add(prev)
            for (person1, person2) in itertools.combinations(cast,2):
                network.addEdge(person1, person2)

        prev = movie
        cast = [person]
        size = 1

        if movie == to_check:
            print(person)
            print(cast)

    print(network.size()[0],"nodes. ",network.size()[1],"edges.")

    if what_should_this_do == "path":
        this_file = open("path.txt", "w")
        while True:
            src = input("Enter source actor (or q to quit): ")
            if src == 'q':
                this_file.close()
                break
            if src not in network.vertices:
                print("Not in network")
                continue

            dest = input("Enter destination actor: ")
            if dest not in network.vertices:
                print("Not in network")
                continue

            this_file.write('------------------------------------\n')
            this_file.write(src + "--->" + dest + "\n")
            this_file.write('------------------------------------\n')

            links = network.path(src, dest)
            
            if len(links) == 0:
                this_file.write("Path not found")
                print("Path not found")
                continue
            for i in range(0, len(links)-1):
                this_file.write(links[i]+ ' -- '+ links[i+1] + "\n")
                print(links[i]+ ' -- '+ links[i+1] + "\n")                
                movie_str = ''
                for movie in acted_in[links[i]].intersection(acted_in[links[i+1]]):
                    movie_str = movie_str + ' ' + movie + ';'
                this_file.write(movie_str + "\n")
                print(movie_str + "\n")                
                
    elif what_should_this_do == "bfs":
        while True:
            src = input("Enter source actor (or q to quit): ")
            if src == 'q':
                break
            if src not in network.vertices:
                print("Not in network")
                continue

            degrees = network.levels(src)

            print(degrees)
