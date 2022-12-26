
# Unbabel Backend Engineering Challenge 2022

The ensuing document pertains to the backend engineering challenge presented by Unbabel. It consists of a simple command line application that parses a stream of translations and computes the average delivery time per minute, within a specified time window.

## Included Files

- `README.md` (this file)
- `unbabel_challenge.py` (solution)
- `events.json` (test input_file)
- `events_2.json` (test input_file)
- `events_3.json` (test input_file)

# Task description

The task is to produce a .json output file containing the average delivery times per minute according to a .json input file of translation events.

# Solution
This standalone software project was written in Python 3.11.0.

## Build and run

Download the `unbabel_challenge.py`  and `.json` files. Open the command prompt and go to the same directory where the files were stored. Run the following command in the command prompt:
```bash
python3 unbabel_challenge.py --input_file 'events.json' --window_size 10
```
The command above runs the `unbabel_challenge.py` script which accepts as arguments the `.json` file `events.json` and counts, for each minute, the moving average delivery time of all translations for the past 10 minutes.

## Input file

In the context of this problem, the `.json` input file format is modeled according to:
```json
[{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}
,{"timestamp": "2018-12-26 18:13:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 31}]
```

## Output file

The application produces a simple .json obeying the following schema:
```json
[
 {
  "date": "2018-12-26 18:11:00",
  "average_delivery_time": 0
 },
 {
  "date": "2018-12-26 18:12:00",
  "average_delivery_time": 20.0
 },
 {
  "date": "2018-12-26 18:13:00",
  "average_delivery_time": 20.0
 },
 {
  "date": "2018-12-26 18:14:00",
  "average_delivery_time": 25.5
 }
]
```
## Considerations

* One should avoid looping over the entire list of `jsons`, at each minute, and then select the valid timestamps according to the specified time window. Indeed, for large `.json` files, this approach would quickly become cumbersome, as the execution time would grow proportionally to the file's size.

* The present solution considers two indexes, `idx_in` and `idx_out`, whose roles are to point at the translation events inside the list of `jsons` which are be either included or removed, respectively, from the computation of the moving average delivery time.


