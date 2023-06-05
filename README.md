# Singer Tap Copier Template

To use this [`copier`](https://copier.readthedocs.io) template:

```bash
pip3 install pipx
pipx ensurepath
# You may need to reopen your shell at this point
pipx install copier
```

Initialize `copier` template directly from Git:

```bash
copier copy --UNSAFE gh:edgarrmondragon/singer-tap-copier-template path/to/destination
```

Or locally from an already-cloned template repo:

```bash
copier copy --UNSAFE . path/to/destination
```

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html).
