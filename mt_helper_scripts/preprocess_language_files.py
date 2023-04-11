import pandas as pd
import os
import jsonlines
import sys
import argparse

def create_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def export_json_files(output_dir, filename, df, src_col='src_col', tgt_col='tgt_col',direction='en-sw'):
    to_be_saved = []
    src_data = df[src_col].values
    tgt_data = df[tgt_col].values
    src_lang, tgt_lang = direction.split('-')
    N_sent = df.shape[0]
    for s in range(N_sent):
        text_string = {"translation": {src_lang:src_data[s], tgt_lang:tgt_data[s]}}
        to_be_saved.append(text_string)

    with jsonlines.open(output_dir+filename, 'w') as writer:
        writer.write_all(to_be_saved)

def csv_to_json(input_path, output_path, source_col, target_col, direction='en-sw', n_sent=None):
    input_files = glob.glob(input_path + '*.tsv') + glob.glob(input_path + '*.csv')  # Get all TSV and CSV files in input directory

    for file in input_files:
        df = pd.read_csv(file, sep='\t') if file.endswith('.tsv') else pd.read_csv(file)  # Read TSV or CSV based on file extension
        sc, tg = df[source_col].values[:n_sent], df[target_col].values[:n_sent]

        df_sctg = pd.DataFrame(sc, columns=['src_col'])
        df_sctg['tgt_col'] = tg

        # Output data
        output_dir = output_path
        create_dir(output_dir)

        output_file = os.path.splitext(os.path.basename(file))[0] + '.json'
        export_json_files(output_dir, output_file, df_sctg, direction=direction)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lafand Text Processing Tool")
    parser.add_argument("function", type=str, choices=["csv_to_json", "export_json_files"], help="Function to call")
    parser.add_argument("input_path", type=str, help="Path to input CSV file")
    parser.add_argument("-o", "--output_path", type=str, default="data/json_files/en_yo_lafand/", help="Path to output JSON files (default: data/json_files/en_yo_lafand/)")
    parser.add_argument("-s", "--source_col", type=str, help="Name of the source text column")
    parser.add_argument("-t", "--target_col", type=str, help="Name of the target text column")
    parser.add_argument("-d", "--direction", type=str, help="Translation direction (e.g. en-sw)")
     
    args = parser.parse_args()

    if args.function == "combine_texts_lafand":
        if not args.source_col or not args.target_col or not args.direction:
            print("Error: Please provide source column, target column, and direction.")
            sys.exit(1)
        csv_to_json(args.input_path, args.output_path, args.source_col, args.target_col, direction=args.direction)
    elif args.function == "export_json_files":
         sys.exit(1)
    else:
        print("Error: Invalid function. Please choose from 'combine_texts_lafand' or 'export_json_files'.")
        sys.exit(1)
