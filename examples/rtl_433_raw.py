#!/usr/bin/env python
"""
$ rtl_433 file.cu8 -w OOK:- | rtl_433_raw

A script to convert rtl_433 OOK output to RAW style output used by esphome or Flipper Zero.
eg. https://esphome.io/components/remote_transmitter.html transmit_raw

Greg Cormier
"""
import sys
import argparse;

# Set this if you don't want your entire array on a single line
maxLineLength = 80
firstNegative = False       # Is the first pulse negative
formatChunk = False


def rtl_433_raw():
    doneChunk = False
    lineLength = 0
    rawString = "["

    while True:
        line = sys.stdin.readline().strip()
        
        if not line:
            break
        
        if line[0].isdigit():
            try:
                doneChunk = False
                lineLength += len(line) + 5
                #print(f':{line}')
                num1, num2 = map(int, line.split())
                if firstNegative:
                    rawString += f"-{num1}, {num2}, "
                else:
                    rawString += f"{num1}, -{num2}, "
                    
            except ValueError:
                print(f'Error: {line}')
                continue

            if lineLength > maxLineLength:
                rawString += "\n"
                lineLength = 0
        elif line[0] == ';' and formatChunk and not doneChunk:
            rawString += "\n\n"
            lineLength = 0
            doneChunk = True

    rawString += "]"        
    print(f'{rawString}')


if __name__ == "__main__":
    dup_test = {}
    parser = argparse.ArgumentParser(description="Convert rtl_433 OOK output to RAW style output.")
    parser.add_argument('--firstNegative', action='store_true', help='Set the first pulse to negative')
    parser.add_argument('--maxLineLength', type=int, default=80, help='Set the maximum line length for output formatting purposes')
    parser.add_argument('--formatChunk', action='store_true', help='Put breaks in the output when the input has comments suggesting a new chunk of data')
    args = parser.parse_args()

    if args.firstNegative:
        firstNegative = True
    
    if args.maxLineLength:
        maxLineLength = args.maxLineLength

    if args.formatChunk:
        formatChunk = True
    
    rtl_433_raw()
