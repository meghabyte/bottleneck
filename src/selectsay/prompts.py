RULE_PROMPT_PREFIX = '''You will be given a list of (OBSERVATION, ACTION, REWARD) examples collected from two agents learning to solve a task.
Possible ACTIONS an agent can take are: 1, 2, 3, 4, 5, and quit.\n
Each OBSERVATION describes the ordered sequence of actions that AGENT 1 picks, and each ACTION describes the ACTION that AGENT 2 picks based on the given OBSERVATION.\n
The examples are separated into HIGH REWARD and LOW REWARD examples.\n'''
RULE_PROMPT_SUFFIX = '''Output a language instruction that best summarizes the strategy AGENT 2 should follow to receive HIGH REWARD, not LOW REWARD, based on the examples.\n
Start the instruction with the prefix 'I should'.\n'''