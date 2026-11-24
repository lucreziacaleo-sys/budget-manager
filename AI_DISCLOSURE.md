## Tool used
Claude (Anthropic), used as a code reviewer and tutor while finishing the project.
Gemini (Google): helped me fix issues in the code while I was working on it.

## What I wrote myself 
I wrote the first version of all five modules: models.py (the Transaction schema), validation.py, services.py, storage.py, and cli.py, following the layered structure
from the brief. I also changed the menu prompt from "Select an option:" to a 
clearer one after testing the app and seeing that it was easy to type the wrong 
thing there. 

## What the AI did
I asked the AI to check my project against the assignment brief. It ran the code 
and found these issues: 

Bugs that crashed the app: a typo in the services.py (I wrote self._transaction without the
s at the end), an undefined variable in the list view of cli.py (I wrote amount instead of 
tx.amount), and errors.append(str) in storage.py, which printed <class 'str'> instead of 
the error message. 

Validation gaps: impossible dates like 2026-13-45 were accepted, nan and inf were 
accepted as amounts, the empty-ID message didn't name the field, and duplicates IDs
in the CSV were not caught. 

Design issues: saving overwrote the sample file and erased the invalid rows, 
the summary added EUR and USD together, and the data path depended on the folder 
the app was started from. 

For each problem, the AI explained where to make a change and why, and I 
applied the changes to my files myself. In addition, the AI wrote the test file (tests/test_budget.py),pytest.ini, the sample data, and drafts of README.md and DESIGN.md.

## Why I used it 
Fixing issues (Gemini): I used Gemini to help me understand and fix problems I ran into while writing the code, before the final review with Claude.

To get a second check before submitting, to find edge cases I hadn't thought of, and to
learn how to write tests with pytest. It was my first time writing tests with pytest. I used the AI's tests as a model to learn the structure (`assert`, `pytest.raises`, `tmp_path`) and checked that each test matches a rule in my code. One test caught a real indentation bug in my summary()function, which I then fixed. |

My README.md was empty I used the AI to draft it in the structure the brief asks for (setup → run → example → test → known limitations), then checked that the commands work on my Mac, that the example numbers match the real output of my app, and that the menu prompt matches my version.

For the DESIGN.md The AI drafted the paragraph from the design decisions we discussed while fixing the code. I checked that it describes my architecture correctly.



## How I checked the AI's work 
I ran python -m pytest. At first one test failed (the summary showed EUR net balance
as 0.0). With the AI's help I found that lines 26–30 of summary() were indented outside
the for loop, so only the last transaction was counted. After fixing the indentation,
all 9 tests passed.

I ran the app myself (`PYTHONPATH=src python -m budget_manager.cli`): I listed
transactions, viewed the summary per currency, added a transaction and quit.

I read every change and can explain what it does.