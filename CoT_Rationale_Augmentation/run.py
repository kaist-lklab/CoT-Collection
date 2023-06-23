import argparse
import json
import os
from multiprocessing import Process
from time import sleep

from utils import LLM, AugmentedDataset


def parse_args():
    parser = argparse.ArgumentParser()


    parser.add_argument('--key',type=str,default='./personal_info.json', help='path to json file containing api keys')
    parser.add_argument('--model_name', type=str, default='code-davinci-002')
    parser.add_argument('--max_tokens', type=int, default=1024)
    parser.add_argument('--temperature', type=float, default=0.7)
    parser.add_argument('--top_p', type=float, default=0.95)
    parser.add_argument('--num_samples', type=int, default=1)
    parser.add_argument('--presence_penalty', type=float, default=1.0)
    parser.add_argument('--frequency_penalty', type=float, default=1.0)


    parser.add_argument("--data_file", type=str,default="/home/seungone/ART/data_extraction/data/train/cbqa_train_phase1_10000.json",required=True)
    parser.add_argument('--data_coverage',type=str,choices=['t0','t0p','flan','sni','additional',"few_shot"],default='flan')
    parser.add_argument('--split', type=str, choices=['train','korean','japanese','chinese','french','russian'] , default='train')
    parser.add_argument("--base_dir",type=str, default="./")
    

    parser.add_argument('--mode',type=str,choices=["single", "multi"], default = "single")
    parser.add_argument('--request_per_minute', type=int, default=60)


    args = parser.parse_args()

    return args



def load_keys(args):
    with open(args.key,'r') as f:
        key = json.load(f)
    key = list(key.values())
    return key

def run_llm(key,idx,num_keys):
    args = parse_args()
    data_int = AugmentedDataset(args, idx, num_keys)
    llm = LLM(args, key, data_int)
    llm.run()

def main(args):
    keys = load_keys(args)
    processes = []
    for idx, key in enumerate(keys):
        process = Process(target=run_llm, args=(key,idx,len(keys)))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


    total_data = AugmentedDataset(args, 0, 100000)
    total_data.merge_results()


if __name__=="__main__":
    args = parse_args()
    main(args)
    


