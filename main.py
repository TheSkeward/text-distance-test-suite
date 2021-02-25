"""Utility to test which textdistance algorithm will work best for your use case"""
import logging
import textdistance

TESTS = [
    textdistance.hamming,
    textdistance.levenshtein,
    textdistance.damerau_levenshtein,
    textdistance.jaro,
    textdistance.jaro_winkler,
    textdistance.strcmp95,
    textdistance.needleman_wunsch,
    textdistance.gotoh,
    textdistance.smith_waterman,
    textdistance.jaccard,
    textdistance.sorensen,
    textdistance.sorensen_dice,
    textdistance.tversky,
    textdistance.overlap,
    textdistance.tanimoto,
    textdistance.cosine,
    textdistance.monge_elkan,
    textdistance.bag,
    textdistance.ratcliff_obershelp,
    textdistance.arith_ncd,
    textdistance.bwtrle_ncd,
    textdistance.sqrt_ncd,
    textdistance.entropy_ncd,
    textdistance.bz2_ncd,
    textdistance.lzma_ncd,
    textdistance.zlib_ncd,
    textdistance.mra,
    textdistance.editex,
    textdistance.length,
]

LEN_TESTS = [
    textdistance.lcsseq,
    textdistance.lcsstr,
    textdistance.prefix,
    textdistance.postfix,
]
logging.basicConfig(level=logging.INFO)


def compare_strings(str1, str2):
    """Compares two strings using every test in the suite, and returns a list of results."""
    results = []
    for test in TESTS:
        result = test(str1, str2)
        logging.debug(
            "%s and %s: %s with %s", str1, str2, result, str(test).split("(")[0]
        )
        results.append([result, str(test).split("(")[0]])
    for test in LEN_TESTS:
        result = len(test(str1, str2))
        logging.debug(
            "%s and %s: %s with %s", str1, str2, result, str(test).split("(")[0]
        )
        results.append((result, str(test).split("(")[0]))
    return results


def run_suite(inputs):
    """Takes a list of lists of strings, where items inside a sublist should return a match,
    and items in separate sub-lists should not return a match,
    and compares each string to each other using a variety of text distance algorithms."""
    match_performance = dict()
    diff_performance = dict()
    for i, lst in enumerate(inputs):
        if len(lst) > 1:
            for j, str1 in enumerate(lst):
                j_offset = j + 1
                for str2 in lst[j_offset:]:
                    results = compare_strings(str1, str2)
                    for result, test in results:
                        match_performance[test] = match_performance.get(test, []) + [
                            result
                        ]
        i_offset = i + 1
        for j, lst2 in enumerate(inputs[i_offset:], i_offset):
            for str1 in lst:
                for str2 in lst2:
                    results = compare_strings(str1, str2)
                    for result, test in results:
                        diff_performance[test] = diff_performance.get(test, []) + [
                            result
                        ]
    print_results(diff_performance, match_performance)


def print_results(diff_performance, match_performance):
    """Takes in the dicts of results and prints the results in a human-readable form."""
    logging.debug("Full results for matching strings: %s", match_performance)
    logging.debug("Full results for different strings: %s", diff_performance)
    ans = []
    for test in match_performance:
        if test in DISTANCE_BASED:
            if max(match_performance[test]) < min(diff_performance[test]):
                ans.append(test)
            match_performance[test] = (
                (sum(match_performance[test]) / len(match_performance[test])),
                max(match_performance[test]),
            )
            diff_performance[test] = (
                (sum(diff_performance[test]) / len(diff_performance[test])),
                min(diff_performance[test]),
            )
        else:
            if min(match_performance[test]) > max(diff_performance[test]):
                ans.append(test)
            match_performance[test] = (
                sum(match_performance[test]) / len(match_performance[test]),
                min(match_performance[test]),
            )
            diff_performance[test] = (
                (sum(diff_performance[test]) / len(diff_performance[test])),
                max(diff_performance[test]),
            )
    if len(ans) > 1:
        logging.info(
            "The following algorithms are the clear best fit for these strings - every comparison "
            "of a matching string scored as a better match than every comparison of a non-matching "
            "string: %s",
            ans,
        )
    elif len(ans) == 1:
        logging.info(
            "The following algorithm is the clear best fit for these strings - uniquely among "
            "tested algorithms, every comparison of a matching string scored as a better match "
            "than every comparison of a non-matching string: %s",
            ans,
        )
    logging.info(
        "Below is a representation of the results test, in the format 'test': (average, "
        "worst_match) for the matching strings, and 'test': (average, best_match) for the "
        "non-matching strings. You can change the logging level to DEBUG if you'd like to see more "
        "detailed results."
    )
    logging.info(str(match_performance)[1:-1])
    logging.info(str(diff_performance)[1:-1])


DISTANCE_BASED = [
    "Hamming",
    "Levenshtein",
    "DamerauLevenshtein",
    "Bag",
    "ArithNCD",
    "BWTRLENCD",
    "SqrtNCD",
    "EntropyNCD",
    "BZ2NCD",
    "LZMANCD",
    "ZLIBNCD",
    "Editex",
]
EXAMPLE_INPUT = [
    [
        "Emcurix Technologies",
        "Emcurix Technologies (old DO NOT USE)",
        "Equipment ONLY - Emcurix Technologies",
        "Emcurix Tech, Inc.",
    ],
    [
        "Elairt Metal SA - Central Office",
        "*** DO NOT USE *** Elairt Metal",
        "Elairt Metal, SA",
    ],
    [
        "Ship to Lurplex Aerospace gmbh",
        "Lurplex Aero, gmbh Munich",
        "Lurplex Aerospace tech (use Lurplex Aero, gmbh Munich acct 84719482-A)",
    ],
]

if __name__ == "main":
    run_suite(EXAMPLE_INPUT)
