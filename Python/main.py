import grid


def main():
    number_of_nodes = 49
    course_nodes = grid.Grid(number_of_nodes)
    course_nodes.search_perimeter()

    for i in range(number_of_nodes):
        print (course_nodes[i].node_number)

if __name__ == "__main__":
    main()