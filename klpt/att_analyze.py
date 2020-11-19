#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import re
sys.path.append('../klpt')
import klpt

class Analysis:
    """
    Utility for reading .att format automata and transducers from the Apertium project. Particuarly used to integrate the [Kurmanji part](https://github.com/apertium/apertium-kmr) in KLPT

    Returns:
        [str]: [output of the Apertium morphological analyzer]
    """
    

    def __init__(self, dialect="Kurmanji", script="Latin"):

        self.eps = '@0@'
        self.initial_state = 0;
        self.accepting_states = set(); # finals
        self.states = set()
        self.transitions = {}
        self.alphabet = set()
        
        # validate parameters
        if dialect == "Kurmanji" and script == "Latin":
            with open(klpt.get_data("data/kmr-Latn.att")) as analysis_file:
                self.load(analysis_file)
        else:
            raise Exception("dialect not supported")
        # elif dialect == "Sorani":
        #     with open(klpt.get_data("data/ckb-analyser.att")) as analysis_file:
        #         self.load(analysis_file)
    
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

    def analyze(self, word):
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

# a = Analysis("Kurmanji", "Latin")
# print(a.analyze('dibêjim'))
# # att_result_2 = a.analyse('dengdanekê')
# # print(a.analyse('xêzikine'))
# att_result = a.analyse('nikarim')
# # It returns a tuple in the form of ('nikarim', [[('@0@karîn<vblex><tv><neg><pri><p1><sg>', 12669)]]) or ('dengdanekê', [[('@0@dengdan<n><f><sg><con><ind>', 12669), ('@0@dengdan<n><f><sg><obl><ind>', 12669)]])
# # different parts of this should be separated, structured and returned as a list of dictionaires
# analysis_dict = dict()

# word_forms = ["dengdanekê", "nikarim", "xêzikine", "dixwî"]
# for word_form in word_forms:
#     for form_analysis in list(a.analyse(word_form)[-1]):
#         print(word_form)
#         for analysis in form_analysis:
#             structure = analysis[0].rsplit('@', 1)[1].split("<", 1)
#             analysis_dict["base"], analysis_dict["description"] = structure[0], structure[1].replace("><", "_").replace(">", "").strip()
#             analysis_dict["terminal_suffix"] = word_form.replace(analysis_dict["base"], "")
#             print(analysis_dict)


# [{'pos': 'verb', 'description': 'past_stem_transitive_active', 'base': 'دیت', 'terminal_suffix': 'بامن'}]
