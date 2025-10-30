# SWAN

SWAN (SWipeable ANnotations) is an open-source, MIT-licensed web application for fast and intuitive histopathology image annotation. Instead of slow, folder-based sorting, SWAN enables swipe-based classification on both desktop and mobile devices, supports flexible label mapping, and logs annotations and metadata in real time. Designed to reduce fatigue and make large-scale annotation more accessible, SWAN offers a lightweight, browser-based interface that allows pathologists and researchers to efficiently label image patches anytime, including on the go.

## Interface Example

This is the final result of a fully configured application and dataset in action.

![Swipe Interface in Educational Mode](docs/ui-swipe-example.png)

## Post User-Study Questionnaires

The following are the links to the post-study questionnaires that were filled ba the study participants:

SWAN (Initial Phase) - https://forms.gle/N5tsQu185kVoqUki8 <br>
SWAN (Enhanced) - https://forms.gle/fsEnC4iupWuspQHaA

## Security

### Verifying commits

```sh
# configure allowed signers
git config gpg.ssh.allowedSignersFile known_signers

# view signatures for commits
git log --show-signature
```
