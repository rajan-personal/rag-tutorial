#!/bin/bash

echo "Running Step 1: Converting to Black and White..."
python3 "step_1_convert_B&W.py"
echo

echo "Running Step 2: Filling Colors..."
python3 "step_2_Fill_color.py"
echo

echo "Running Step 3: Computing results..."
echo
python3 "step_3_No_of_Color_on_each_Line.py"
echo

echo "All steps completed!"