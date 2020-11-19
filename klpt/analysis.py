#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import re
sys.path.append('../klpt')
from .configuration import Configuration
from .preprocess import Preprocess
import klpt

class Analysis:


    def __init__(self, dialect, script):

        self.eps = '@0@'
        self.initial_state = 0;
        self.accepting_states = set(); # finals
        self.states = set()
        self.transitions = {}
        self.alphabet = set()

        # validate parameters
        if dialect == "Kurmanji":
            with open(klpt.get_data("data/kmr-analyser.att")) as analysis_file:
                self.load(analysis_file)
        elif dialect == "Sorani":
            with open(klpt.get_data("data/ckb-analyser.att")) as analysis_file:
                self.load(analysis_file)
    
    def load(self, analysis_file):
        for line in analysis_file.readlines():
            row = line.strip('\n\t').split('\t') 
            if len(row) == 2:
                self.accepting_states.add(int(row[0]))
                self.states.add(int(row[0]))
                #print(row)
            elif len(row) == 5:
                i_state = int(row[0])
                o_state = int(row[1])
                self.states.add(i_state)
                self.states.add(o_state)
                i_sym = row[2]
                o_sym = row[3]                
                self.alphabet.add(i_sym)
                self.alphabet.add(o_sym)
                if (i_state, i_sym) not in self.transitions:
                    self.transitions[(i_state, i_sym)] = []
                self.transitions[(i_state, i_sym)].append((o_sym, o_state))
    
    def closure(self, S, reached_states):    # Calculate epsilon closure over state S
    
        if S not in self.state_output_pairs:
            self.state_output_pairs[S] = set();
    
        if (S, self.eps) in self.transitions:
            for state in self.transitions[(S, self.eps)]:
                reached_states.add(state[1]);
    
                if state[1] not in self.state_output_pairs:
                    self.state_output_pairs[state[1]] = set();
    
                for pair in self.state_output_pairs[S]:
                    if state[0] == self.eps:
                        self.state_output_pairs[state[1]].add((pair[0], state[1]));
                    else: 
                        self.state_output_pairs[state[1]].add((pair[0] + state[0], state[1]));
    
                self.closure(state[1], reached_states);
    
        return reached_states;
    
    def step(self, S, c):            # Step the transducer
        reached_states = set();
    
#        if S in self.accepting_states:
#            return set([S]);
    
        if (S, c) in self.transitions: 
            for state in self.transitions[(S, c)]:
                self.closure(state[1], reached_states);
                reached_states.add(state[1]);
    
                if state[1] not in self.state_output_pairs:
                    self.state_output_pairs[state[1]] = set();
    
                for pair in self.state_output_pairs[S]:
                    if state[0] == self.eps:
                        self.state_output_pairs[state[1]].add((pair[0], state[1]));
                    else: 
                        self.state_output_pairs[state[1]].add((pair[0] + state[0], state[1]));
    
                self.closure(state[1], reached_states);
    
        return reached_states;

    def analyse(self, word):
        self.state_output_pairs = {};           # A structure to contain the list of "alive state-output pairs" 
        self.state_output_pairs[0] = set([(self.eps, 0)]); 
        self.accepting_output_pairs = set();    # The set of state-output pairs that are accepting
        self.current_states = set([self.initial_state]); # Set containing the set of current states
        i = 0
        while True:            # Loop until no input remains
            reached_states = set()
            if i == len(word):
                for state in self.current_states:
                    reached_states = self.closure(state, reached_states)
                    del self.state_output_pairs[state]
                break
            #print(i, word[i], self.current_states, self.state_output_pairs) 
            for state in self.current_states:
                if state not in self.state_output_pairs:
                    self.state_output_pairs[state] = set();
                reached_states = reached_states.union(self.step(state, word[i]))
                del self.state_output_pairs[state]
        
            self.current_states = reached_states;
            i += 1
 
        accepting_output_pairs = []
        for state in self.state_output_pairs:
            #print(state, self.accepting_states, self.state_output_pairs[state])
            if state in self.accepting_states:
                accepting_output_pairs.append(list(self.state_output_pairs[state]))
        
       
        return (word, accepting_output_pairs)
