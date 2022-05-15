import os
import math
import pandas as pd
from valentine import valentine_match, valentine_metrics
from valentine.algorithms import SimilarityFlooding

def one_to_one_matches(matches: dict):
    set_match_values = set(matches.values())

    if len(set_match_values) < 2:
        return matches

    matched = dict()

    for key in matches.keys():
        matched[key[0]] = False
        matched[key[1]] = False

    median = list(set_match_values)[math.ceil(len(set_match_values)/2)]

    matches1to1 = dict()

    for key in matches.keys():
        if (not matched[key[0]]) and (not matched[key[1]]):
            similarity = matches.get(key)
            if similarity >= median:
                matches1to1[key] = similarity
                matched[key[0]] = True
                matched[key[1]] = True
            else:
                break
    return matches1to1

for k in range(1, 15):
    name = f'pair_{k}'
    data_path = f'./homework-2/Data/{name}/'
    df1 = pd.read_csv(os.path.join(data_path, 'Table1.csv'))
    df2 = pd.read_csv(os.path.join(data_path, 'Table2.csv'))

    matcher = SimilarityFlooding()
    matches = valentine_match(df1, df2, matcher)

    result = {}
    for match in matches:
        temp = result.get(match[0][1], {})
        temp[match[1][1]]  = matches[match]
        result[match[0][1]] = temp

    result_matrix_path = f'./homework-2/Result/{name}.csv'
    df = pd.DataFrame(result)
    df.to_csv(result_matrix_path)

    ground_truth = [tuple(line.strip('<>\n').split(', ')) for line in open(os.path.join(data_path, 'mapping.txt'), 'r').readlines()]
    metrics = valentine_metrics.all_metrics(matches, ground_truth)

    result_mapping_path = f'./homework-2/Result/{name}_mapping.txt'
    mapping_result = one_to_one_matches(matches)
    mapping_output = ['<'] * 2
    for pair in mapping_result:
        mapping_output[0] += pair[0][1] + ', '
        mapping_output[1] += pair[1][1] + ', '
    mapping_output[0] = mapping_output[0][:-2] + '>'
    mapping_output[1] = mapping_output[1][:-2] + '>'

    open(result_mapping_path, 'w').write('\n'.join(mapping_output))