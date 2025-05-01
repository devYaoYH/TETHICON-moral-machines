from re import A
import pandas as pd
import argparse
from moralmachines_task.prompt_templates import STAY, CHANGE

ATTRIBUTE_LEVEL_REPLACEMENT = {
    "older": "Old",
    "younger": "Young", 
}

def parse_output(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Extract only needed columns
    df = df[['answer', 'problem_code', 'consistent', 'coherent']]

    # Define columns for problem code
    code_cols = [
        "Language",
        "ScenarioType",
        "AttributeLevel",
        "Intervention",
        "Barrier",
        "CrossingSignal",
        "Characters",
    ]

    # Check if Answer is valid
    valid_answers = STAY | CHANGE

    # Create two rows for each original row
    rows = []
    for _, row in df.iterrows():
        codes = row['problem_code'].split('|')
        if len(codes) != 2:
            print(f"Warning: Skipping malformed problem_code: {row['problem_code']}")
            continue

        # Verify if Answer is valid
        row['answer'] = row['answer'].lower()
        if row['answer'] not in valid_answers:
            print(f"Warning: Invalid Answer: {row['answer']}")
            continue

        # Unnest problem code
        change_data = codes[0].split(',')
        stay_data = codes[1].split(',')

        # Backward compatibility, align coding to 2018 expt
        if change_data[2] in ATTRIBUTE_LEVEL_REPLACEMENT:
            change_data[2] = ATTRIBUTE_LEVEL_REPLACEMENT[change_data[2]]
        if stay_data[2] in ATTRIBUTE_LEVEL_REPLACEMENT:
            stay_data[2] = ATTRIBUTE_LEVEL_REPLACEMENT[stay_data[2]]

        # Capitalize ScenarioType and AttributeLevel columns
        change_data[1] = change_data[1].capitalize()
        change_data[2] = change_data[2].capitalize()
        stay_data[1] = stay_data[1].capitalize()
        stay_data[2] = stay_data[2].capitalize()

        # Compute PedPed
        pedped = 1 if (int(change_data[4]) == int(stay_data[4]) == 0) else 0

        # Add CHANGE row
        change_row = {
            'problem_code': codes[0],
            'answer': row['answer'],
            'status': 'CHANGE',
            'Saved': 1 if row['answer'] not in CHANGE else 0,
        }
        change_row.update({
            code_cols[i]: change_data[i] for i in range(len(code_cols))
        })
        change_row["ScenarioTypeStrict"] = change_data[1]
        change_row["PedPed"] = pedped
        change_row["consistent"] = row['consistent']
        change_row["coherent"] = row['coherent']
        rows.append(change_row)

        # Add STAY row
        stay_row = {
            'problem_code': codes[1],
            'answer': row['answer'],
            'status': 'STAY',
            'Saved': 1 if row['answer'] not in STAY else 0,
        }
        stay_row.update({
            code_cols[i]: stay_data[i] for i in range(len(code_cols))
        })
        stay_row["ScenarioTypeStrict"] = stay_data[1]
        stay_row["PedPed"] = pedped
        stay_row["consistent"] = row['consistent']
        stay_row["coherent"] = row['coherent']
        rows.append(stay_row)

    # Create new dataframe from processed rows
    result_df = pd.DataFrame(rows)
    
    # Save to new CSV file
    result_df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Parse moral machine experiment output')
    parser.add_argument('input_file', help='Path to input CSV file')
    parser.add_argument('output_file', help='Path to output CSV file')
    
    args = parser.parse_args()
    parse_output(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
