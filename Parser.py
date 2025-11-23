from Coordinates import Coordinates


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def read_tsp_file(file):
        result = []
        start_reading = False

        with open(file, "r") as f:
            for line in f:
                line = line.strip()

                if line == "NODE_COORD_SECTION":
                    start_reading = True
                    continue

                if not start_reading:
                    continue

                if line == "EOF":
                    break


                parts = line.split()
                if len(parts) < 3:
                    continue

                node_index = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])

                coord = Coordinates(node_index, x, y)
                result.append(coord)

        return result
