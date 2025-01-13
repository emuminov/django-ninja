with import <nixpkgs> {};
mkShell {
  venvDir = "./.venv";
  buildInputs = with pkgs.python3Packages; [
    python
    venvShellHook
    python3Packages.python-lsp-server
    ruff
    python3Packages.python-lsp-ruff
  ];
  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    pip install -r requirements.txt
  '';
  postShellHook = ''
    # allow pip to install wheels
    unset SOURCE_DATE_EPOCH
  '';
}
