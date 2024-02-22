import clusteringcopy as clu
import predicttestcopy as pt

def main():
    clu.trainIt()

    design_problems = [
        "Design a drawing editor. A design is composed of the graphics (lines, rectangles and roses), positioned at precise positions. Each graphic form must be modeled by a class that provides a method draw(): void. A rose is a complex graphic designed by a black-box class component. This component performs this drawing in memory, and provides access through a method getRose(): int that returns the address of the drawing. It is probable that the system evolves in order to draw circles",
        "Design a DVD market place work. The DVD marketplace provides DVD to its clients with three categories: children, normal and new. A DVD is new during some weeks, and after change category. The DVD price depends on the category. It is probable that the system evolves in order to take into account the horror category",
        "Many distinct and unrelated operations need to be performed on node objects in a heterogeneous aggregate structure. You want to avoid 'polluting00' the node classes with these operations. And, you do not want to have to query the type of each node and cast the pointer to the appropriate type before performing the desired operation"
    ]

    for problem in design_problems:
        print(pt.predictIt(problem))

if __name__ == "__main__":
    main()