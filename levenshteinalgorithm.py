def calculate_similarity(original, transcribed):
    # Calculate Levenshtein distance
    def levenshtein_distance(s1, s2):
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    # Calculate similarity as a percentage
    max_length = max(len(original), len(transcribed))
    distance = levenshtein_distance(original, transcribed)
    similarity_percentage = 100 * (1 - distance / max_length)

    return max(0, similarity_percentage)  # Ensure the result is at least 0%

if __name__ == '__main__':
    # Example usage:
    original_transcript = "This is the original transcript."
    transcribed_transcript = "This is the best transcript."

    similarity = calculate_similarity(original_transcript, transcribed_transcript)
    print(f"Similarity: {similarity:.2f}%")
