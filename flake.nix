{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    utils,
    ...
  }:
    utils.lib.eachDefaultSystem
    (
      system: let
        pkgs = import nixpkgs {inherit system;};
      in rec
      {
        # Used by `nix develop`
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python311Packages.pygame
          ];
        };
      }
    );
}
