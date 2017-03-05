# Trivia 40 - Doesn't Our Logo Look Cool?

![AlexCTF logo](logo.png)

### Solution

The flag format for this ctf is `ALEXCTF{[A-Za-z0-9_]*}`.
Run `tr` to delete any character that isn't in the set.

    tr -dC 'A-Za-z0-9_{}' < logo.txt

### Flag

    ALEXCTF{0UR_L0G0_R0CKS}
