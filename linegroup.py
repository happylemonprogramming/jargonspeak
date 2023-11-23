def linegroup(output, buffer=5):
    words = output[0]
    x_coordinates = output[1]
    y_coordinates = output[2]

    # Combine words, x, and y coordinates into a single list of tuples
    words_and_bounds = list(zip(words, x_coordinates, y_coordinates))

    # Sort the words based on their y-coordinate
    sorted_words = sorted(words_and_bounds, key=lambda word: word[2][0])

    # Group words into lines based on the y-coordinate with buffer
    lines = []
    current_line = []

    for i in range(len(sorted_words) - 1):
        current_word = sorted_words[i]
        next_word = sorted_words[i + 1]

        # Check if the y-coordinate difference is within the buffer range
        if abs(current_word[2][0] - next_word[2][0]) <= buffer:
            current_line.append(current_word)
        else:
            current_line.append(current_word)
            lines.append(current_line)
            current_line = []
    
    # Add the last line
    current_line.append(sorted_words[-1])
    lines.append(current_line)

    # Extract boundary box vertices for each line
    lines_with_bounds = []
    for line in lines:
        line_words, x_coords, y_coords = zip(*line)
        
        leftmost_x = min(min(x) for x in x_coords)
        rightmost_x = max(max(x) for x in x_coords)
        uppermost_y = min(min(y) for y in y_coords)
        lowermost_y = max(max(y) for y in y_coords)

        bounds_vertices = [(leftmost_x, uppermost_y), (rightmost_x, uppermost_y),
                           (rightmost_x, lowermost_y), (leftmost_x, lowermost_y)]

        lines_with_bounds.append((line_words, bounds_vertices))

    rows = []
    bounds = []

    for i, line in enumerate(lines_with_bounds, 1):
        words, bound = line
        row = f"{' '.join(words)}"
        rows.append(row)
        bounds.append(bound)

    return rows, bounds

if __name__ == '__main__':
    # Example input data
    output = (['Look', 'what', 'they', 'need', 'to', 'mimic', 'a', 'fraction', 'of', 'our', 'power'],
            [[130, 217, 217, 130], [231, 324, 324, 231], [335, 420, 420, 335], [434, 523, 523, 434],
            [538, 576, 576, 538], [81, 193, 193, 81], [208, 228, 228, 208], [241, 378, 378, 241],
            [399, 436, 436, 399], [448, 510, 510, 448], [525, 642, 642, 525]],
            [[726, 726, 759, 759], [726, 727, 760, 759], [727, 727, 760, 760], [727, 727, 761, 761],
            [728, 728, 761, 761], [769, 770, 801, 800], [770, 770, 800, 800], [770, 771, 802, 801],
            [772, 772, 802, 802], [772, 772, 803, 803], [773, 774, 804, 803]])

    # Group words into lines with a buffer of 5 pixels
    lines_with_bounds = linegroup(output, buffer=5)
    print(lines_with_bounds)
    # rows = []
    # bounds = []
    # # Display the result
    # for i, line in enumerate(lines_with_bounds, 1):
    #     words, bound = line
    #     row = f"{' '.join(words)}"
    #     rows.append(row)
    #     bounds.append(bound)

    # print(rows)
    # print(bounds)