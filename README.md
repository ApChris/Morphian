# Morphian

Morphian is a Python3 script that generates unique possible user passwords based on user-provided characteristics. It can be used as an ethical hacking tool to assess password security or for educational purposes.

## Installation

1. Clone the repository or download the `morphian.py` script.
2. Ensure you have Python 3.x installed on your system.
3. Install the required dependencies by running the following command:

## Usage

1. Clone the repository or download the `morphian.py` script.
2. Ensure you have Python 3.x installed on your system.
3. Run the script using the following command:

```
python morphian.py
```
Follow the prompts to enter various characteristics such as name, surname, birthday, hobby, etc.

## Output
Morphian will generate a list of unique possible user passwords by combining the provided characteristics. The generated passwords will be categorized into four different strength levels:

- Strength 0: Too guessable - risky password (guesses < 10^3).
- Strength 1: Very guessable - protection from throttled online attacks (guesses < 10^6).
- Strength 2: Somewhat guessable - protection from unthrottled online attacks (guesses < 10^8).
- Strength 3: Safely unguessable - moderate protection from offline slow-hash scenario (guesses < 10^10).
- Strength 4: Very unguessable - strong protection from offline slow-hash scenario (guesses >= 10^10).

The strength levels and corresponding protection descriptions are based on the zxcvbn library. Please refer to their repository and the `readme.md` for more detailed information.

The generated passwords will be appended to the respective text files:

- `weak.txt`: Contains passwords categorized as too guessable (strength 0).
- `average.txt`: Contains passwords categorized as very guessable (strength 1).
- `strong.txt`: Contains passwords categorized as somewhat guessable (strength 2) or safely unguessable (strength 3).
- `verystrong.txt`: Contains passwords categorized as very unguessable (strength 4).

Please check the respective files to find the generated passwords for each strength level.


Examples

...
Note
Please ensure you use this tool responsibly and only on systems you have proper authorization to assess. Be mindful of any legal and ethical implications when using this tool.

License
Morphian is licensed under the GNU General Public License v3.0.