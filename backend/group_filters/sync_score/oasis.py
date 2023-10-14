def oasis(
    word_bins_user1: list[list[str]],
    smile_user1: list[float],
    word_bins_user2: list[list[str]],
    smile_user2: list[float],
    window_size: int,
    n_bins: int,
    energy_threshold: float = 0.1,
) -> float:
    sync_score_list = list()
    original_bin = word_bins_user1[0]
    for i, word in enumerate(original_bin):
        # Initialize the synchrony score as 0
        sync_score = 0

        # Calculate the signal energy for AU data of both user
        energy_user1 = calc_signal_energy(i * window_size, window_size, smile_user1)
        energy_user2 = calc_signal_energy(i * window_size, window_size, smile_user2)
        min_energy = min(energy_user1, energy_user2)

        # Continue only if the minimum signal energy > threshold
        if min_energy > energy_threshold:
            n_buckets = len(word_bins_user2)
            for j, compare_bin in enumerate(word_bins_user2):
                if i < len(compare_bin):
                    offset_coefficient = 1 - (j / n_buckets)
                    if sync_score >= offset_coefficient:
                        break

                    # Calculate shape similarity
                    compare_word = compare_bin[i]
                    shape_similarity = 1 - calc_euclidean_word_distance(
                        word, compare_word, n_bins
                    )

                    # Calculate value similarity
                    energy_user2_with_offset = calc_signal_energy(
                        (i * window_size) + j, window_size, smile_user2
                    )
                    value_similarity = 1 - (
                        abs((energy_user1 - energy_user2_with_offset)) / window_size
                    )

                    # Update synchrony score
                    sync_score = max(
                        sync_score,
                        offset_coefficient * shape_similarity * value_similarity,
                    )

        for _ in range(window_size):
            sync_score_list.append(sync_score)
    return sync_score_list


def calc_signal_energy(pos, window_size, signal):
    sum = 0
    for i in range(window_size):
        if pos + i < len(signal):
            sum += abs(signal[pos + i])
    return sum / window_size


def calc_euclidean_word_distance(word, compare_word, num_bins):
    distance = 0
    for c1, c2 in zip(word, compare_word):
        char_distance = abs(ord(c1) - ord(c2)) / (num_bins - 1)
        distance += char_distance
    return distance / len(word)
